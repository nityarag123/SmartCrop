"""Seed data for SmartCrop.

- government_schemes : real, well-known central government schemes. Sources are
  official government portals. State schemes are listed as placeholders that a
  deployment should complete from the relevant state agriculture department.
- crop_calendar     : agronomy knowledge base (sowing..harvesting timelines).
"""
import os

from .models.db import get_store

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


GOVERNMENT_SCHEMES = [
    {
        "code": "pm-kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Central",
        "summary": "Income support of Rs. 6,000 per year to eligible landholding farmer families.",
        "benefits": "Rs. 2,000 every 4 months, transferred directly to the bank account.",
        "eligibility": [
            "All landholding farmer families with cultivable land",
            "Exclusions apply (institutional landholders, income-tax payers etc.)",
        ],
        "documents": ["Aadhaar", "Land records", "Bank account", "Self-declaration"],
        "process": "Apply/verify on the PM-KISAN portal or through the state government's beneficiary list.",
        "source": "https://pmkisan.gov.in/",
    },
    {
        "code": "pmfby",
        "name": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        "category": "Central",
        "summary": "Crop insurance scheme protecting farmers against crop loss from natural calamities, pests and diseases.",
        "benefits": "Low premium (2% kharif, 1.5% rabi food crops, 5% commercial); full claim settlement on notified losses.",
        "eligibility": [
            "All farmers growing notified crops in notified areas",
            "Tenant farmers and sharecroppers can also be covered",
        ],
        "documents": ["Loan records or land records", "Aadhaar", "Bank account", "Crop details"],
        "process": "Enrol through bank, Common Service Centre (CSC) or insurance company before the notified cut-off date each season.",
        "source": "https://pmfby.gov.in/",
    },
    {
        "code": "kcc",
        "name": "Kisan Credit Card (KCC)",
        "category": "Central",
        "summary": "Flexible credit card for farmers covering crop, investment, and allied activities.",
        "benefits": "Affordable crop loans, flexible withdrawals, interest subvention available on timely repayment.",
        "eligibility": [
            "Farmers, tenant farmers, and sharecroppers",
            "Farmers in animal husbandry and fisheries under the scheme",
        ],
        "documents": ["Aadhaar", "Land records or lease agreement", "Passport photos", "Bank account"],
        "process": "Apply at any bank branch or through a Common Service Centre; banks issue KCC after verification.",
        "source": "https://www.nabard.org/",
    },
    {
        "code": "pmksy",
        "name": "PMKSY (Pradhan Mantri Krishi Sinchayee Yojana)",
        "category": "Central",
        "summary": "'More crop per drop' — improves water use efficiency with irrigation and rainwater harvesting.",
        "benefits": "Support for micro-irrigation (drip/sprinkler), water harvesting structures and command area development.",
        "eligibility": [
            "Farmers, farmer groups and water user associations",
            "Gram Panchayats for water harvesting structures",
        ],
        "documents": ["Land records", "Aadhaar", "Bank account", "Project/beneficiary details"],
        "process": "Apply through the state agriculture department or district mission office implementing PMKSY.",
        "source": "https://pmksy.gov.in/",
    },
    {
        "code": "soil-health-card",
        "name": "Soil Health Card (SHC)",
        "category": "Central",
        "summary": "Soil testing at the farm level with personalised fertiliser recommendations.",
        "benefits": "Free/near-free soil testing and a card with N, P, K and micronutrient guidance for 2 years.",
        "eligibility": ["All farmers with cultivable land"],
        "documents": ["Land records", "Farmer details", "Aadhaar"],
        "process": "Soil sample collected by the state soil testing lab; card issued through the soil health card portal.",
        "source": "https://www.soilhealth.dac.gov.in/",
    },
    {
        "code": "enam",
        "name": "e-NAM (National Agriculture Market)",
        "category": "Central",
        "summary": "Online pan-India trading platform connecting mandis for better prices.",
        "benefits": "Transparent price discovery, online bidding, direct payment to farmers' accounts.",
        "eligibility": [
            "Farmers registered with an e-NAM-enabled mandi",
            "Farmers' producer organisations and traders on the platform",
        ],
        "documents": ["Aadhaar", "Bank account", "Farmer registration at linked mandi"],
        "process": "Register at your nearest e-NAM mandi or through the e-NAM portal/mobile app.",
        "source": "https://enam.gov.in/",
    },
    {
        "code": "pkvy",
        "name": "PKVY (Paramparagat Krishi Vikas Yojana)",
        "category": "Central",
        "summary": "Promotes organic farming in clusters with certification support.",
        "benefits": "Cluster-based organic farming, Rs. 50,000 per hectare support (3 years), certification assistance.",
        "eligibility": ["Farmers who want to take up organic farming", "Farmer clusters/groups"],
        "documents": ["Land records", "Aadhaar", "Bank account", "Cluster participation"],
        "process": "Apply through the state agriculture department; clusters are formed by the implementing agency.",
        "source": "https://pgsindia-ncof.gov.in/",
    },
    {
        "code": "kisan-call-centre",
        "name": "Kisan Call Centre (KCC Helpline)",
        "category": "Central",
        "summary": "Free helpline where farmers can ask agriculture questions in local languages.",
        "benefits": "Expert advice on crops, pests, weather, and schemes — toll free.",
        "eligibility": ["Any farmer"],
        "documents": ["None (call based)"],
        "process": "Call 1800-180-1551 (toll free) from any phone.",
        "source": "https://www.mkisan.gov.in/",
    },
    {
        "code": "state-scheme",
        "name": "State Agriculture Schemes",
        "category": "State",
        "summary": "Each state runs its own subsidy and input-support programmes for farmers.",
        "benefits": "Varies by state — input subsidies, equipment subsidy, free power, seeds etc.",
        "eligibility": ["Farmers resident in the respective state"],
        "documents": ["Land records", "Aadhaar", "Bank account"],
        "process": "Contact your state agriculture department / district agriculture office for the current list.",
        "source": "State Agriculture Department",
    },
]


# Realistic reference timelines (weeks after sowing). Distances between phases
# are real agronomy guidance; exact dates depend on variety and weather.
CROP_CALENDAR_KB = {
    "rice": {
        "seasons": ["kharif", "rabi"],
        "soil": "Clay loam to loamy soil, retains water",
        "phases": [
            {"phase": "Sowing/Nursery", "week_start": 1, "week_end": 3, "activity": "Prepare nursery beds; transplant 25-30 day old seedlings"},
            {"phase": "Transplanting", "week_start": 4, "week_end": 5, "activity": "Transplant seedlings at 20x15 cm spacing in puddled field"},
            {"phase": "Germination/Establishment", "week_start": 5, "week_end": 6, "activity": "Maintain 3-5 cm standing water for early establishment"},
            {"phase": "Irrigation", "week_start": 4, "week_end": 16, "activity": "Keep field flooded 3-5 cm during tillering and panicle initiation"},
            {"phase": "Fertilization", "week_start": 4, "week_end": 10, "activity": "Split N: 50% at transplant, 25% at tillering, 25% at panicle initiation"},
            {"phase": "Pest monitoring", "week_start": 6, "week_end": 16, "activity": "Watch for stem borer, leaf folder, blast and brown spot"},
            {"phase": "Flowering", "week_start": 12, "week_end": 14, "activity": "Ensure adequate water; avoid drought at flowering"},
            {"phase": "Harvesting", "week_start": 17, "week_end": 18, "activity": "Harvest at 20-25% grain moisture, thresh and dry"},
        ],
    },
    "wheat": {
        "seasons": ["rabi"],
        "soil": "Well drained loam to clay loam",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 100-125 kg/ha seed at 2.5-3 cm depth, 20-22 cm row spacing"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "Light irrigation within 3-4 weeks if moisture low"},
            {"phase": "Irrigation", "week_start": 3, "week_end": 16, "activity": "Irrigate at crown root, tillering, jointing, flowering and grain filling"},
            {"phase": "Fertilization", "week_start": 1, "week_end": 5, "activity": "Full P&K at sowing; N split at crown root and tillering"},
            {"phase": "Pest monitoring", "week_start": 8, "week_end": 16, "activity": "Watch for rust, aphids, termites and loose smut"},
            {"phase": "Flowering", "week_start": 12, "week_end": 14, "activity": "Adequate moisture at flowering improves grain set"},
            {"phase": "Harvesting", "week_start": 17, "week_end": 19, "activity": "Harvest when straw turns yellow and grain hard"},
        ],
    },
    "maize": {
        "seasons": ["kharif", "rabi", "zaid"],
        "soil": "Well drained sandy loam to loam",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 20 kg/ha at 60x25 cm spacing with good moisture"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "Keep soil moist for uniform germination"},
            {"phase": "Irrigation", "week_start": 3, "week_end": 14, "activity": "Critical stages: knee-high, tasseling, silking and grain filling"},
            {"phase": "Fertilization", "week_start": 2, "week_end": 8, "activity": "Basal P&K; N split at knee-high and pre-tasseling"},
            {"phase": "Pest monitoring", "week_start": 4, "week_end": 14, "activity": "Watch for stem borer, fall armyworm and shoot fly"},
            {"phase": "Flowering", "week_start": 10, "week_end": 12, "activity": "Tasseling to silking; avoid moisture stress"},
            {"phase": "Harvesting", "week_start": 15, "week_end": 17, "activity": "Harvest when husks dry and grains hard with black layer"},
        ],
    },
    "sugarcane": {
        "seasons": ["kharif", "spring"],
        "soil": "Deep, well drained loam",
        "phases": [
            {"phase": "Planting", "week_start": 1, "week_end": 3, "activity": "Plant healthy setts with 2-3 buds in furrows"},
            {"phase": "Germination", "week_start": 2, "week_end": 4, "activity": "Maintain moisture for sett sprouting"},
            {"phase": "Irrigation", "week_start": 4, "week_end": 50, "activity": "Regular irrigation; critical at tillering, grand growth and maturity"},
            {"phase": "Fertilization", "week_start": 4, "week_end": 16, "activity": "Split N as per growth; apply P&K at planting"},
            {"phase": "Pest monitoring", "week_start": 8, "week_end": 40, "activity": "Watch for shoot borer, top borer, whitefly and smut"},
            {"phase": "Flowering/Canopy", "week_start": 24, "week_end": 32, "activity": "Grand growth phase; ensure sunlight and nutrition"},
            {"phase": "Harvesting", "week_start": 44, "week_end": 52, "activity": "Harvest 10-12 months after planting at optimum maturity"},
        ],
    },
    "cotton": {
        "seasons": ["kharif"],
        "soil": "Deep black cotton soil to well drained loam",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 8-10 kg/ha at 90x60 cm spacing"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "Ensure soil moisture for emergence"},
            {"phase": "Irrigation", "week_start": 4, "week_end": 24, "activity": "Avoid waterlogging; irrigate at flowering and boll development"},
            {"phase": "Fertilization", "week_start": 2, "week_end": 10, "activity": "Basal P&K; N split at squaring and flowering"},
            {"phase": "Pest monitoring", "week_start": 6, "week_end": 26, "activity": "Watch for bollworm, aphids, jassids and whitefly"},
            {"phase": "Flowering", "week_start": 12, "week_end": 14, "activity": "Peak flowering; avoid stress for better retention"},
            {"phase": "Harvesting", "week_start": 24, "week_end": 28, "activity": "Pick bolls as they open; harvest in 2-3 pickings"},
        ],
    },
    "groundnut": {
        "seasons": ["kharif", "rabi"],
        "soil": "Light well drained sandy loam",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 100-120 kg/ha pod kernels at 30x10 cm"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "Keep moisture for emergence"},
            {"phase": "Irrigation", "week_start": 3, "week_end": 16, "activity": "Light irrigations; critical at pegging and pod filling"},
            {"phase": "Fertilization", "week_start": 1, "week_end": 4, "activity": "Apply gypsum at flowering; basal P and K at sowing"},
            {"phase": "Pest monitoring", "week_start": 5, "week_end": 16, "activity": "Watch for leaf miner, aphids, rust and tikka leaf spot"},
            {"phase": "Flowering/Pegging", "week_start": 5, "week_end": 8, "activity": "Pegs enter soil; avoid deep ploughing"},
            {"phase": "Harvesting", "week_start": 16, "week_end": 18, "activity": "Harvest when pods mature and haulms yellow"},
        ],
    },
    "soybean": {
        "seasons": ["kharif"],
        "soil": "Well drained loam to clay loam, pH 6-7.5",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 60-70 kg/ha at 30-45 cm row spacing"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "Moisture required for uniform stand"},
            {"phase": "Irrigation", "week_start": 4, "week_end": 12, "activity": "Irrigate at flowering and pod filling; avoid waterlogging"},
            {"phase": "Fertilization", "week_start": 1, "week_end": 3, "activity": "Low N (inoculate seed); P and K as basal"},
            {"phase": "Pest monitoring", "week_start": 4, "week_end": 13, "activity": "Watch for defoliators, girdle beetle and yellow mosaic"},
            {"phase": "Flowering", "week_start": 6, "week_end": 8, "activity": "Moisture critical at flowering"},
            {"phase": "Harvesting", "week_start": 13, "week_end": 15, "activity": "Harvest when leaves drop and pods rattle"},
        ],
    },
    "chickpea": {
        "seasons": ["rabi"],
        "soil": "Well drained sandy loam to clay loam",
        "phases": [
            {"phase": "Sowing", "week_start": 1, "week_end": 2, "activity": "Sow 75-100 kg/ha at 30x10 cm"},
            {"phase": "Germination", "week_start": 1, "week_end": 2, "activity": "One light irrigation for establishment"},
            {"phase": "Irrigation", "week_start": 4, "week_end": 15, "activity": "Irrigate at branching and pod development; avoid excess"},
            {"phase": "Fertilization", "week_start": 1, "week_end": 3, "activity": "Basal P; low nitrogen (legume)"},
            {"phase": "Pest monitoring", "week_start": 5, "week_end": 16, "activity": "Watch for pod borer and wilt"},
            {"phase": "Flowering", "week_start": 9, "week_end": 11, "activity": "Protect flowers; manage pod borer"},
            {"phase": "Harvesting", "week_start": 16, "week_end": 18, "activity": "Harvest when pods turn brown and plants dry"},
        ],
    },
    "potato": {
        "seasons": ["rabi"],
        "soil": "Well drained sandy loam, loose and friable",
        "phases": [
            {"phase": "Sowing/Planting", "week_start": 1, "week_end": 2, "activity": "Plant disease-free seed tubers 45-60 g at 60x20 cm"},
            {"phase": "Germination/Emergence", "week_start": 1, "week_end": 2, "activity": "Emergence in 2-3 weeks with moisture"},
            {"phase": "Irrigation", "week_start": 3, "week_end": 12, "activity": "Frequent light irrigation; critical at tuber initiation"},
            {"phase": "Fertilization", "week_start": 2, "week_end": 5, "activity": "Basal P&K; N split at planting and earthing up"},
            {"phase": "Pest monitoring", "week_start": 4, "week_end": 12, "activity": "Watch for late blight and aphids"},
            {"phase": "Flowering/Tubers", "week_start": 7, "week_end": 9, "activity": "Earthing up; maintain moisture for tuber bulking"},
            {"phase": "Harvesting", "week_start": 12, "week_end": 14, "activity": "Harvest after haulms dry and skin sets"},
        ],
    },
    "tomato": {
        "seasons": ["rabi", "zaid"],
        "soil": "Well drained loam, pH 6-7",
        "phases": [
            {"phase": "Nursery sowing", "week_start": -5, "week_end": -3, "activity": "Sow seeds in nursery 4-6 weeks before transplanting"},
            {"phase": "Transplanting", "week_start": 1, "week_end": 2, "activity": "Transplant 25-30 day seedlings at 60x45 cm"},
            {"phase": "Irrigation", "week_start": 1, "week_end": 14, "activity": "Regular light irrigation; avoid moisture stress at flowering"},
            {"phase": "Fertilization", "week_start": 2, "week_end": 8, "activity": "Basal P; N&K split at vegetative and fruiting stages"},
            {"phase": "Pest monitoring", "week_start": 4, "week_end": 14, "activity": "Watch for fruit borer, whitefly and early/late blight"},
            {"phase": "Flowering/Fruiting", "week_start": 6, "week_end": 10, "activity": "Staking and pruning improve fruit quality"},
            {"phase": "Harvesting", "week_start": 10, "week_end": 14, "activity": "Harvest at breaker-to-pink stage for market"},
        ],
    },
}


def seed():
    """Seed collections only when they are empty (idempotent)."""
    store = get_store()

    if not store.find_one("government_schemes"):
        store.insert_many("government_schemes", GOVERNMENT_SCHEMES)
