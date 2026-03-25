import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
import random
import string
from datetime import datetime, date

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CalFoodConnect",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Storage (JSON files, no DB) ───────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
CAPACITY_FILE      = os.path.join(DATA_DIR, "capacity.json")

def read_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def today():
    return str(date.today())

# ── Session state bootstrap ───────────────────────────────────────────────────
defaults = {
    "dark_mode":       True,
    "logged_in":       False,
    "role":            None,
    "user_code":       None,
    "user_name":       "",
    "family_size":     1,
    "registered_bank": None,
    "checked_in":      False,
    "page":            "🏠 Home",
    "show_login":      None,
    # Registration form
    "show_reg_form":   False,
    "reg_target_bank": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────
def gen_code():
    return "#" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

def load_registrations():
    return read_json(REGISTRATIONS_FILE, {})

def save_registrations(data):
    write_json(REGISTRATIONS_FILE, data)

def load_capacity():
    saved = read_json(CAPACITY_FILE, {})
    for b in BANKS:
        if b not in saved:
            saved[b] = 50
    return saved

def save_capacity(data):
    write_json(CAPACITY_FILE, data)

def get_bank_registrations(bank):
    regs = load_registrations()
    t    = today()
    return {k: v for k, v in regs.items()
            if v.get("bank") == bank and v.get("date") == t
            and v.get("status") in ("registered", "checked_in")}

def get_slots_left(bank):
    cap  = load_capacity().get(bank, 50)
    used = len(get_bank_registrations(bank))
    return max(0, cap - used)

def register_user(bank, profile):
    """profile is a dict with all 15 form fields."""
    regs = load_registrations()
    code = gen_code()
    family_size = (
        int(profile.get("children", 0)) +
        int(profile.get("adults",   0)) +
        int(profile.get("seniors",  0))
    )
    family_size = max(family_size, 1)
    regs[code] = {
        # slot / operational fields
        "bank":          bank,
        "family_size":   family_size,
        "name":          profile.get("first_name", "Anonymous"),
        "date":          today(),
        "status":        "registered",
        "registered_at": datetime.now().strftime("%H:%M"),
        "checked_in_at": None,
        "served_at":     None,
        # client profile fields
        "consent":       profile.get("consent"),
        "birth_year":    profile.get("birth_year"),
        "client_id":     profile.get("client_id"),
        "first_name":    profile.get("first_name"),
        "middle_name":   profile.get("middle_name"),
        "last_name":     profile.get("last_name"),
        "phone":         profile.get("phone"),
        "can_text":      profile.get("can_text"),
        "address":       profile.get("address"),
        "city":          profile.get("city"),
        "zip_code":      profile.get("zip_code"),
        "children":      profile.get("children"),
        "seniors":       profile.get("seniors"),
        "adults":        profile.get("adults"),
        "race_ethnicity":profile.get("race_ethnicity"),
    }
    save_registrations(regs)
    return code, family_size

def checkin_user(code):
    regs = load_registrations()
    if code in regs and regs[code]["status"] == "registered":
        regs[code]["status"]        = "checked_in"
        regs[code]["checked_in_at"] = datetime.now().strftime("%H:%M")
        save_registrations(regs)
        return True
    return False

def deregister_user(code):
    regs = load_registrations()
    if code in regs:
        regs[code]["status"] = "cancelled"
        save_registrations(regs)
        return True
    return False

def mark_served(code):
    regs = load_registrations()
    if code in regs:
        regs[code]["status"]    = "served"
        regs[code]["served_at"] = datetime.now().strftime("%H:%M")
        save_registrations(regs)
        return True
    return False

# ── Registration form ─────────────────────────────────────────────────────────
RACE_OPTIONS = [
    "Prefer not to say",
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Hispanic or Latino",
    "Middle Eastern or North African",
    "Native Hawaiian or Other Pacific Islander",
    "White",
    "Two or more races",
    "Other",
]

def render_registration_form(bank):
    """
    Renders the full Second Harvest client registration form.
    Returns (submitted: bool, profile: dict | None).
    Must be called inside the main page body (not inside another form).
    """
    accent = "#00d4aa"
    border = "#2a2a3a" if st.session_state.dark_mode else "#dde2ee"
    muted  = "#6b6b8a"

    st.markdown(f"""
    <div style="background:{'#111118' if st.session_state.dark_mode else '#fff'};
                border:1px solid {border};border-radius:16px;
                padding:32px 36px;margin-bottom:24px;">
      <div style="display:inline-block;background:{accent}18;border:1px solid {accent}44;
                  color:{accent};font-size:.7rem;font-weight:700;text-transform:uppercase;
                  letter-spacing:.1em;padding:3px 12px;border-radius:99px;margin-bottom:16px;">
        📋 Client Registration — Second Harvest
      </div>
      <div style="font-family:'Syne',times-new-roman;font-size:1.4rem;font-weight:800;margin-bottom:6px;">
        Register at {bank}
      </div>
      <div style="color:{muted};font-size:.88rem;margin-bottom:6px;">
        Please complete all required fields. This information is kept confidential
        and used only by Second Harvest food network staff.
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("client_registration_form", clear_on_submit=False):

        # ── Section 1: Consent ──────────────────────────────────────────────
        st.markdown("#### 1 · Consent")
        consent = st.radio(
            "Do you consent to have your data stored by Second Harvest?  \\*",
            options=["Yes", "No"],
            horizontal=True,
            index=0,
        )

        st.markdown("<hr style='border-color:#2a2a3a;margin:20px 0 16px'>",
                    unsafe_allow_html=True)

        # ── Section 2: Identity ─────────────────────────────────────────────
        st.markdown("#### 2 · Identity")
        col_by, col_id = st.columns(2)
        with col_by:
            birth_year = st.number_input(
                "Birth Year  \\*",
                min_value=1900, max_value=date.today().year,
                value=1980, step=1,
            )
        with col_id:
            client_id = st.text_input("Client ID", placeholder="Leave blank if new client")

        col_fn, col_mn, col_ln = st.columns([2, 1, 2])
        with col_fn:
            first_name = st.text_input("First Name  \\*", placeholder="First name")
        with col_mn:
            middle_name = st.text_input("Middle Name", placeholder="Optional")
        with col_ln:
            last_name = st.text_input("Last Name  \\*", placeholder="Last name")

        st.markdown("<hr style='border-color:#2a2a3a;margin:20px 0 16px'>",
                    unsafe_allow_html=True)

        # ── Section 3: Contact ──────────────────────────────────────────────
        st.markdown("#### 3 · Contact")
        col_ph, col_txt = st.columns([2, 1])
        with col_ph:
            phone = st.text_input("Phone Number  \\*", placeholder="(555) 000-0000")
        with col_txt:
            can_text = st.radio(
                "Can we text you?  \\*",
                options=["Yes", "No"],
                horizontal=True,
                index=0,
            )

        address  = st.text_input("Street Address  \\*", placeholder="123 Main St")
        col_city, col_zip = st.columns([3, 1])
        with col_city:
            city = st.text_input("City  \\*", placeholder="City")
        with col_zip:
            zip_code = st.text_input("Zip Code  \\*", placeholder="00000")

        st.markdown("<hr style='border-color:#2a2a3a;margin:20px 0 16px'>",
                    unsafe_allow_html=True)

        # ── Section 4: Household ────────────────────────────────────────────
        st.markdown("#### 4 · Household Composition")
        st.markdown(
            "<small style='color:#6b6b8a;'>These counts are used to prepare the right amount of food for your family.</small>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        col_ch, col_ad, col_sr = st.columns(3)
        with col_ch:
            children = st.selectbox(
                "Children (0–18 yrs)  \\*",
                options=list(range(0, 11)),
                index=0,
            )
        with col_ad:
            adults = st.selectbox(
                "Adults (19–59 yrs)  \\*",
                options=list(range(0, 11)),
                index=1,
            )
        with col_sr:
            seniors = st.selectbox(
                "Seniors (60+ yrs)  \\*",
                options=list(range(0, 11)),
                index=0,
            )

        total_members = int(children) + int(adults) + int(seniors)
        if total_members > 0:
            st.markdown(
                f"<div style='font-size:.82rem;color:#00d4aa;margin-top:4px;'>"
                f"👥 Total household size: <b>{total_members}</b></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='border-color:#2a2a3a;margin:20px 0 16px'>",
                    unsafe_allow_html=True)

        # ── Section 5: Race & Ethnicity ─────────────────────────────────────
        st.markdown("#### 5 · Race & Ethnicity")
        st.markdown(
            "<small style='color:#6b6b8a;'>Select the option that best describes your household. This information is collected for reporting purposes only.</small>",
            unsafe_allow_html=True,
        )
        st.markdown("")
        race_ethnicity = st.selectbox(
            "Race / Ethnicity of Household  \\*",
            options=RACE_OPTIONS,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Submit ──────────────────────────────────────────────────────────
        submitted = st.form_submit_button(
            "✅ Submit & Secure My Slot",
            use_container_width=True,
        )

    if submitted:
        # Validation
        errors = []
        if consent != "Yes":
            errors.append("You must consent to data storage to register.")
        if not first_name.strip():
            errors.append("First name is required.")
        if not last_name.strip():
            errors.append("Last name is required.")
        if not phone.strip():
            errors.append("Phone number is required.")
        if not address.strip():
            errors.append("Street address is required.")
        if not city.strip():
            errors.append("City is required.")
        if not zip_code.strip():
            errors.append("Zip code is required.")
        if total_members == 0:
            errors.append("Household must have at least 1 member.")

        if errors:
            for e in errors:
                st.error(e)
            return False, None

        profile = {
            "consent":       consent,
            "birth_year":    int(birth_year),
            "client_id":     client_id.strip() or None,
            "first_name":    first_name.strip(),
            "middle_name":   middle_name.strip() or None,
            "last_name":     last_name.strip(),
            "phone":         phone.strip(),
            "can_text":      can_text,
            "address":       address.strip(),
            "city":          city.strip(),
            "zip_code":      zip_code.strip(),
            "children":      int(children),
            "adults":        int(adults),
            "seniors":       int(seniors),
            "race_ethnicity":race_ethnicity,
        }
        return True, profile

    return False, None


def reg_button(bank, key_suffix):
    """
    Renders a Register button. On click, sets show_reg_form + reg_target_bank
    and reruns so the form appears at the top of the page.
    Only shown when user is logged in, not already registered, and slots exist.
    """
    if not (st.session_state.logged_in and st.session_state.role == "user"):
        st.info("Log in as a Visitor to register.")
        return
    left = get_slots_left(bank)
    if st.session_state.registered_bank == bank:
        st.info("✅ You are registered here.")
    elif st.session_state.registered_bank:
        st.warning("Leave your current queue first to register here.")
    elif left == 0:
        st.error("No slots available today.")
    else:
        if st.button(f"📋 Register at {bank}", key=f"reg_{key_suffix}",
                     use_container_width=True):
            st.session_state.show_reg_form   = True
            st.session_state.reg_target_bank = bank
            st.session_state.page            = "✅ My Check-In"
            st.rerun()


# ── Static data ───────────────────────────────────────────────────────────────
BANKS = [
    "SF Food Bank", "LA Regional Bank", "Sacramento Harvest",
    "San Diego Share", "Oakland Community", "Fresno Food Net",
    "San Jose Pantry", "Bakersfield Aid"
]

BANK_COORDS = {
    "SF Food Bank":       (37.7749, -122.4194),
    "LA Regional Bank":   (34.0522, -118.2437),
    "Sacramento Harvest": (38.5816, -121.4944),
    "San Diego Share":    (32.7157, -117.1611),
    "Oakland Community":  (37.8044, -122.2712),
    "Fresno Food Net":    (36.7378, -119.7871),
    "San Jose Pantry":    (37.3382, -121.8863),
    "Bakersfield Aid":    (35.3733, -119.0187),
}

@st.cache_data
def load_inventory():
    rows = [
        ("SF Food Bank","Rice",320,14,45,"OK"),
        ("SF Food Bank","Canned Beans",180,5,30,"Low"),
        ("SF Food Bank","Pasta",240,21,25,"OK"),
        ("SF Food Bank","Bread",60,3,40,"Critical"),
        ("SF Food Bank","Cooking Oil",90,18,15,"OK"),
        ("SF Food Bank","Canned Corn",110,6,20,"Low"),
        ("SF Food Bank","Baby Formula",40,4,10,"Critical"),
        ("LA Regional Bank","Rice",500,20,80,"OK"),
        ("LA Regional Bank","Canned Tuna",200,7,35,"Low"),
        ("LA Regional Bank","Pasta",310,15,50,"OK"),
        ("LA Regional Bank","Bread",80,2,60,"Critical"),
        ("LA Regional Bank","Milk (UHT)",150,9,40,"Low"),
        ("LA Regional Bank","Cereal",220,25,30,"OK"),
        ("LA Regional Bank","Peanut Butter",95,11,20,"OK"),
        ("Sacramento Harvest","Rice",180,30,30,"OK"),
        ("Sacramento Harvest","Canned Soup",140,6,25,"Low"),
        ("Sacramento Harvest","Pasta",160,22,20,"OK"),
        ("Sacramento Harvest","Bread",45,4,35,"Critical"),
        ("Sacramento Harvest","Eggs",70,3,28,"Critical"),
        ("Sacramento Harvest","Oatmeal",120,18,15,"OK"),
        ("San Diego Share","Canned Beans",230,12,40,"OK"),
        ("San Diego Share","Rice",280,16,55,"OK"),
        ("San Diego Share","Bread",55,5,45,"Low"),
        ("San Diego Share","Baby Formula",30,3,8,"Critical"),
        ("San Diego Share","Pasta",190,20,25,"OK"),
        ("San Diego Share","Canned Corn",100,7,18,"Low"),
        ("Oakland Community","Rice",210,11,38,"OK"),
        ("Oakland Community","Canned Tuna",130,6,22,"Low"),
        ("Oakland Community","Bread",35,2,30,"Critical"),
        ("Oakland Community","Cereal",180,19,25,"OK"),
        ("Oakland Community","Peanut Butter",75,14,18,"OK"),
        ("Oakland Community","Cooking Oil",60,8,12,"Low"),
        ("Fresno Food Net","Rice",400,25,65,"OK"),
        ("Fresno Food Net","Pasta",270,17,35,"OK"),
        ("Fresno Food Net","Bread",90,4,50,"Critical"),
        ("Fresno Food Net","Canned Beans",160,10,28,"OK"),
        ("Fresno Food Net","Milk (UHT)",110,6,32,"Low"),
        ("Fresno Food Net","Oatmeal",95,22,14,"OK"),
        ("San Jose Pantry","Rice",290,13,48,"OK"),
        ("San Jose Pantry","Canned Soup",170,5,30,"Low"),
        ("San Jose Pantry","Bread",50,3,38,"Critical"),
        ("San Jose Pantry","Baby Formula",25,4,7,"Critical"),
        ("San Jose Pantry","Pasta",210,19,28,"OK"),
        ("San Jose Pantry","Cereal",140,16,20,"OK"),
        ("Bakersfield Aid","Rice",350,18,58,"OK"),
        ("Bakersfield Aid","Canned Tuna",155,7,26,"Low"),
        ("Bakersfield Aid","Bread",65,5,42,"Low"),
        ("Bakersfield Aid","Pasta",195,20,30,"OK"),
        ("Bakersfield Aid","Cooking Oil",80,12,16,"OK"),
        ("Bakersfield Aid","Canned Corn",120,6,22,"Low"),
    ]
    return pd.DataFrame(rows, columns=[
        "bank_name","item_name","quantity",
        "days_left","avg_daily_demand","supply_status"
    ])

df = load_inventory()

# ── Theme CSS ─────────────────────────────────────────────────────────────────
def inject_css(dark):
    bg       = "#0a0a0f"      if dark else "#f4f6fb"
    surface  = "#111118"      if dark else "#ffffff"
    surface2 = "#1a1a26"      if dark else "#f0f2f8"
    border   = "#2a2a3a"      if dark else "#dde2ee"
    text     = "#e8e8f0"      if dark else "#0c1228"
    muted    = "#6b6b8a"      if dark else "#6b7280"
    accent   = "#00d4aa"
    accent2  = "#f5a623"
    sb_bg    = "#080810"      if dark else "#0c1228"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Geist+Mono&family=Manrope:wght@400;500;600;700&display=swap');

    html,body,[class*="css"],.stApp{{
        font-family:'Manrope',sans-serif;
        background:{bg}!important;
        color:{text}!important;
    }}
    .stApp{{background:{bg}!important;}}

    section[data-testid="stSidebar"]{{
        background:{sb_bg}!important;
        border-right:1px solid {border};
    }}
    section[data-testid="stSidebar"] *{{color:#e8e8f0!important;}}
    section[data-testid="stSidebar"] .stRadio>label{{display:none;}}
    section[data-testid="stSidebar"] .stRadio label{{
        display:flex!important;padding:10px 16px;border-radius:8px;
        font-size:.9rem;font-weight:500;cursor:pointer;transition:background .15s;
        color:rgba(232,232,240,.7)!important;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover{{
        background:rgba(255,255,255,.06)!important;color:#e8e8f0!important;
    }}

    h1,h2,h3{{font-family:'Syne',sans-serif!important;color:{text}!important;}}

    .lc-card{{
        background:{surface};border:1px solid {border};
        border-radius:12px;padding:24px;margin-bottom:16px;
        transition:border-color .2s,box-shadow .2s;
    }}
    .lc-card:hover{{border-color:{accent}55;box-shadow:0 0 24px {accent}18;}}

    .lc-metric-card{{
        background:{surface};border:1px solid {border};
        border-radius:12px;padding:22px 20px;
        transition:border-color .2s,box-shadow .2s;
    }}
    .lc-metric-card:hover{{border-color:{accent}66;box-shadow:0 0 20px {accent}15;}}
    .lc-metric-icon{{font-size:1.4rem;margin-bottom:8px;}}
    .lc-metric-label{{font-size:.7rem;font-weight:700;text-transform:uppercase;
        letter-spacing:.1em;color:{muted};margin-bottom:4px;}}
    .lc-metric-val{{font-family:'Syne',sans-serif;font-size:2rem;
        font-weight:800;color:{text};}}
    .lc-metric-sub{{font-size:.75rem;color:{muted};margin-top:4px;}}

    .lc-hero{{
        background:{surface};border:1px solid {border};
        border-radius:16px;padding:52px 56px;margin-bottom:28px;
        position:relative;overflow:hidden;
    }}
    .lc-hero::before{{
        content:'';position:absolute;top:-80px;right:-80px;
        width:320px;height:320px;
        background:radial-gradient({accent}22,transparent 70%);
        border-radius:50%;pointer-events:none;
    }}
    .lc-hero::after{{
        content:'';position:absolute;bottom:-60px;left:40%;
        width:200px;height:200px;
        background:radial-gradient({accent2}18,transparent 70%);
        border-radius:50%;pointer-events:none;
    }}
    .lc-hero-tag{{
        display:inline-block;background:{accent}18;
        border:1px solid {accent}44;color:{accent};
        font-size:.72rem;font-weight:700;text-transform:uppercase;
        letter-spacing:.1em;padding:4px 14px;border-radius:99px;margin-bottom:20px;
    }}
    .lc-hero h1{{
        font-family:'Syne',sans-serif!important;
        font-size:clamp(2rem,4vw,3.2rem)!important;
        font-weight:800!important;line-height:1.12!important;
        margin-bottom:16px!important;color:{text}!important;
    }}
    .lc-hero p{{font-size:1.05rem;color:{muted};max-width:540px;line-height:1.65;}}

    .accent{{color:{accent}!important;}}
    .accent2{{color:{accent2}!important;}}

    .pill{{display:inline-block;padding:3px 12px;border-radius:99px;
           font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;}}
    .pill-ok  {{background:{accent}18;border:1px solid {accent}44;color:{accent};}}
    .pill-low {{background:{accent2}18;border:1px solid {accent2}44;color:{accent2};}}
    .pill-crit{{background:#ff4d6d18;border:1px solid #ff4d6d44;color:#ff4d6d;}}
    .pill-reg {{background:#818cf818;border:1px solid #818cf844;color:#818cf8;}}
    .pill-ci  {{background:{accent}18;border:1px solid {accent}44;color:{accent};}}

    .slots-bar-wrap{{background:{border};border-radius:99px;height:6px;margin-top:8px;}}
    .slots-bar{{height:6px;border-radius:99px;
                background:linear-gradient(90deg,{accent},{accent2});transition:width .4s;}}

    .ci-state-box{{border-radius:12px;padding:20px 24px;border:1px solid;margin-top:16px;}}
    .ci-registered{{border-color:{accent}44;background:{accent}0d;}}
    .ci-checkedin{{border-color:{accent2}44;background:{accent2}0d;}}

    .code-box{{
        font-family:'Geist Mono',monospace;font-size:1.6rem;font-weight:700;
        color:{accent};background:{accent}0f;border:1px solid {accent}33;
        border-radius:10px;padding:12px 24px;
        display:inline-block;letter-spacing:.15em;margin:8px 0;
    }}

    .login-wrap{{
        background:{surface};border:1px solid {border};
        border-radius:16px;padding:48px 40px;
        max-width:460px;margin:40px auto;
        box-shadow:0 0 60px {accent}0a;
    }}

    .lc-divider{{border:none;border-top:1px solid {border};margin:28px 0;}}

    .stButton>button{{
        background:{accent}!important;color:#000!important;
        border:none!important;border-radius:8px!important;
        font-weight:700!important;font-family:'Manrope',sans-serif!important;
        padding:10px 24px!important;transition:opacity .15s!important;
    }}
    .stButton>button:hover{{opacity:.85!important;}}

    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div{{
        background:{surface2}!important;border:1px solid {border}!important;
        border-radius:8px!important;color:{text}!important;
        font-family:'Manrope',sans-serif!important;
    }}

    .stTabs [data-baseweb="tab-list"]{{background:{surface2};border-radius:10px;padding:4px;}}
    .stTabs [data-baseweb="tab"]{{
        background:transparent;color:{muted};border-radius:8px;
        font-weight:600;font-family:'Manrope',sans-serif;
    }}
    .stTabs [aria-selected="true"]{{background:{surface}!important;color:{text}!important;}}

    .streamlit-expanderHeader{{
        background:{surface2}!important;border:1px solid {border}!important;
        border-radius:10px!important;font-weight:600!important;color:{text}!important;
    }}
    .streamlit-expanderContent{{
        background:{surface}!important;border:1px solid {border}!important;
        border-top:none!important;border-radius:0 0 10px 10px!important;
    }}

    .stSuccess{{background:{accent}15!important;border-left-color:{accent}!important;}}
    .stWarning{{background:{accent2}15!important;border-left-color:{accent2}!important;}}
    .stError{{background:#ff4d6d15!important;border-left-color:#ff4d6d!important;}}
    .stInfo{{background:#818cf815!important;border-left-color:#818cf8!important;}}

    ::-webkit-scrollbar{{width:6px;height:6px;}}
    ::-webkit-scrollbar-track{{background:{bg};}}
    ::-webkit-scrollbar-thumb{{background:{border};border-radius:99px;}}

    footer{{display:none!important;}}
    #MainMenu{{display:none!important;}}
    header{{display:none!important;}}
    </style>
    """, unsafe_allow_html=True)

inject_css(st.session_state.dark_mode)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 12px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:800;color:#e8e8f0;">
        🥗 CalFoodConnect
      </div>
      <div style="font-size:.68rem;color:#3a3a5a;margin-top:3px;text-transform:uppercase;letter-spacing:.08em;">
        California Food Network
      </div>
    </div>
    """, unsafe_allow_html=True)

    dm = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dm != st.session_state.dark_mode:
        st.session_state.dark_mode = dm
        st.rerun()

    st.markdown("<hr style='border-color:#2a2a3a;margin:10px 0'>", unsafe_allow_html=True)

    # Build nav options based on login state
    if not st.session_state.logged_in:
        nav_opts = ["🏠 Home", "🗺 Map", "🏪 Food Banks", "📦 Find Items"]
    elif st.session_state.role == "user":
        nav_opts = ["🏠 Home", "🗺 Map", "🏪 Food Banks", "📦 Find Items", "✅ My Check-In"]
    else:
        nav_opts = ["🏠 Home", "🗺 Map", "🏪 Food Banks", "📦 Inventory", "📊 Dashboard", "⚙️ Manage"]

    # Ensure current page is valid
    if st.session_state.page not in nav_opts:
        st.session_state.page = nav_opts[0]

    page = st.radio("nav", nav_opts, label_visibility="collapsed",
                    index=nav_opts.index(st.session_state.page))
    st.session_state.page = page

    st.markdown("<hr style='border-color:#2a2a3a;margin:10px 0'>", unsafe_allow_html=True)

    # Auth
    if not st.session_state.logged_in:
        ca, cb = st.columns(2)
        with ca:
            if st.button("👤 Visitor", use_container_width=True):
                st.session_state.show_login = "user"
                st.rerun()
        with cb:
            if st.button("🔑 Host", use_container_width=True):
                st.session_state.show_login = "host"
                st.rerun()
    else:
        role_icon = "👤" if st.session_state.role == "user" else "🔑"
        bank_info = ""
        if st.session_state.role == "user" and st.session_state.registered_bank:
            status_txt = "✅ Checked In" if st.session_state.checked_in else "📋 Registered"
            bank_info  = f'<div style="font-size:.75rem;color:#00d4aa;margin-top:4px;">{status_txt}</div><div style="font-size:.72rem;color:#6b6b8a;">{st.session_state.registered_bank}</div>'

        st.markdown(f"""
        <div style="padding:12px 16px;background:#1a1a26;border-radius:8px;margin-bottom:12px;">
          <div style="font-size:.68rem;color:#6b6b8a;text-transform:uppercase;letter-spacing:.08em;">Signed in as</div>
          <div style="font-weight:700;margin-top:2px;">{role_icon} {st.session_state.user_name or st.session_state.role.title()}</div>
          {f'<div style="font-family:monospace;font-size:.82rem;color:#00d4aa;margin-top:4px;">{st.session_state.user_code}</div>' if st.session_state.user_code else ''}
          {bank_info}
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", use_container_width=True):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.session_state.dark_mode = dm
            st.rerun()

    st.markdown("""
    <div style="position:fixed;bottom:16px;left:0;width:240px;text-align:center;
                font-size:.65rem;color:#3a3a5a;">
      CalFoodConnect · California · 2026
    </div>
    """, unsafe_allow_html=True)

# ── Login screen ──────────────────────────────────────────────────────────────
if st.session_state.show_login and not st.session_state.logged_in:
    role  = st.session_state.show_login
    icon  = "👤" if role == "user" else "🔑"
    title = "Visitor Login" if role == "user" else "Host / Admin Login"
    desc  = ("Find food banks near you, register for a slot, and manage your visit."
             if role == "user" else
             "Manage inventory, approve check-ins, and view live operations.")

    st.markdown(f"""
    <div class="login-wrap">
      <div style="font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:800;margin-bottom:6px;">
        {icon} {title}
      </div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-bottom:28px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form(f"login_form_{role}"):
        name = st.text_input("Your name (optional)", placeholder="Enter your name")
        if role == "host":
            pwd = st.text_input("Host password", type="password", placeholder="Password")
        go  = st.form_submit_button(f"Continue →", use_container_width=True)

        if go:
            if role == "host":
                if pwd == "host123":
                    st.session_state.logged_in  = True
                    st.session_state.role       = "host"
                    st.session_state.user_name  = name or "Host"
                    st.session_state.show_login = None
                    st.session_state.page       = "📊 Dashboard"
                    st.rerun()
                else:
                    st.error("Wrong password. Hint: host123")
            else:
                st.session_state.logged_in   = True
                st.session_state.role        = "user"
                st.session_state.user_name   = name or "Visitor"
                st.session_state.show_login  = None
                st.session_state.page        = "🏠 Home"
                st.rerun()

    if st.button("← Back"):
        st.session_state.show_login = None
        st.rerun()
    st.stop()

# ── Shared helpers ────────────────────────────────────────────────────────────
def slots_bar_html(bank):
    cap   = load_capacity().get(bank, 50)
    used  = len(get_bank_registrations(bank))
    left  = max(0, cap - used)
    pct   = int((used / cap) * 100) if cap else 0
    color = "#00d4aa" if left > 10 else "#f5a623" if left > 0 else "#ff4d6d"
    label = "🟢 Open" if left > 10 else "🟡 Filling up" if left > 0 else "🔴 Full"
    return left, cap, pct, color, label

def avail_label(days_left):
    if days_left <= 2:  return "⚠️ Running out very soon"
    if days_left <= 7:  return "🟡 Limited — visit soon"
    return "🟢 Well stocked"

# ═════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":

    # ── Guest ──
    if not st.session_state.logged_in:
        st.markdown("""
        <div class="lc-hero">
          <div class="lc-hero-tag">🌎 California Food Network</div>
          <h1>Find Food Near You.<br><span class="accent">Today.</span></h1>
          <p>CalFoodConnect connects you to food banks across California in real time.
             See availability, secure a slot, and plan your visit — before you leave home.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        open_banks  = sum(1 for b in BANKS if get_slots_left(b) > 0)
        total_slots = sum(get_slots_left(b) for b in BANKS)

        with c1:
            st.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">🏪</div>
              <div class="lc-metric-label">Food Banks</div>
              <div class="lc-metric-val">{len(BANKS)}</div>
              <div class="lc-metric-sub">Across California</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">✅</div>
              <div class="lc-metric-label">Open Today</div>
              <div class="lc-metric-val">{open_banks}</div>
              <div class="lc-metric-sub">With slots available</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">🎟️</div>
              <div class="lc-metric-label">Slots Available</div>
              <div class="lc-metric-val">{total_slots}</div>
              <div class="lc-metric-sub">Register to secure yours</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.markdown("### 🏪 All Food Banks")
        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            items = df[df["bank_name"] == bank]
            cats  = " · ".join(items["item_name"].tolist()[:4])
            st.markdown(f"""
            <div class="lc-card" style="display:flex;align-items:center;
                 justify-content:space-between;flex-wrap:wrap;gap:12px;">
              <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;">{bank}</div>
                <div style="font-size:.78rem;color:#6b6b8a;margin-top:3px;">🥫 {cats}</div>
              </div>
              <div style="text-align:right;">
                <span style="color:{color};font-weight:700;font-size:.88rem;">{badge}</span>
                <div style="font-size:.75rem;color:#6b6b8a;">{left} slots left</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.info("👤 Click **Visitor** in the sidebar to register at a food bank.")

    # ── User home ──
    elif st.session_state.role == "user":
        name = st.session_state.user_name
        st.markdown(f"""
        <div class="lc-hero">
          <div class="lc-hero-tag">👋 Welcome</div>
          <h1>Hello, <span class="accent">{name}</span>.</h1>
          <p>Find a food bank near you, register for a slot, and check in when you arrive.</p>
        </div>
        """, unsafe_allow_html=True)

        # Status banner
        if st.session_state.registered_bank:
            bank  = st.session_state.registered_bank
            cls   = "ci-checkedin" if st.session_state.checked_in else "ci-registered"
            stxt  = "✅ Checked In" if st.session_state.checked_in else "📋 Registered — not yet arrived"
            st.markdown(f"""
            <div class="ci-state-box {cls}">
              <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;">{stxt}</div>
              <div style="margin-top:6px;font-size:.9rem;color:#6b6b8a;">
                At <b style="color:#e8e8f0;">{bank}</b>
              </div>
              <div class="code-box" style="margin-top:12px;">{st.session_state.user_code}</div>
              <div style="font-size:.72rem;color:#6b6b8a;margin-top:4px;">Show this code at the desk</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

            col_ci, col_dr = st.columns(2)
            with col_ci:
                # CHECK IN — only if registered and NOT yet checked in
                if not st.session_state.checked_in:
                    if st.button("✅ I'm Here — Check In Now", use_container_width=True, key="home_ci"):
                        if checkin_user(st.session_state.user_code):
                            st.session_state.checked_in = True
                            st.success("Checked in! 🎉 Head to the desk.")
                            st.rerun()
                else:
                    st.success("You're checked in ✅")

            with col_dr:
                # LEAVE QUEUE — BLOCKED once checked in (session state prevents it)
                if st.session_state.checked_in:
                    st.markdown("""
                    <div style="padding:10px 16px;background:#ff4d6d0d;border:1px solid #ff4d6d33;
                                border-radius:8px;font-size:.85rem;color:#ff4d6d;">
                      ⛔ Cannot leave queue after check-in.<br>Speak with staff if needed.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button("❌ Leave Queue", use_container_width=True, key="home_dr"):
                        deregister_user(st.session_state.user_code)
                        st.session_state.registered_bank = None
                        st.session_state.user_code       = None
                        st.session_state.checked_in      = False
                        st.warning("You've left the queue. Slot released.")
                        st.rerun()

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.markdown("### 🏪 Available Food Banks")

        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            items = df[df["bank_name"] == bank]
            cats  = " · ".join(items["item_name"].tolist()[:5])

            with st.expander(f"🏪  {bank}   ·   {badge}   ({left} slots left)"):
                st.markdown(f"**Available:** {cats}")
                st.markdown(f"""
                <div style="font-size:.75rem;color:#6b6b8a;margin-bottom:4px;">{left} of {cap} slots remaining</div>
                <div class="slots-bar-wrap">
                  <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")

                can_reg = not st.session_state.registered_bank and left > 0
                if can_reg:
                    if st.button(f"📋 Register at {bank}", key=f"home_reg_{bank}"):
                        st.session_state.show_reg_form   = True
                        st.session_state.reg_target_bank = bank
                        st.session_state.page            = "✅ My Check-In"
                        st.rerun()
                elif st.session_state.registered_bank == bank:
                    st.info("✅ You're registered here.")
                elif st.session_state.registered_bank:
                    st.warning("Leave your current queue first.")
                elif left == 0:
                    st.error("No slots left today.")

    # ── Host home ──
    else:
        st.markdown("""
        <div class="lc-hero">
          <div class="lc-hero-tag">🔑 Host Dashboard</div>
          <h1>Operations <span class="accent">Overview</span></h1>
          <p>Live stats across all California food banks. Use the sidebar to manage check-ins and inventory.</p>
        </div>
        """, unsafe_allow_html=True)

        regs     = load_registrations()
        t        = today()
        t_regs   = [v for v in regs.values() if v.get("date") == t]
        total_r  = len([v for v in t_regs if v["status"] in ("registered","checked_in")])
        total_ci = len([v for v in t_regs if v["status"] == "checked_in"])
        total_sv = len([v for v in t_regs if v["status"] == "served"])
        total_cx = len([v for v in t_regs if v["status"] == "cancelled"])
        expiring = len(df[df["days_left"] <= 7])

        cols = st.columns(5)
        for col, icon, lbl, val, sub in [
            (cols[0],"📋","Registered",total_r,"active today"),
            (cols[1],"✅","Checked In",total_ci,"arrived"),
            (cols[2],"🤝","Served",total_sv,"completed"),
            (cols[3],"❌","Cancelled",total_cx,"left queue"),
            (cols[4],"⚠️","Expiring",expiring,"items ≤ 7 days"),
        ]:
            col.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">{icon}</div>
              <div class="lc-metric-label">{lbl}</div>
              <div class="lc-metric-val">{val}</div>
              <div class="lc-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.markdown("### 🏪 Per-Bank Snapshot")
        cols2 = st.columns(2)
        for i, bank in enumerate(BANKS):
            b_regs = [v for v in t_regs if v.get("bank") == bank]
            b_r    = len([v for v in b_regs if v["status"] == "registered"])
            b_ci   = len([v for v in b_regs if v["status"] == "checked_in"])
            b_sv   = len([v for v in b_regs if v["status"] == "served"])
            left, cap, pct, color, badge = slots_bar_html(bank)
            with cols2[i % 2]:
                st.markdown(f"""
                <div class="lc-card">
                  <div style="font-family:'Syne',sans-serif;font-weight:700;">{bank}</div>
                  <div style="display:flex;gap:16px;margin:8px 0;font-size:.82rem;flex-wrap:wrap;">
                    <span><b style="color:#818cf8">{b_r}</b> registered</span>
                    <span><b style="color:#00d4aa">{b_ci}</b> here now</span>
                    <span><b style="color:#f5a623">{b_sv}</b> served</span>
                  </div>
                  <div style="font-size:.75rem;color:#6b6b8a;">{left} of {cap} slots left · {badge}</div>
                  <div class="slots-bar-wrap">
                    <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MAP PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🗺 Map":

    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">🗺 Food Banks Near You</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">All California partner locations with live slot availability</div>
    </div>
    """, unsafe_allow_html=True)

    map_rows = []
    for bank in BANKS:
        lat, lon = BANK_COORDS[bank]
        left, cap, pct, color, badge = slots_bar_html(bank)
        items    = df[df["bank_name"] == bank]
        top_i    = ", ".join(items["item_name"].tolist()[:3])
        min_days = int(items["days_left"].min())
        map_rows.append(dict(
            Bank=bank, Lat=lat, Lon=lon,
            Left=left, Cap=cap, Status=badge.split()[1],
            Color=color, Items=top_i, MinDays=min_days,
        ))
    map_df = pd.DataFrame(map_rows)

    bg    = "#0a0a0f" if st.session_state.dark_mode else "#f4f6fb"
    land  = "#1a1a26" if st.session_state.dark_mode else "#e0e8f0"
    ocean = "#111118" if st.session_state.dark_mode else "#c8d8ee"

    fig_map = go.Figure()
    for _, r in map_df.iterrows():
        size = max(14, r["Left"] // 3 + 12)
        fig_map.add_trace(go.Scattergeo(
            lat=[r["Lat"]], lon=[r["Lon"]],
            mode="markers+text",
            marker=dict(size=size, color=r["Color"],
                        line=dict(width=2, color="rgba(255,255,255,0.13)"), opacity=0.88),
            text=r["Bank"].split()[0],
            textposition="top center",
            textfont=dict(color="#e8e8f0", size=10),
            hovertemplate=(
                f"<b>{r['Bank']}</b><br>"
                f"Status: {r['Status']}<br>"
                f"Slots: {r['Left']} / {r['Cap']}<br>"
                f"Top items: {r['Items']}<br>"
                f"Earliest expiry: {r['MinDays']} days<br>"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    fig_map.update_layout(
        geo=dict(
            scope="usa", showland=True, landcolor=land,
            showocean=True, oceancolor=ocean,
            showlakes=True, lakecolor=ocean,
            showcountries=True, countrycolor="#2a2a3a",
            showsubunits=True, subunitcolor="#2a2a3a",
            center=dict(lat=37.2, lon=-119.5), projection_scale=4.8,
        ),
        paper_bgcolor=bg, margin=dict(l=0,r=0,t=0,b=0), height=460,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("### 📍 All Locations")
    cols = st.columns(2)
    for i, bank in enumerate(BANKS):
        left, cap, pct, color, badge = slots_bar_html(bank)
        items    = df[df["bank_name"] == bank]
        min_days = int(items["days_left"].min())
        avail    = avail_label(min_days)
        with cols[i % 2]:
            st.markdown(f"""
            <div class="lc-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-family:'Syne',sans-serif;font-weight:700;">{bank}</div>
                  <div style="font-size:.78rem;color:#6b6b8a;margin-top:3px;">{avail}</div>
                </div>
                <span style="color:{color};font-weight:700;font-size:.85rem;">{badge}</span>
              </div>
              <div style="font-size:.75rem;color:#6b6b8a;margin-top:8px;">{left} of {cap} slots left today</div>
              <div class="slots-bar-wrap">
                <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# FOOD BANKS PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🏪 Food Banks":

    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">🏪 Food Banks</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">Browse all partner food banks and their available inventory</div>
    </div>
    """, unsafe_allow_html=True)

    for bank in BANKS:
        left, cap, pct, color, badge = slots_bar_html(bank)
        items = df[df["bank_name"] == bank].copy()
        n_ok  = len(items[items["supply_status"]=="OK"])
        n_low = len(items[items["supply_status"]=="Low"])

        with st.expander(f"🏪  {bank}   ·   {badge}   ·   {left} slots left"):
            col_l, col_r = st.columns([2,1])
            with col_l:
                st.markdown(f"""
                <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
                  <span class="pill pill-ok">{n_ok} stocked</span>
                  <span class="pill pill-low">{n_low} limited</span>
                  <span class="pill pill-ci">{left} slots open</span>
                </div>
                """, unsafe_allow_html=True)
            with col_r:
                st.markdown(f"""
                <div style="font-size:.72rem;color:#6b6b8a;">Slots used today</div>
                <div class="slots-bar-wrap">
                  <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
                </div>
                <div style="font-size:.7rem;color:#6b6b8a;margin-top:3px;">{cap-left}/{cap} taken</div>
                """, unsafe_allow_html=True)

            # Inventory table (no scary numbers for users)
            if st.session_state.role == "host":
                disp = items[["item_name","quantity","days_left","avg_daily_demand","supply_status"]].copy()
                disp.columns = ["Item","Qty","Days Left","Daily Demand","Status"]
                st.dataframe(disp, use_container_width=True, hide_index=True)
            else:
                for _, row in items.iterrows():
                    s    = row["supply_status"].lower()
                    pcls = "pill-ok" if "ok" in s else "pill-low" if "low" in s else "pill-crit"
                    av   = avail_label(row["days_left"])
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:9px 0;border-bottom:1px solid #2a2a3a;">
                      <span style="font-weight:500;">{row['item_name']}</span>
                      <span>
                        <span class="pill {pcls}" style="margin-right:8px;">{row['supply_status']}</span>
                        <span style="font-size:.75rem;color:#6b6b8a;">{av}</span>
                      </span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("")
            # Register button
            st.markdown("")
            reg_button(bank, f"fb_{bank}")

# ═════════════════════════════════════════════════════════════════════════════
# FIND ITEMS / INVENTORY
# ═════════════════════════════════════════════════════════════════════════════
elif page in ("📦 Find Items", "📦 Inventory"):

    is_host = st.session_state.role == "host"
    title   = "📦 Inventory Explorer" if is_host else "📦 What Can I Find?"
    subtitle= "Full inventory across all food banks." if is_host else "Search for any item and see which food banks have it today."

    st.markdown(f"""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">{title}</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,2,1])
    with c1:
        item_q  = st.text_input("🔍 Search item", placeholder="e.g. Rice, Baby Formula…")
    with c2:
        bank_f  = st.selectbox("Filter by Food Bank", ["All"] + BANKS)
    with c3:
        stat_f  = st.selectbox("Status", ["All","OK","Low","Critical"])

    filt = df.copy()
    if item_q:  filt = filt[filt["item_name"].str.contains(item_q, case=False)]
    if bank_f != "All": filt = filt[filt["bank_name"] == bank_f]
    if stat_f != "All": filt = filt[filt["supply_status"] == stat_f]

    st.markdown(f"**{len(filt)} result(s)**")

    if filt.empty:
        st.warning("No items match your search.")
    elif is_host:
        disp = filt[["bank_name","item_name","quantity","days_left","avg_daily_demand","supply_status"]].copy()
        disp.columns = ["Food Bank","Item","Qty","Days Left","Daily Demand","Status"]
        st.dataframe(disp, use_container_width=True, hide_index=True,
            column_config={
                "Qty":         st.column_config.NumberColumn(format="%d"),
                "Days Left":   st.column_config.NumberColumn(format="%d days"),
                "Daily Demand":st.column_config.NumberColumn(format="%d/day"),
            })
    else:
        for _, row in filt.iterrows():
            s    = row["supply_status"].lower()
            pcls = "pill-ok" if "ok" in s else "pill-low" if "low" in s else "pill-crit"
            av   = avail_label(row["days_left"])
            left, _, _, slot_color, _ = slots_bar_html(row["bank_name"])
            st.markdown(f"""
            <div class="lc-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                <div>
                  <div style="font-weight:700;font-size:1rem;">{row['item_name']}</div>
                  <div style="font-size:.82rem;color:#6b6b8a;margin-top:3px;">📍 {row['bank_name']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {pcls}">{row['supply_status']}</span>
                  <div style="font-size:.74rem;color:#6b6b8a;margin-top:4px;">{av}</div>
                </div>
              </div>
              <div style="font-size:.77rem;color:{slot_color};margin-top:8px;">🎟️ {left} slots left at this bank today</div>
            </div>
            """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MY CHECK-IN PAGE (Users only)
# ═════════════════════════════════════════════════════════════════════════════
elif page == "✅ My Check-In":

    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">✅ My Check-In</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">Register, manage your visit, and check in when you arrive</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 1: Show registration form if triggered ───────────────────────────
    if st.session_state.show_reg_form and not st.session_state.registered_bank:
        target_bank = st.session_state.reg_target_bank

        if st.button("← Back to bank list", key="reg_form_back"):
            st.session_state.show_reg_form   = False
            st.session_state.reg_target_bank = None
            st.rerun()

        submitted, profile = render_registration_form(target_bank)

        if submitted and profile:
            code, fam_size = register_user(target_bank, profile)
            st.session_state.registered_bank = target_bank
            st.session_state.user_code       = code
            st.session_state.family_size     = fam_size
            st.session_state.user_name       = profile["first_name"]
            st.session_state.checked_in      = False
            st.session_state.show_reg_form   = False
            st.session_state.reg_target_bank = None
            st.rerun()

    # ── STEP 2: Not yet registered — show bank picker ─────────────────────────
    elif not st.session_state.registered_bank:
        st.info("You haven't registered at any food bank yet. Choose a location below.")
        st.markdown("### 🏪 Choose a Food Bank")

        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            with st.expander(f"🏪  {bank}   ·   {badge}   ·   {left} slots left"):
                items = df[df["bank_name"] == bank]
                cats  = " · ".join(items["item_name"].tolist()[:5])
                st.markdown(f"**Available:** {cats}")
                st.markdown(f"""
                <div style="font-size:.75rem;color:#6b6b8a;margin-top:6px;">{left} of {cap} slots remaining</div>
                <div class="slots-bar-wrap">
                  <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
                if left > 0:
                    if st.button(f"📋 Register at {bank}", key=f"ci_p_reg_{bank}",
                                 use_container_width=True):
                        st.session_state.show_reg_form   = True
                        st.session_state.reg_target_bank = bank
                        st.rerun()
                else:
                    st.error("No slots available today.")

    # ── STEP 3: Already registered — show status + actions ────────────────────
    else:
        bank = st.session_state.registered_bank
        code = st.session_state.user_code
        fam  = st.session_state.family_size

        # Load stored profile for display
        regs    = load_registrations()
        profile = regs.get(code, {})
        full_name = " ".join(filter(None, [
            profile.get("first_name",""),
            profile.get("middle_name",""),
            profile.get("last_name",""),
        ])) or "—"

        st.markdown(f"""
        <div class="lc-card">
          <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;margin-bottom:4px;">
            Your Registration
          </div>
          <div style="color:#6b6b8a;font-size:.85rem;margin-bottom:20px;">
            Show your confirmation code at the desk when you arrive.
          </div>
          <div style="display:flex;gap:36px;flex-wrap:wrap;align-items:flex-start;">
            <div>
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6b6b8a;">Name</div>
              <div style="font-weight:700;margin-top:3px;">{full_name}</div>
            </div>
            <div>
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6b6b8a;">Food Bank</div>
              <div style="font-weight:700;margin-top:3px;">{bank}</div>
            </div>
            <div>
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6b6b8a;">Confirmation Code</div>
              <div class="code-box">{code}</div>
            </div>
            <div>
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6b6b8a;">Household</div>
              <div style="font-weight:700;margin-top:3px;">{fam} people</div>
            </div>
            <div>
              <div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:#6b6b8a;">Status</div>
              <div style="font-weight:700;margin-top:3px;color:#00d4aa;">
                {'✅ Checked In — You\'re here!' if st.session_state.checked_in else '📋 Registered — Not yet arrived'}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Your Actions")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Check In**")
            st.markdown(
                "<small style='color:#6b6b8a;'>Press this when you physically arrive at the food bank.</small>",
                unsafe_allow_html=True,
            )
            st.markdown("")
            if not st.session_state.checked_in:
                if st.button("✅ I've Arrived — Check Me In",
                             use_container_width=True, key="ci_page_ci"):
                    if checkin_user(code):
                        st.session_state.checked_in = True
                        st.success("You're checked in! 🎉 Head to the desk with your code.")
                        st.rerun()
            else:
                st.success("✅ You're checked in. Please visit the desk.")

        with col2:
            st.markdown("**❌ Leave Queue**")
            st.markdown(
                "<small style='color:#6b6b8a;'>Changed plans? This frees your slot for someone else.</small>",
                unsafe_allow_html=True,
            )
            st.markdown("")
            # SESSION STATE LOCK — once checked_in is True this button is permanently hidden
            if st.session_state.checked_in:
                st.markdown("""
                <div style="padding:12px 16px;background:#ff4d6d0d;
                            border:1px solid #ff4d6d33;border-radius:8px;
                            font-size:.85rem;color:#ff4d6d;">
                  ⛔ You are already checked in.<br>
                  You cannot leave the queue at this stage.<br>
                  Please speak with staff if you need to leave.
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button("❌ Leave Queue / Cancel Visit",
                             use_container_width=True, key="ci_page_dr"):
                    deregister_user(code)
                    st.session_state.registered_bank = None
                    st.session_state.user_code       = None
                    st.session_state.checked_in      = False
                    st.warning("You've left the queue. Your slot has been released.")
                    st.rerun()

        # ── Profile summary ───────────────────────────────────────────────────
        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.markdown("### 📋 Your Submitted Profile")

        field_map = [
            ("Consent",        profile.get("consent","—")),
            ("Birth Year",     profile.get("birth_year","—")),
            ("Client ID",      profile.get("client_id") or "New client"),
            ("Phone",          profile.get("phone","—")),
            ("Can Text",       profile.get("can_text","—")),
            ("Address",        profile.get("address","—")),
            ("City",           profile.get("city","—")),
            ("Zip Code",       profile.get("zip_code","—")),
            ("Children 0–18",  profile.get("children","—")),
            ("Adults 19–59",   profile.get("adults","—")),
            ("Seniors 60+",    profile.get("seniors","—")),
            ("Race/Ethnicity", profile.get("race_ethnicity","—")),
        ]
        col_a, col_b = st.columns(2)
        for i, (label, val) in enumerate(field_map):
            with (col_a if i % 2 == 0 else col_b):
                st.markdown(f"""
                <div style="padding:9px 0;border-bottom:1px solid #2a2a3a;">
                  <span style="font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;
                               color:#6b6b8a;">{label}</span><br>
                  <span style="font-weight:600;">{val}</span>
                </div>
                """, unsafe_allow_html=True)

        # ── What's available at their bank ────────────────────────────────────
        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.markdown(f"### 📦 What's at {bank} Today")
        bank_items = df[df["bank_name"] == bank]
        for _, row in bank_items.iterrows():
            s    = row["supply_status"].lower()
            pcls = "pill-ok" if "ok" in s else "pill-low" if "low" in s else "pill-crit"
            av   = avail_label(row["days_left"])
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:10px 0;border-bottom:1px solid #2a2a3a;">
              <span style="font-weight:500;">{row['item_name']}</span>
              <span>
                <span class="pill {pcls}" style="margin-right:8px;">{row['supply_status']}</span>
                <span style="font-size:.75rem;color:#6b6b8a;">{av}</span>
              </span>
            </div>
            """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# HOST DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📊 Dashboard":

    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">📊 Dashboard</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">Live operations across all food banks</div>
    </div>
    """, unsafe_allow_html=True)

    regs   = load_registrations()
    t      = today()
    t_regs = [v for v in regs.values() if v.get("date") == t]

    total_r  = len([v for v in t_regs if v["status"] in ("registered","checked_in")])
    total_ci = len([v for v in t_regs if v["status"] == "checked_in"])
    total_sv = len([v for v in t_regs if v["status"] == "served"])
    total_cx = len([v for v in t_regs if v["status"] == "cancelled"])
    ppl_sv   = sum(v.get("family_size",1) for v in t_regs if v["status"] == "served")
    expiring = len(df[df["days_left"] <= 7])

    cols = st.columns(6)
    for col, icon, lbl, val, sub in [
        (cols[0],"📋","Registered",total_r,"active"),
        (cols[1],"✅","Checked In",total_ci,"arrived"),
        (cols[2],"🤝","Served",total_sv,"done"),
        (cols[3],"👥","People",ppl_sv,"individuals"),
        (cols[4],"❌","Cancelled",total_cx,"left queue"),
        (cols[5],"⚠️","Expiring",expiring,"≤7 days"),
    ]:
        col.markdown(f"""<div class="lc-metric-card">
          <div class="lc-metric-icon">{icon}</div>
          <div class="lc-metric-label">{lbl}</div>
          <div class="lc-metric-val">{val}</div>
          <div class="lc-metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
    st.markdown("### 🏪 Per-Bank Snapshot")
    cols2 = st.columns(2)
    for i, bank in enumerate(BANKS):
        b_r  = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="registered"])
        b_ci = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="checked_in"])
        b_sv = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="served"])
        left, cap, pct, color, badge = slots_bar_html(bank)
        with cols2[i % 2]:
            st.markdown(f"""
            <div class="lc-card">
              <div style="font-family:'Syne',sans-serif;font-weight:700;">{bank}</div>
              <div style="display:flex;gap:16px;margin:8px 0;font-size:.82rem;">
                <span><b style="color:#818cf8">{b_r}</b> registered</span>
                <span><b style="color:#00d4aa">{b_ci}</b> here</span>
                <span><b style="color:#f5a623">{b_sv}</b> served</span>
              </div>
              <div style="font-size:.74rem;color:#6b6b8a;">{left}/{cap} slots left · {badge}</div>
              <div class="slots-bar-wrap">
                <div class="slots-bar" style="width:{pct}%;background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
    st.markdown("### 📈 Analytics")

    bg_c = "#0a0a0f" if st.session_state.dark_mode else "#ffffff"
    fc   = "#e8e8f0" if st.session_state.dark_mode else "#0c1228"

    ca, cb = st.columns(2)
    with ca:
        grp = df.groupby("bank_name").agg(
            Supply=("quantity","sum"),
            Demand=("avg_daily_demand", lambda x: x.sum()*7),
        ).reset_index()
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name="Supply",x=grp["bank_name"],y=grp["Supply"],marker_color="#00d4aa"))
        fig1.add_trace(go.Bar(name="Weekly Demand",x=grp["bank_name"],y=grp["Demand"],marker_color="#f5a623"))
        fig1.update_layout(barmode="group",title="Supply vs Weekly Demand",
            plot_bgcolor=bg_c,paper_bgcolor=bg_c,
            font=dict(family="Manrope",color=fc),
            legend=dict(orientation="h",y=-0.3),
            margin=dict(t=40,b=90,l=40,r=10),
            xaxis=dict(tickangle=-30))
        st.plotly_chart(fig1, use_container_width=True)

    with cb:
        sc   = df["supply_status"].value_counts().reset_index()
        sc.columns = ["Status","Count"]
        fig2 = px.pie(sc,names="Status",values="Count",hole=0.5,
            color="Status",color_discrete_map={"OK":"#00d4aa","Low":"#f5a623","Critical":"#ff4d6d"},
            title="Inventory Status")
        fig2.update_layout(paper_bgcolor=bg_c,font=dict(family="Manrope",color=fc))
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df,x="days_left",nbins=15,title="Days Until Expiry",
        color_discrete_sequence=["#00d4aa"],labels={"days_left":"Days Left"})
    fig3.update_layout(plot_bgcolor=bg_c,paper_bgcolor=bg_c,bargap=0.08,
        font=dict(family="Manrope",color=fc))
    st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# HOST MANAGE PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Manage":

    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;">⚙️ Manage</div>
      <div style="color:#6b6b8a;font-size:.9rem;margin-top:4px;">Check in visitors, mark served, adjust capacity</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👥 Live Queue", "🎟 Capacity", "📋 Full Log"])

    with tab1:
        st.markdown("#### Mark visitors as served")
        sel_bank = st.selectbox("Food Bank", BANKS, key="mgmt_bank")
        regs     = load_registrations()
        t        = today()
        active   = {k: v for k, v in regs.items()
                    if v.get("bank") == sel_bank and v.get("date") == t
                    and v["status"] in ("registered","checked_in")}

        if not active:
            st.info(f"No active registrations at {sel_bank} today.")
        else:
            for code, info in active.items():
                status = info["status"]
                pcls   = "pill-ci" if status == "checked_in" else "pill-reg"
                slbl   = "✅ Checked In" if status == "checked_in" else "📋 Registered"
                ctime  = info.get("checked_in_at","")
                rtime  = info.get("registered_at","")

                col_i, col_a = st.columns([3,1])
                with col_i:
                    st.markdown(f"""
                    <div style="padding:12px 0;border-bottom:1px solid #2a2a3a;">
                      <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
                        <code style="font-family:'Geist Mono',monospace;color:#00d4aa;font-size:.95rem;">{code}</code>
                        <span class="pill {pcls}">{slbl}</span>
                        <span style="font-size:.8rem;color:#6b6b8a;">
                          {info.get('name','Anon')} · {info.get('family_size',1)} people
                          · Registered {rtime}
                          {' · Arrived ' + ctime if ctime else ''}
                        </span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_a:
                    if st.button("✅ Served", key=f"srv_{code}", use_container_width=True):
                        mark_served(code)
                        st.success(f"{code} marked served.")
                        st.rerun()

    with tab2:
        st.markdown("#### Daily Capacity Per Food Bank")
        st.markdown("<small style='color:#6b6b8a;'>Max families that can register per day.</small>", unsafe_allow_html=True)
        st.markdown("")
        cap_data = load_capacity()
        new_caps = {}
        cols = st.columns(2)
        for i, bank in enumerate(BANKS):
            with cols[i % 2]:
                new_caps[bank] = st.number_input(
                    bank, min_value=10, max_value=500,
                    value=cap_data.get(bank, 50), step=5, key=f"cap_{bank}"
                )
        if st.button("💾 Save Capacity", use_container_width=True):
            save_capacity(new_caps)
            st.success("Capacity updated!")

    with tab3:
        st.markdown("#### Today's Full Log")
        regs = load_registrations()
        t    = today()
        rows = []
        for code, v in regs.items():
            if v.get("date") == t:
                rows.append({
                    "Code":          code,
                    "First Name":    v.get("first_name","—"),
                    "Last Name":     v.get("last_name","—"),
                    "Client ID":     v.get("client_id") or "New",
                    "Bank":          v.get("bank","—"),
                    "Status":        v.get("status","—"),
                    "Household":     v.get("family_size",1),
                    "Children 0-18": v.get("children","—"),
                    "Adults 19-59":  v.get("adults","—"),
                    "Seniors 60+":   v.get("seniors","—"),
                    "Phone":         v.get("phone","—"),
                    "Can Text":      v.get("can_text","—"),
                    "City":          v.get("city","—"),
                    "Zip":           v.get("zip_code","—"),
                    "Race/Ethnicity":v.get("race_ethnicity","—"),
                    "Consent":       v.get("consent","—"),
                    "Registered":    v.get("registered_at","—"),
                    "Checked In":    v.get("checked_in_at","—"),
                    "Served":        v.get("served_at","—"),
                })
        if rows:
            log_df = pd.DataFrame(rows)
            st.dataframe(log_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Download CSV", log_df.to_csv(index=False),
                file_name=f"checkins_{t}.csv", mime="text/csv"
            )
        else:
            st.info("No registrations today yet.")
