"""AI Farm Assistant chat APIs."""
from flask import Blueprint, request

from ..chatbot.fallback import answer as fallback_answer
from ..chatbot.llm import get_llm
from ..chatbot.translation import translate
from ..models.db import get_store
from ..models.users import public_user
from ..utils.helpers import ok, error, login_required, current_user

bp = Blueprint("api_chat", __name__)

_SYSTEM = (
    "You are SmartCrop, an AI farming assistant for Indian farmers. Give simple, "
    "practical advice. Never fabricate weather data, government schemes "
    "or dangerous pesticide instructions. For serious cases, recommend professional or "
    "local agricultural guidance. Clearly state uncertainty when you are not sure."
)


@bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    lang = (data.get("lang") or "en").strip().lower()
    if not message:
        return error("Message is required", 400)

    user = current_user()
    llm = get_llm()

    used_llm = False
    if llm.available():
        try:
            context = ""
            if user:
                context = (f"The farmer is located in {user.get('location') or 'unknown place'}. "
                           f"Current crop: {user.get('current_crop') or 'not set'}.")
            reply = llm.chat(message, _SYSTEM + "\n" + context, lang)
            used_llm = True
        except Exception:
            reply, _ = fallback_answer(message, user)
    else:
        reply, _ = fallback_answer(message, user)

    display = translate(reply, lang) if lang != "en" else reply
    translated = lang != "en"

    get_store().insert("chat_history", {
        "user_id": user["id"] if user else None,
        "message": message,
        "response": display,
        "language": lang,
        "engine": "LLM" if used_llm else "knowledge-base",
    })

    return ok({
        "response": display,
        "engine": "LLM" if used_llm else "knowledge-base",
        "translated": translated,
        "language": lang,
        "profile": public_user(user) if user else None,
    })


@bp.route("/chat/history", methods=["GET"])
@login_required
def history():
    user = current_user()
    if not user:
        return error("Not logged in", 401)
    rows = get_store().find(
        "chat_history",
        {"user_id": user["id"]},
        sort=[("created_at", -1)],
        limit=50,
    )
    rows.reverse()
    return ok({"messages": rows})
