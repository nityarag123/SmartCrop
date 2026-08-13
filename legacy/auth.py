# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import db as db_module
import mongo_auth
import local_auth

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (email and password):
            flash('Email and password are required', 'danger')
            return render_template('register.html')

        # Hash the password
        pw_hash = generate_password_hash(password)

        try:
            conn = db_module.get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                    (name, email, pw_hash)
                )
                conn.commit()
                cur.close()

                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE email=%s", (email,))
                row = cur.fetchone()
                cur.close()
            finally:
                db_module.close_conn(conn)

            if row:
                session['user_id'] = row['id'] if isinstance(row, dict) else row[0]
                session['auth_backend'] = 'database'
                return redirect(url_for('main.dashboard'))

        except Exception as e:
            try:
                if mongo_auth.is_configured():
                    user = mongo_auth.create_user(name, email, pw_hash)
                    session['user_id'] = user['id']
                    session['auth_backend'] = 'mongo'
                    flash('Registered with MongoDB Atlas because MySQL is unavailable.', 'warning')
                    return redirect(url_for('main.dashboard'))
            except ValueError as mongo_error:
                flash('Registration failed: ' + str(mongo_error), 'danger')
                return render_template('register.html')
            except Exception:
                pass

            try:
                user = local_auth.create_user(name, email, pw_hash)
                session['user_id'] = user['id']
                session['auth_backend'] = 'local'
                flash('Registered with local storage because database is unavailable.', 'warning')
                return redirect(url_for('main.dashboard'))
            except ValueError as local_error:
                flash('Registration failed: ' + str(local_error), 'danger')
                return render_template('register.html')
            except Exception:
                flash('Registration failed: ' + str(e), 'danger')
                return render_template('register.html')

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = db_module.get_conn()
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, password_hash FROM users WHERE email=%s", (email,))
                row = cur.fetchone()
                cur.close()
            finally:
                db_module.close_conn(conn)

            if row:
                user_id = row['id'] if isinstance(row, dict) else row[0]
                stored_hash = row['password_hash'] if isinstance(row, dict) else row[1]

                if check_password_hash(stored_hash, password):
                    session['user_id'] = user_id
                    session['auth_backend'] = 'database'
                    return redirect(url_for('main.dashboard'))

            flash('Invalid email or password', 'danger')

        except Exception:
            if mongo_auth.is_configured():
                try:
                    user = mongo_auth.get_user_by_email(email)
                    if user and check_password_hash(user['password_hash'], password):
                        session['user_id'] = user['id']
                        session['auth_backend'] = 'mongo'
                        flash('Logged in with MongoDB Atlas because MySQL is unavailable.', 'warning')
                        return redirect(url_for('main.dashboard'))
                except Exception:
                    pass

            user = local_auth.get_user_by_email(email)
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['auth_backend'] = 'local'
                flash('Logged in using local storage because database is unavailable.', 'warning')
                return redirect(url_for('main.dashboard'))

            flash('Invalid email or password', 'danger')

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('auth_backend', None)
    return redirect(url_for('index'))
