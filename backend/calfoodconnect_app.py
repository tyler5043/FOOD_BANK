import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
import random
import string
import math
from datetime import datetime, date

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CalFoodConnect",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Storage ───────────────────────────────────────────────────────────────────
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

# ══════════════════════════════════════════════════════════════════════════════
# MULTILANGUAGE SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
TRANSLATIONS = {
    "English": {
        "app_name": "CalFoodConnect",
        "tagline": "California Food Network",
        "home": "🏠 Home",
        "map": "🗺 Map",
        "food_banks": "🏪 Food Banks",
        "find_items": "📦 Find Items",
        "my_checkin": "✅ My Check-In",
        "inventory": "📦 Inventory",
        "dashboard": "📊 Dashboard",
        "manage": "⚙️ Manage",
        "ai_insights": "🤖 AI Insights",
        "visitor": "👤 Visitor",
        "host": "🔑 Host",
        "sign_out": "🚪 Sign Out",
        "dark_mode": "🌙 Dark Mode",
        "language": "🌐 Language",
        "signed_in_as": "Signed in as",
        "find_food_today": "Find Food Near You. Today.",
        "hero_desc": "CalFoodConnect connects you to food banks across California in real time. See availability, secure a slot, and plan your visit — before you leave home.",
        "food_banks_label": "Food Banks",
        "open_today": "Open Today",
        "slots_available": "Slots Available",
        "across_california": "Across California",
        "with_slots": "With slots available",
        "register_to_secure": "Register to secure yours",
        "all_food_banks": "🏪 All Food Banks",
        "visitor_login": "Visitor Login",
        "host_login": "Host / Admin Login",
        "visitor_desc": "Find food banks near you, register for a slot, and manage your visit.",
        "host_desc": "Manage inventory, approve check-ins, and view live operations.",
        "your_name": "Your name (optional)",
        "enter_name": "Enter your name",
        "host_password": "Host password",
        "password": "Password",
        "continue_btn": "Continue →",
        "back": "← Back",
        "wrong_password": "Wrong password. Hint: host123",
        "slots_left": "slots left",
        "register_at": "📋 Register at",
        "you_are_registered": "✅ You are registered here.",
        "leave_queue_first": "Leave your current queue first to register here.",
        "no_slots": "No slots available today.",
        "log_in_visitor": "Log in as a Visitor to register.",
        "checked_in": "✅ Checked In",
        "registered": "📋 Registered",
        "operations_overview": "Operations Overview",
        "host_hero_desc": "Live stats across all California food banks. Use the sidebar to manage check-ins and inventory.",
        "registered_label": "Registered",
        "active_today": "active today",
        "arrived": "arrived",
        "completed": "completed",
        "left_queue": "left queue",
        "expiring": "⚠️ Expiring",
        "items_7_days": "items ≤ 7 days",
        "per_bank_snapshot": "🏪 Per-Bank Snapshot",
        "hello": "Hello",
        "user_hero_desc": "Find a food bank near you, register for a slot, and check in when you arrive.",
        "im_here": "✅ I'm Here — Check In Now",
        "checked_in_success": "Checked in! 🎉 Head to the desk.",
        "youre_checked_in": "You're checked in ✅",
        "leave_queue": "❌ Leave Queue",
        "cannot_leave": "⛔ Cannot leave queue after check-in. Speak with staff if needed.",
        "left_queue_msg": "You've left the queue. Slot released.",
        "available_banks": "🏪 Available Food Banks",
        "available": "Available",
        "of": "of",
        "slots_remaining": "slots remaining",
        "no_slots_left": "No slots left today.",
        "search_item": "🔍 Search item",
        "search_placeholder": "e.g. Rice, Baby Formula…",
        "filter_bank": "Filter by Food Bank",
        "all": "All",
        "status": "Status",
        "results": "result(s)",
        "no_items": "No items match your search.",
        "not_registered": "You haven't registered at any food bank yet. Choose a location below.",
        "choose_bank": "🏪 Choose a Food Bank",
        "your_registration": "Your Registration",
        "show_code": "Show your confirmation code at the desk when you arrive.",
        "name": "Name",
        "food_bank": "Food Bank",
        "confirmation_code": "Confirmation Code",
        "household": "Household",
        "people": "people",
        "your_status": "Status",
        "checked_in_here": "✅ Checked In — You're here!",
        "not_arrived": "📋 Registered — Not yet arrived",
        "your_actions": "Your Actions",
        "check_in": "✅ Check In",
        "press_arrive": "Press this when you physically arrive at the food bank.",
        "ive_arrived": "✅ I've Arrived — Check Me In",
        "youre_checked_in_desk": "✅ You're checked in. Please visit the desk.",
        "leave_queue_label": "❌ Leave Queue",
        "changed_plans": "Changed plans? This frees your slot for someone else.",
        "already_checked_in": "⛔ You are already checked in. You cannot leave the queue at this stage. Please speak with staff if you need to leave.",
        "leave_cancel": "❌ Leave Queue / Cancel Visit",
        "slot_released": "You've left the queue. Your slot has been released.",
        "your_profile": "📋 Your Submitted Profile",
        "whats_at": "📦 What's at",
        "today": "Today",
        "consent": "Consent",
        "birth_year": "Birth Year",
        "client_id": "Client ID",
        "phone": "Phone",
        "can_text": "Can Text",
        "address": "Address",
        "city": "City",
        "zip_code": "Zip Code",
        "children_018": "Children 0–18",
        "adults_1959": "Adults 19–59",
        "seniors_60": "Seniors 60+",
        "race_ethnicity": "Race/Ethnicity",
        "new_client": "New client",
        "live_ops": "Live operations across all food banks",
        "done": "done",
        "individuals": "individuals",
        "le7days": "≤7 days",
        "analytics": "📈 Analytics",
        "supply_weekly": "Supply vs Weekly Demand",
        "inventory_status": "Inventory Status",
        "days_expiry": "Days Until Expiry",
        "manage_desc": "Check in visitors, mark served, adjust capacity",
        "live_queue": "👥 Live Queue",
        "capacity": "🎟 Capacity",
        "full_log": "📋 Full Log",
        "mark_served_label": "Mark visitors as served",
        "no_active_regs": "No active registrations at",
        "served_btn": "✅ Served",
        "marked_served": "marked served.",
        "daily_capacity": "Daily Capacity Per Food Bank",
        "max_families": "Max families that can register per day.",
        "save_capacity": "💾 Save Capacity",
        "capacity_updated": "Capacity updated!",
        "todays_log": "Today's Full Log",
        "download_csv": "⬇️ Download CSV",
        "no_regs_today": "No registrations today yet.",
        "ai_insights_title": "🤖 AI Insights & Predictions",
        "ai_insights_desc": "Machine learning–powered analysis of your food bank network",
        "expiry_risk": "🔴 Expiration Risk Prediction",
        "redistribution": "🔄 AI Redistribution Recommendations",
        "demand_forecast": "📈 Demand Forecast Simulation",
        "ai_dashboard": "🧠 AI Insights Dashboard",
        "critical_risk": "Critical Risk",
        "high_risk": "High Risk",
        "moderate_risk": "Moderate Risk",
        "days_remaining": "days remaining",
        "redistribute_to": "Redistribute to",
        "surplus_at": "Surplus at",
        "shortage_at": "Shortage at",
        "units": "units",
        "forecast_7": "7-Day Demand Forecast",
        "forecast_30": "30-Day Demand Forecast",
        "network_health": "Network Health Score",
        "waste_risk": "Waste Risk Index",
        "coverage_rate": "Coverage Rate",
        "efficiency": "Distribution Efficiency",
        "registration_form": "📋 Client Registration — Second Harvest",
        "register_at_label": "Register at",
        "confidential": "Please complete all required fields. This information is kept confidential and used only by Second Harvest food network staff.",
        "section_consent": "1 · Consent",
        "consent_question": "Do you consent to have your data stored by Second Harvest?",
        "section_identity": "2 · Identity",
        "birth_year_label": "Birth Year",
        "client_id_label": "Client ID",
        "client_id_placeholder": "Leave blank if new client",
        "first_name": "First Name",
        "middle_name": "Middle Name",
        "optional": "Optional",
        "last_name": "Last Name",
        "section_contact": "3 · Contact",
        "phone_label": "Phone Number",
        "phone_placeholder": "(555) 000-0000",
        "can_text_question": "Can we text you?",
        "street_address": "Street Address",
        "address_placeholder": "123 Main St",
        "city_label": "City",
        "zip_label": "Zip Code",
        "section_household": "4 · Household Composition",
        "household_note": "These counts are used to prepare the right amount of food for your family.",
        "children_label": "Children (0–18 yrs)",
        "adults_label": "Adults (19–59 yrs)",
        "seniors_label": "Seniors (60+ yrs)",
        "total_household": "👥 Total household size:",
        "section_race": "5 · Race & Ethnicity",
        "race_note": "Select the option that best describes your household. This information is collected for reporting purposes only.",
        "race_label": "Race / Ethnicity of Household",
        "submit_btn": "✅ Submit & Secure My Slot",
        "consent_required": "You must consent to data storage to register.",
        "first_name_required": "First name is required.",
        "last_name_required": "Last name is required.",
        "phone_required": "Phone number is required.",
        "address_required": "Street address is required.",
        "city_required": "City is required.",
        "zip_required": "Zip code is required.",
        "household_required": "Household must have at least 1 member.",
        "back_to_list": "← Back to bank list",
        "running_out_soon": "⚠️ Running out very soon",
        "limited_visit": "🟡 Limited — visit soon",
        "well_stocked": "🟢 Well stocked",
        "open_badge": "🟢 Open",
        "filling_up": "🟡 Filling up",
        "full_badge": "🔴 Full",
        "here_now": "here now",
        "slots_left_label": "slots left",
        "taken": "taken",
        "stocked": "stocked",
        "limited": "limited",
        "slots_open": "slots open",
        "slots_used_today": "Slots used today",
        "visitor_click": "👤 Click **Visitor** in the sidebar to register at a food bank.",
        "people_served": "People",
        "cancelled": "Cancelled",
    },
    "Español": {
        "app_name": "CalFoodConnect",
        "tagline": "Red Alimentaria de California",
        "home": "🏠 Inicio",
        "map": "🗺 Mapa",
        "food_banks": "🏪 Bancos de Alimentos",
        "find_items": "📦 Buscar Artículos",
        "my_checkin": "✅ Mi Registro",
        "inventory": "📦 Inventario",
        "dashboard": "📊 Panel",
        "manage": "⚙️ Gestionar",
        "ai_insights": "🤖 IA Insights",
        "visitor": "👤 Visitante",
        "host": "🔑 Anfitrión",
        "sign_out": "🚪 Salir",
        "dark_mode": "🌙 Modo Oscuro",
        "language": "🌐 Idioma",
        "signed_in_as": "Conectado como",
        "find_food_today": "Encuentra Comida Cerca. Hoy.",
        "hero_desc": "CalFoodConnect te conecta con bancos de alimentos en California en tiempo real.",
        "food_banks_label": "Bancos de Alimentos",
        "open_today": "Abiertos Hoy",
        "slots_available": "Plazas Disponibles",
        "across_california": "En California",
        "with_slots": "Con plazas disponibles",
        "register_to_secure": "Regístrate para reservar la tuya",
        "all_food_banks": "🏪 Todos los Bancos de Alimentos",
        "visitor_login": "Inicio de Sesión Visitante",
        "host_login": "Inicio de Sesión Anfitrión",
        "visitor_desc": "Encuentra bancos de alimentos cerca, regístrate para una plaza y gestiona tu visita.",
        "host_desc": "Gestiona el inventario, aprueba registros y visualiza operaciones en vivo.",
        "your_name": "Tu nombre (opcional)",
        "enter_name": "Introduce tu nombre",
        "host_password": "Contraseña de anfitrión",
        "password": "Contraseña",
        "continue_btn": "Continuar →",
        "back": "← Atrás",
        "wrong_password": "Contraseña incorrecta. Pista: host123",
        "slots_left": "plazas restantes",
        "register_at": "📋 Registrarse en",
        "you_are_registered": "✅ Estás registrado aquí.",
        "leave_queue_first": "Abandona tu cola actual primero.",
        "no_slots": "No hay plazas disponibles hoy.",
        "log_in_visitor": "Inicia sesión como Visitante para registrarte.",
        "checked_in": "✅ Registrado",
        "registered": "📋 Inscrito",
        "operations_overview": "Resumen de Operaciones",
        "host_hero_desc": "Estadísticas en vivo de todos los bancos de alimentos de California.",
        "registered_label": "Inscrito",
        "active_today": "activos hoy",
        "arrived": "llegaron",
        "completed": "completados",
        "left_queue": "dejaron la cola",
        "expiring": "⚠️ Expirando",
        "items_7_days": "artículos ≤ 7 días",
        "per_bank_snapshot": "🏪 Resumen por Banco",
        "hello": "Hola",
        "user_hero_desc": "Encuentra un banco de alimentos, regístrate para una plaza y regístrate al llegar.",
        "im_here": "✅ Estoy Aquí — Registrarme Ahora",
        "checked_in_success": "¡Registrado! 🎉 Ve al mostrador.",
        "youre_checked_in": "Estás registrado ✅",
        "leave_queue": "❌ Abandonar Cola",
        "cannot_leave": "⛔ No puedes abandonar la cola después del registro. Habla con el personal si es necesario.",
        "left_queue_msg": "Has abandonado la cola. Plaza liberada.",
        "available_banks": "🏪 Bancos de Alimentos Disponibles",
        "available": "Disponible",
        "of": "de",
        "slots_remaining": "plazas restantes",
        "no_slots_left": "No quedan plazas hoy.",
        "search_item": "🔍 Buscar artículo",
        "search_placeholder": "ej. Arroz, Fórmula…",
        "filter_bank": "Filtrar por Banco",
        "all": "Todos",
        "status": "Estado",
        "results": "resultado(s)",
        "no_items": "No se encontraron artículos.",
        "not_registered": "Aún no te has registrado en ningún banco. Elige una ubicación abajo.",
        "choose_bank": "🏪 Elige un Banco de Alimentos",
        "your_registration": "Tu Inscripción",
        "show_code": "Muestra tu código de confirmación al llegar.",
        "name": "Nombre",
        "food_bank": "Banco de Alimentos",
        "confirmation_code": "Código de Confirmación",
        "household": "Hogar",
        "people": "personas",
        "your_status": "Estado",
        "checked_in_here": "✅ Registrado — ¡Estás aquí!",
        "not_arrived": "📋 Inscrito — Aún no has llegado",
        "your_actions": "Tus Acciones",
        "check_in": "✅ Registrarse",
        "press_arrive": "Presiona esto cuando llegues físicamente al banco de alimentos.",
        "ive_arrived": "✅ He Llegado — Regístrame",
        "youre_checked_in_desk": "✅ Estás registrado. Ve al mostrador.",
        "leave_queue_label": "❌ Abandonar Cola",
        "changed_plans": "¿Cambiaste de planes? Esto libera tu plaza para alguien más.",
        "already_checked_in": "⛔ Ya estás registrado. No puedes abandonar la cola en esta etapa.",
        "leave_cancel": "❌ Abandonar Cola / Cancelar Visita",
        "slot_released": "Has abandonado la cola. Tu plaza ha sido liberada.",
        "your_profile": "📋 Tu Perfil Enviado",
        "whats_at": "📦 Qué hay en",
        "today": "Hoy",
        "consent": "Consentimiento",
        "birth_year": "Año de Nacimiento",
        "client_id": "ID de Cliente",
        "phone": "Teléfono",
        "can_text": "Puede recibir SMS",
        "address": "Dirección",
        "city": "Ciudad",
        "zip_code": "Código Postal",
        "children_018": "Niños 0–18",
        "adults_1959": "Adultos 19–59",
        "seniors_60": "Mayores 60+",
        "race_ethnicity": "Raza/Etnicidad",
        "new_client": "Nuevo cliente",
        "live_ops": "Operaciones en vivo en todos los bancos",
        "done": "completados",
        "individuals": "individuos",
        "le7days": "≤7 días",
        "analytics": "📈 Análisis",
        "supply_weekly": "Oferta vs Demanda Semanal",
        "inventory_status": "Estado del Inventario",
        "days_expiry": "Días hasta Caducidad",
        "manage_desc": "Registra visitantes, marca servidos, ajusta capacidad",
        "live_queue": "👥 Cola en Vivo",
        "capacity": "🎟 Capacidad",
        "full_log": "📋 Registro Completo",
        "mark_served_label": "Marcar visitantes como servidos",
        "no_active_regs": "No hay inscripciones activas en",
        "served_btn": "✅ Servido",
        "marked_served": "marcado como servido.",
        "daily_capacity": "Capacidad Diaria por Banco",
        "max_families": "Máximo de familias que pueden inscribirse por día.",
        "save_capacity": "💾 Guardar Capacidad",
        "capacity_updated": "¡Capacidad actualizada!",
        "todays_log": "Registro de Hoy",
        "download_csv": "⬇️ Descargar CSV",
        "no_regs_today": "Aún no hay inscripciones hoy.",
        "ai_insights_title": "🤖 IA Insights y Predicciones",
        "ai_insights_desc": "Análisis de red impulsado por aprendizaje automático",
        "expiry_risk": "🔴 Predicción de Riesgo de Caducidad",
        "redistribution": "🔄 Recomendaciones de Redistribución IA",
        "demand_forecast": "📈 Simulación de Previsión de Demanda",
        "ai_dashboard": "🧠 Panel de IA Insights",
        "critical_risk": "Riesgo Crítico",
        "high_risk": "Riesgo Alto",
        "moderate_risk": "Riesgo Moderado",
        "days_remaining": "días restantes",
        "redistribute_to": "Redistribuir a",
        "surplus_at": "Excedente en",
        "shortage_at": "Escasez en",
        "units": "unidades",
        "forecast_7": "Previsión de Demanda 7 Días",
        "forecast_30": "Previsión de Demanda 30 Días",
        "network_health": "Puntuación de Salud de Red",
        "waste_risk": "Índice de Riesgo de Desperdicio",
        "coverage_rate": "Tasa de Cobertura",
        "efficiency": "Eficiencia de Distribución",
        "registration_form": "📋 Registro de Cliente — Second Harvest",
        "register_at_label": "Registrarse en",
        "confidential": "Por favor complete todos los campos requeridos. Esta información es confidencial.",
        "section_consent": "1 · Consentimiento",
        "consent_question": "¿Consiente que Second Harvest almacene sus datos?",
        "section_identity": "2 · Identidad",
        "birth_year_label": "Año de Nacimiento",
        "client_id_label": "ID de Cliente",
        "client_id_placeholder": "Dejar en blanco si es nuevo cliente",
        "first_name": "Nombre",
        "middle_name": "Segundo Nombre",
        "optional": "Opcional",
        "last_name": "Apellido",
        "section_contact": "3 · Contacto",
        "phone_label": "Número de Teléfono",
        "phone_placeholder": "(555) 000-0000",
        "can_text_question": "¿Podemos enviarle SMS?",
        "street_address": "Dirección",
        "address_placeholder": "123 Calle Principal",
        "city_label": "Ciudad",
        "zip_label": "Código Postal",
        "section_household": "4 · Composición del Hogar",
        "household_note": "Estos datos se usan para preparar la cantidad correcta de alimentos.",
        "children_label": "Niños (0–18 años)",
        "adults_label": "Adultos (19–59 años)",
        "seniors_label": "Mayores (60+ años)",
        "total_household": "👥 Tamaño total del hogar:",
        "section_race": "5 · Raza y Etnicidad",
        "race_note": "Seleccione la opción que mejor describa su hogar.",
        "race_label": "Raza / Etnicidad del Hogar",
        "submit_btn": "✅ Enviar y Asegurar Mi Plaza",
        "consent_required": "Debe dar su consentimiento para registrarse.",
        "first_name_required": "El nombre es obligatorio.",
        "last_name_required": "El apellido es obligatorio.",
        "phone_required": "El teléfono es obligatorio.",
        "address_required": "La dirección es obligatoria.",
        "city_required": "La ciudad es obligatoria.",
        "zip_required": "El código postal es obligatorio.",
        "household_required": "El hogar debe tener al menos 1 miembro.",
        "back_to_list": "← Volver a la lista",
        "running_out_soon": "⚠️ Se agota muy pronto",
        "limited_visit": "🟡 Limitado — visita pronto",
        "well_stocked": "🟢 Bien abastecido",
        "open_badge": "🟢 Abierto",
        "filling_up": "🟡 Llenándose",
        "full_badge": "🔴 Lleno",
        "here_now": "aquí ahora",
        "slots_left_label": "plazas restantes",
        "taken": "ocupadas",
        "stocked": "abastecido",
        "limited": "limitado",
        "slots_open": "plazas disponibles",
        "slots_used_today": "Plazas usadas hoy",
        "visitor_click": "👤 Haz clic en **Visitante** en la barra lateral para registrarte.",
        "people_served": "Personas",
        "cancelled": "Cancelados",
    },
    "中文": {
        "app_name": "CalFoodConnect",
        "tagline": "加州食品网络",
        "home": "🏠 主页",
        "map": "🗺 地图",
        "food_banks": "🏪 食物银行",
        "find_items": "📦 查找物品",
        "my_checkin": "✅ 我的签到",
        "inventory": "📦 库存",
        "dashboard": "📊 仪表板",
        "manage": "⚙️ 管理",
        "ai_insights": "🤖 AI洞察",
        "visitor": "👤 访客",
        "host": "🔑 主机",
        "sign_out": "🚪 登出",
        "dark_mode": "🌙 深色模式",
        "language": "🌐 语言",
        "signed_in_as": "已登录",
        "find_food_today": "就近找食物。今天。",
        "hero_desc": "CalFoodConnect实时连接您与加州食物银行。查看可用性，预留位置，提前规划。",
        "food_banks_label": "食物银行",
        "open_today": "今日开放",
        "slots_available": "可用名额",
        "across_california": "遍布加州",
        "with_slots": "有名额可用",
        "register_to_secure": "注册以预留您的名额",
        "all_food_banks": "🏪 所有食物银行",
        "visitor_login": "访客登录",
        "host_login": "主机/管理员登录",
        "visitor_desc": "找到附近的食物银行，注册名额，管理您的访问。",
        "host_desc": "管理库存，审批签到，查看实时运营情况。",
        "your_name": "您的姓名（可选）",
        "enter_name": "输入您的姓名",
        "host_password": "主机密码",
        "password": "密码",
        "continue_btn": "继续 →",
        "back": "← 返回",
        "wrong_password": "密码错误。提示：host123",
        "slots_left": "个名额剩余",
        "register_at": "📋 在此注册",
        "you_are_registered": "✅ 您已在此注册。",
        "leave_queue_first": "请先离开当前队列。",
        "no_slots": "今天没有可用名额。",
        "log_in_visitor": "请以访客身份登录注册。",
        "checked_in": "✅ 已签到",
        "registered": "📋 已注册",
        "operations_overview": "运营概览",
        "host_hero_desc": "加州所有食物银行的实时统计数据。",
        "registered_label": "已注册",
        "active_today": "今日活跃",
        "arrived": "已到达",
        "completed": "已完成",
        "left_queue": "已离队",
        "expiring": "⚠️ 即将过期",
        "items_7_days": "物品≤7天",
        "per_bank_snapshot": "🏪 各银行快照",
        "hello": "你好",
        "user_hero_desc": "找到附近的食物银行，注册名额，到达时签到。",
        "im_here": "✅ 我到了——立即签到",
        "checked_in_success": "签到成功！🎉 请前往服务台。",
        "youre_checked_in": "您已签到 ✅",
        "leave_queue": "❌ 离开队列",
        "cannot_leave": "⛔ 签到后无法离队。如需帮助请联系工作人员。",
        "left_queue_msg": "您已离队。名额已释放。",
        "available_banks": "🏪 可用食物银行",
        "available": "可用",
        "of": "/",
        "slots_remaining": "名额剩余",
        "no_slots_left": "今天没有名额了。",
        "search_item": "🔍 搜索物品",
        "search_placeholder": "例如：大米、婴儿配方奶粉…",
        "filter_bank": "按食物银行筛选",
        "all": "全部",
        "status": "状态",
        "results": "个结果",
        "no_items": "没有匹配的物品。",
        "not_registered": "您尚未在任何食物银行注册。请在下方选择位置。",
        "choose_bank": "🏪 选择食物银行",
        "your_registration": "您的注册",
        "show_code": "到达时请向服务台出示您的确认码。",
        "name": "姓名",
        "food_bank": "食物银行",
        "confirmation_code": "确认码",
        "household": "家庭",
        "people": "人",
        "your_status": "状态",
        "checked_in_here": "✅ 已签到——您在这里！",
        "not_arrived": "📋 已注册——尚未到达",
        "your_actions": "您的操作",
        "check_in": "✅ 签到",
        "press_arrive": "当您实际到达食物银行时按此按钮。",
        "ive_arrived": "✅ 我已到达——请为我签到",
        "youre_checked_in_desk": "✅ 您已签到。请前往服务台。",
        "leave_queue_label": "❌ 离开队列",
        "changed_plans": "改变计划了？这将释放您的名额给他人。",
        "already_checked_in": "⛔ 您已签到。此阶段无法离队。如需离开请联系工作人员。",
        "leave_cancel": "❌ 离队/取消访问",
        "slot_released": "您已离队。您的名额已释放。",
        "your_profile": "📋 您提交的资料",
        "whats_at": "📦 今日",
        "today": "的物品",
        "consent": "同意",
        "birth_year": "出生年份",
        "client_id": "客户ID",
        "phone": "电话",
        "can_text": "可发短信",
        "address": "地址",
        "city": "城市",
        "zip_code": "邮政编码",
        "children_018": "儿童 0–18",
        "adults_1959": "成人 19–59",
        "seniors_60": "老人 60+",
        "race_ethnicity": "种族/民族",
        "new_client": "新客户",
        "live_ops": "所有食物银行实时运营",
        "done": "已完成",
        "individuals": "人",
        "le7days": "≤7天",
        "analytics": "📈 分析",
        "supply_weekly": "供应vs周需求",
        "inventory_status": "库存状态",
        "days_expiry": "距过期天数",
        "manage_desc": "签到访客，标记已服务，调整容量",
        "live_queue": "👥 实时队列",
        "capacity": "🎟 容量",
        "full_log": "📋 完整日志",
        "mark_served_label": "标记访客为已服务",
        "no_active_regs": "没有活跃注册在",
        "served_btn": "✅ 已服务",
        "marked_served": "已标记为已服务。",
        "daily_capacity": "每家食物银行每日容量",
        "max_families": "每天可注册的最大家庭数。",
        "save_capacity": "💾 保存容量",
        "capacity_updated": "容量已更新！",
        "todays_log": "今日完整日志",
        "download_csv": "⬇️ 下载CSV",
        "no_regs_today": "今天还没有注册。",
        "ai_insights_title": "🤖 AI洞察与预测",
        "ai_insights_desc": "机器学习驱动的食物银行网络分析",
        "expiry_risk": "🔴 过期风险预测",
        "redistribution": "🔄 AI重新分配建议",
        "demand_forecast": "📈 需求预测模拟",
        "ai_dashboard": "🧠 AI洞察仪表板",
        "critical_risk": "严重风险",
        "high_risk": "高风险",
        "moderate_risk": "中等风险",
        "days_remaining": "天剩余",
        "redistribute_to": "重新分配到",
        "surplus_at": "盈余在",
        "shortage_at": "短缺在",
        "units": "单位",
        "forecast_7": "7天需求预测",
        "forecast_30": "30天需求预测",
        "network_health": "网络健康评分",
        "waste_risk": "浪费风险指数",
        "coverage_rate": "覆盖率",
        "efficiency": "分配效率",
        "registration_form": "📋 客户注册——Second Harvest",
        "register_at_label": "注册在",
        "confidential": "请完成所有必填字段。此信息保密，仅供工作人员使用。",
        "section_consent": "1 · 同意",
        "consent_question": "您是否同意Second Harvest存储您的数据？",
        "section_identity": "2 · 身份",
        "birth_year_label": "出生年份",
        "client_id_label": "客户ID",
        "client_id_placeholder": "新客户请留空",
        "first_name": "名",
        "middle_name": "中间名",
        "optional": "可选",
        "last_name": "姓",
        "section_contact": "3 · 联系方式",
        "phone_label": "电话号码",
        "phone_placeholder": "(555) 000-0000",
        "can_text_question": "我们可以发短信给您吗？",
        "street_address": "街道地址",
        "address_placeholder": "123 主街",
        "city_label": "城市",
        "zip_label": "邮政编码",
        "section_household": "4 · 家庭构成",
        "household_note": "这些数据用于为您的家庭准备适量的食物。",
        "children_label": "儿童（0–18岁）",
        "adults_label": "成人（19–59岁）",
        "seniors_label": "老人（60+岁）",
        "total_household": "👥 家庭总人数：",
        "section_race": "5 · 种族与民族",
        "race_note": "选择最能描述您家庭的选项。此信息仅用于报告目的。",
        "race_label": "家庭种族/民族",
        "submit_btn": "✅ 提交并预留我的名额",
        "consent_required": "您必须同意数据存储才能注册。",
        "first_name_required": "名字为必填项。",
        "last_name_required": "姓氏为必填项。",
        "phone_required": "电话号码为必填项。",
        "address_required": "街道地址为必填项。",
        "city_required": "城市为必填项。",
        "zip_required": "邮政编码为必填项。",
        "household_required": "家庭至少需要1名成员。",
        "back_to_list": "← 返回银行列表",
        "running_out_soon": "⚠️ 即将耗尽",
        "limited_visit": "🟡 有限——请尽快访问",
        "well_stocked": "🟢 库存充足",
        "open_badge": "🟢 开放",
        "filling_up": "🟡 即将满额",
        "full_badge": "🔴 已满",
        "here_now": "正在这里",
        "slots_left_label": "名额剩余",
        "taken": "已占用",
        "stocked": "有库存",
        "limited": "有限",
        "slots_open": "名额开放",
        "slots_used_today": "今日已用名额",
        "visitor_click": "👤 点击侧边栏中的**访客**在食物银行注册。",
        "people_served": "人数",
        "cancelled": "已取消",
    },
    "Tiếng Việt": {
        "app_name": "CalFoodConnect",
        "tagline": "Mạng lưới thực phẩm California",
        "home": "🏠 Trang chủ",
        "map": "🗺 Bản đồ",
        "food_banks": "🏪 Ngân hàng thực phẩm",
        "find_items": "📦 Tìm sản phẩm",
        "my_checkin": "✅ Đăng ký của tôi",
        "inventory": "📦 Kho hàng",
        "dashboard": "📊 Bảng điều khiển",
        "manage": "⚙️ Quản lý",
        "ai_insights": "🤖 AI Insights",
        "visitor": "👤 Khách",
        "host": "🔑 Quản trị",
        "sign_out": "🚪 Đăng xuất",
        "dark_mode": "🌙 Chế độ tối",
        "language": "🌐 Ngôn ngữ",
        "signed_in_as": "Đã đăng nhập",
        "find_food_today": "Tìm thực phẩm gần bạn. Hôm nay.",
        "hero_desc": "CalFoodConnect kết nối bạn với các ngân hàng thực phẩm California theo thời gian thực.",
        "food_banks_label": "Ngân hàng thực phẩm",
        "open_today": "Mở hôm nay",
        "slots_available": "Chỗ còn trống",
        "across_california": "Khắp California",
        "with_slots": "Còn chỗ trống",
        "register_to_secure": "Đăng ký để giữ chỗ",
        "all_food_banks": "🏪 Tất cả ngân hàng thực phẩm",
        "visitor_login": "Đăng nhập Khách",
        "host_login": "Đăng nhập Quản trị",
        "visitor_desc": "Tìm ngân hàng thực phẩm gần bạn, đăng ký chỗ và quản lý chuyến thăm.",
        "host_desc": "Quản lý kho hàng, phê duyệt đăng ký và xem hoạt động trực tiếp.",
        "your_name": "Tên của bạn (tùy chọn)",
        "enter_name": "Nhập tên của bạn",
        "host_password": "Mật khẩu quản trị",
        "password": "Mật khẩu",
        "continue_btn": "Tiếp tục →",
        "back": "← Quay lại",
        "wrong_password": "Sai mật khẩu. Gợi ý: host123",
        "slots_left": "chỗ còn lại",
        "register_at": "📋 Đăng ký tại",
        "you_are_registered": "✅ Bạn đã đăng ký ở đây.",
        "leave_queue_first": "Hãy rời hàng đợi hiện tại trước.",
        "no_slots": "Không còn chỗ trống hôm nay.",
        "log_in_visitor": "Đăng nhập với tư cách Khách để đăng ký.",
        "checked_in": "✅ Đã check-in",
        "registered": "📋 Đã đăng ký",
        "operations_overview": "Tổng quan hoạt động",
        "host_hero_desc": "Thống kê trực tiếp tại tất cả ngân hàng thực phẩm California.",
        "registered_label": "Đã đăng ký",
        "active_today": "hoạt động hôm nay",
        "arrived": "đã đến",
        "completed": "hoàn thành",
        "left_queue": "rời hàng đợi",
        "expiring": "⚠️ Sắp hết hạn",
        "items_7_days": "mặt hàng ≤7 ngày",
        "per_bank_snapshot": "🏪 Tổng quan từng ngân hàng",
        "hello": "Xin chào",
        "user_hero_desc": "Tìm ngân hàng thực phẩm gần bạn, đăng ký chỗ và check-in khi đến.",
        "im_here": "✅ Tôi đến rồi — Check-in ngay",
        "checked_in_success": "Đã check-in! 🎉 Đến quầy lễ tân.",
        "youre_checked_in": "Bạn đã check-in ✅",
        "leave_queue": "❌ Rời hàng đợi",
        "cannot_leave": "⛔ Không thể rời hàng đợi sau khi check-in. Liên hệ nhân viên nếu cần.",
        "left_queue_msg": "Bạn đã rời hàng đợi. Chỗ đã được giải phóng.",
        "available_banks": "🏪 Ngân hàng thực phẩm có sẵn",
        "available": "Có sẵn",
        "of": "trong số",
        "slots_remaining": "chỗ còn lại",
        "no_slots_left": "Không còn chỗ hôm nay.",
        "search_item": "🔍 Tìm kiếm mặt hàng",
        "search_placeholder": "vd. Gạo, Sữa bột…",
        "filter_bank": "Lọc theo ngân hàng",
        "all": "Tất cả",
        "status": "Trạng thái",
        "results": "kết quả",
        "no_items": "Không tìm thấy mặt hàng.",
        "not_registered": "Bạn chưa đăng ký tại ngân hàng nào. Chọn địa điểm bên dưới.",
        "choose_bank": "🏪 Chọn ngân hàng thực phẩm",
        "your_registration": "Đăng ký của bạn",
        "show_code": "Hiển thị mã xác nhận tại quầy khi đến.",
        "name": "Tên",
        "food_bank": "Ngân hàng thực phẩm",
        "confirmation_code": "Mã xác nhận",
        "household": "Hộ gia đình",
        "people": "người",
        "your_status": "Trạng thái",
        "checked_in_here": "✅ Đã check-in — Bạn đang ở đây!",
        "not_arrived": "📋 Đã đăng ký — Chưa đến",
        "your_actions": "Hành động của bạn",
        "check_in": "✅ Check-in",
        "press_arrive": "Nhấn khi bạn thực sự đến ngân hàng thực phẩm.",
        "ive_arrived": "✅ Tôi đã đến — Check-in cho tôi",
        "youre_checked_in_desk": "✅ Bạn đã check-in. Đến quầy lễ tân.",
        "leave_queue_label": "❌ Rời hàng đợi",
        "changed_plans": "Thay đổi kế hoạch? Điều này giải phóng chỗ cho người khác.",
        "already_checked_in": "⛔ Bạn đã check-in. Không thể rời hàng đợi ở giai đoạn này.",
        "leave_cancel": "❌ Rời hàng đợi / Hủy chuyến thăm",
        "slot_released": "Bạn đã rời hàng đợi. Chỗ của bạn đã được giải phóng.",
        "your_profile": "📋 Hồ sơ đã gửi",
        "whats_at": "📦 Có gì tại",
        "today": "hôm nay",
        "consent": "Đồng ý",
        "birth_year": "Năm sinh",
        "client_id": "ID khách hàng",
        "phone": "Điện thoại",
        "can_text": "Có thể nhắn tin",
        "address": "Địa chỉ",
        "city": "Thành phố",
        "zip_code": "Mã bưu chính",
        "children_018": "Trẻ em 0–18",
        "adults_1959": "Người lớn 19–59",
        "seniors_60": "Người cao tuổi 60+",
        "race_ethnicity": "Chủng tộc/Dân tộc",
        "new_client": "Khách hàng mới",
        "live_ops": "Hoạt động trực tiếp tại tất cả ngân hàng",
        "done": "hoàn thành",
        "individuals": "cá nhân",
        "le7days": "≤7 ngày",
        "analytics": "📈 Phân tích",
        "supply_weekly": "Cung cấp vs Nhu cầu hàng tuần",
        "inventory_status": "Trạng thái kho hàng",
        "days_expiry": "Ngày đến hết hạn",
        "manage_desc": "Check-in khách, đánh dấu phục vụ, điều chỉnh công suất",
        "live_queue": "👥 Hàng đợi trực tiếp",
        "capacity": "🎟 Công suất",
        "full_log": "📋 Nhật ký đầy đủ",
        "mark_served_label": "Đánh dấu khách đã phục vụ",
        "no_active_regs": "Không có đăng ký hoạt động tại",
        "served_btn": "✅ Đã phục vụ",
        "marked_served": "đã được đánh dấu phục vụ.",
        "daily_capacity": "Công suất hàng ngày mỗi ngân hàng",
        "max_families": "Số gia đình tối đa có thể đăng ký mỗi ngày.",
        "save_capacity": "💾 Lưu công suất",
        "capacity_updated": "Công suất đã cập nhật!",
        "todays_log": "Nhật ký hôm nay",
        "download_csv": "⬇️ Tải CSV",
        "no_regs_today": "Chưa có đăng ký hôm nay.",
        "ai_insights_title": "🤖 AI Insights & Dự báo",
        "ai_insights_desc": "Phân tích mạng lưới ngân hàng thực phẩm bằng học máy",
        "expiry_risk": "🔴 Dự báo rủi ro hết hạn",
        "redistribution": "🔄 Khuyến nghị phân phối lại AI",
        "demand_forecast": "📈 Mô phỏng dự báo nhu cầu",
        "ai_dashboard": "🧠 Bảng điều khiển AI Insights",
        "critical_risk": "Rủi ro nghiêm trọng",
        "high_risk": "Rủi ro cao",
        "moderate_risk": "Rủi ro vừa",
        "days_remaining": "ngày còn lại",
        "redistribute_to": "Phân phối lại đến",
        "surplus_at": "Thặng dư tại",
        "shortage_at": "Thiếu hụt tại",
        "units": "đơn vị",
        "forecast_7": "Dự báo nhu cầu 7 ngày",
        "forecast_30": "Dự báo nhu cầu 30 ngày",
        "network_health": "Điểm sức khỏe mạng lưới",
        "waste_risk": "Chỉ số rủi ro lãng phí",
        "coverage_rate": "Tỷ lệ bao phủ",
        "efficiency": "Hiệu quả phân phối",
        "registration_form": "📋 Đăng ký khách hàng — Second Harvest",
        "register_at_label": "Đăng ký tại",
        "confidential": "Vui lòng điền đầy đủ các trường bắt buộc. Thông tin này được bảo mật.",
        "section_consent": "1 · Đồng ý",
        "consent_question": "Bạn có đồng ý cho Second Harvest lưu trữ dữ liệu của bạn không?",
        "section_identity": "2 · Danh tính",
        "birth_year_label": "Năm sinh",
        "client_id_label": "ID khách hàng",
        "client_id_placeholder": "Để trống nếu là khách hàng mới",
        "first_name": "Tên",
        "middle_name": "Tên đệm",
        "optional": "Tùy chọn",
        "last_name": "Họ",
        "section_contact": "3 · Liên hệ",
        "phone_label": "Số điện thoại",
        "phone_placeholder": "(555) 000-0000",
        "can_text_question": "Chúng tôi có thể nhắn tin cho bạn không?",
        "street_address": "Địa chỉ đường phố",
        "address_placeholder": "123 Đường Chính",
        "city_label": "Thành phố",
        "zip_label": "Mã bưu chính",
        "section_household": "4 · Thành phần hộ gia đình",
        "household_note": "Các số liệu này được dùng để chuẩn bị đúng lượng thực phẩm cho gia đình bạn.",
        "children_label": "Trẻ em (0–18 tuổi)",
        "adults_label": "Người lớn (19–59 tuổi)",
        "seniors_label": "Người cao tuổi (60+ tuổi)",
        "total_household": "👥 Tổng số thành viên hộ gia đình:",
        "section_race": "5 · Chủng tộc & Dân tộc",
        "race_note": "Chọn tùy chọn mô tả tốt nhất hộ gia đình của bạn.",
        "race_label": "Chủng tộc / Dân tộc của hộ gia đình",
        "submit_btn": "✅ Gửi & Giữ chỗ của tôi",
        "consent_required": "Bạn phải đồng ý lưu trữ dữ liệu để đăng ký.",
        "first_name_required": "Tên là bắt buộc.",
        "last_name_required": "Họ là bắt buộc.",
        "phone_required": "Số điện thoại là bắt buộc.",
        "address_required": "Địa chỉ là bắt buộc.",
        "city_required": "Thành phố là bắt buộc.",
        "zip_required": "Mã bưu chính là bắt buộc.",
        "household_required": "Hộ gia đình phải có ít nhất 1 thành viên.",
        "back_to_list": "← Quay lại danh sách ngân hàng",
        "running_out_soon": "⚠️ Sắp hết",
        "limited_visit": "🟡 Hạn chế — hãy đến sớm",
        "well_stocked": "🟢 Đủ hàng",
        "open_badge": "🟢 Mở",
        "filling_up": "🟡 Sắp đầy",
        "full_badge": "🔴 Đầy",
        "here_now": "đang ở đây",
        "slots_left_label": "chỗ còn lại",
        "taken": "đã lấy",
        "stocked": "có hàng",
        "limited": "hạn chế",
        "slots_open": "chỗ trống",
        "slots_used_today": "Chỗ đã dùng hôm nay",
        "visitor_click": "👤 Nhấp vào **Khách** trong thanh bên để đăng ký tại ngân hàng thực phẩm.",
        "people_served": "Người",
        "cancelled": "Đã hủy",
    },
}

def T(key):
    lang = st.session_state.get("language", "English")
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"].get(key, key))

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
    "page":            "home",
    "show_login":      None,
    "show_reg_form":   False,
    "reg_target_bank": None,
    "language":        "English",
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
    regs = load_registrations()
    code = gen_code()
    family_size = max(int(profile.get("children",0))+int(profile.get("adults",0))+int(profile.get("seniors",0)),1)
    regs[code] = {
        "bank": bank, "family_size": family_size,
        "name": profile.get("first_name","Anonymous"),
        "date": today(), "status": "registered",
        "registered_at": datetime.now().strftime("%H:%M"),
        "checked_in_at": None, "served_at": None,
        **{k: profile.get(k) for k in ["consent","birth_year","client_id","first_name",
           "middle_name","last_name","phone","can_text","address","city","zip_code",
           "children","seniors","adults","race_ethnicity"]}
    }
    save_registrations(regs)
    return code, family_size

def checkin_user(code):
    regs = load_registrations()
    if code in regs and regs[code]["status"] == "registered":
        regs[code]["status"] = "checked_in"
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
        regs[code]["status"] = "served"
        regs[code]["served_at"] = datetime.now().strftime("%H:%M")
        save_registrations(regs)
        return True
    return False

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

RACE_OPTIONS = [
    "Prefer not to say","American Indian or Alaska Native","Asian",
    "Black or African American","Hispanic or Latino",
    "Middle Eastern or North African","Native Hawaiian or Other Pacific Islander",
    "White","Two or more races","Other",
]

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
    return pd.DataFrame(rows, columns=["bank_name","item_name","quantity","days_left","avg_daily_demand","supply_status"])

df = load_inventory()

# ══════════════════════════════════════════════════════════════════════════════
# AI FEATURE ENGINE (rule-based simulation)
# ══════════════════════════════════════════════════════════════════════════════
def compute_expiry_risk(df):
    """Score items by expiry risk: days_left weighted against daily demand."""
    risk = df.copy()
    risk["days_of_stock"] = risk["quantity"] / risk["avg_daily_demand"].clip(lower=1)
    risk["risk_score"] = (risk["avg_daily_demand"] * 3) / (risk["days_left"].clip(lower=0.1))
    risk["risk_level"] = pd.cut(
        risk["days_left"],
        bins=[-1, 3, 7, 14, 999],
        labels=["Critical", "High", "Moderate", "Low"]
    )
    return risk.sort_values("days_left")

def compute_redistribution(df):
    """Find items with surplus at one bank and shortage at another."""
    recs = []
    items = df["item_name"].unique()
    for item in items:
        sub = df[df["item_name"]==item].copy()
        if len(sub) < 2: continue
        sub["days_of_stock"] = sub["quantity"] / sub["avg_daily_demand"].clip(lower=1)
        surplus = sub[sub["days_of_stock"] > 20].nlargest(1, "quantity")
        shortage = sub[sub["days_left"] < 7].nsmallest(1, "days_left")
        if not surplus.empty and not shortage.empty:
            src = surplus.iloc[0]
            dst = shortage.iloc[0]
            if src["bank_name"] != dst["bank_name"]:
                transfer = int(src["quantity"] * 0.25)
                recs.append({
                    "item": item,
                    "from_bank": src["bank_name"],
                    "to_bank": dst["bank_name"],
                    "transfer_qty": transfer,
                    "urgency": "🔴 Urgent" if dst["days_left"] <= 3 else "🟡 Recommended",
                    "from_qty": int(src["quantity"]),
                    "to_days": int(dst["days_left"]),
                })
    return recs

def compute_demand_forecast(df, days=7):
    """Simulate demand forecast with seasonal noise."""
    forecasts = []
    for _, row in df.iterrows():
        base = row["avg_daily_demand"]
        daily = []
        for d in range(days):
            noise = random.uniform(0.85, 1.18)
            weekend_bump = 1.15 if d % 7 in [5,6] else 1.0
            daily.append(round(base * noise * weekend_bump, 1))
        forecasts.append({
            "bank": row["bank_name"],
            "item": row["item_name"],
            "daily_forecasts": daily,
            "total_7d": sum(daily),
            "current_qty": row["quantity"],
            "days_left": row["days_left"],
            "will_run_short": sum(daily) > row["quantity"],
        })
    return forecasts

def compute_network_kpis(df):
    total_qty = df["quantity"].sum()
    total_demand_7d = (df["avg_daily_demand"] * 7).sum()
    coverage = min(100, round(total_qty / max(total_demand_7d, 1) * 100, 1))
    critical = len(df[df["days_left"] <= 3])
    expiring = len(df[df["days_left"] <= 7])
    waste_risk = round(critical / max(len(df), 1) * 100, 1)
    health = max(0, round(100 - waste_risk * 1.5 - (expiring / max(len(df),1) * 20), 1))
    efficiency = round(random.uniform(78, 94), 1)
    return {
        "health": health,
        "waste_risk": waste_risk,
        "coverage": coverage,
        "efficiency": efficiency,
        "critical_count": critical,
        "expiring_count": expiring,
    }

# ══════════════════════════════════════════════════════════════════════════════
# UPGRADED THEME — Warm Earth × Teal Futurism
# ══════════════════════════════════════════════════════════════════════════════
def inject_css(dark):
    bg       = "#080c12" if dark else "#f0f4f8"
    surface  = "#0f1623" if dark else "#ffffff"
    surface2 = "#161f30" if dark else "#e8eef6"
    surface3 = "#1c2840" if dark else "#dde6f0"
    border   = "#243048" if dark else "#c8d6e8"
    text     = "#e2eaf5" if dark else "#0a1628"
    muted    = "#5a7090" if dark else "#5a6a80"
    accent   = "#00e5c0"   # teal-mint
    accent2  = "#ff8c42"   # warm amber
    accent3  = "#a78bfa"   # violet
    accent4  = "#38bdf8"   # sky blue
    sb_bg    = "#060a10" if dark else "#0a1628"
    danger   = "#ff4d6d"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700;800&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; }}

    html, body, [class*="css"], .stApp {{
        font-family: 'Space Grotesk', sans-serif !important;
        background: {bg} !important;
        color: {text} !important;
    }}
    .stApp {{ background: {bg} !important; }}

    /* Animated background grid */
    .stApp::before {{
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient({border}22 1px, transparent 1px),
            linear-gradient(90deg, {border}22 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }}

    section[data-testid="stSidebar"] {{
        background: {sb_bg} !important;
        border-right: 1px solid {border};
    }}
    section[data-testid="stSidebar"] * {{ color: {text} !important; }}
    section[data-testid="stSidebar"] .stRadio > label {{ display: none; }}
    section[data-testid="stSidebar"] .stRadio label {{
        display: flex !important;
        padding: 9px 14px;
        border-radius: 8px;
        font-size: .85rem;
        font-weight: 500;
        cursor: pointer;
        transition: all .2s;
        color: {muted} !important;
        border: 1px solid transparent;
    }}
    section[data-testid="stSidebar"] .stRadio label:hover {{
        background: {surface2} !important;
        color: {text} !important;
        border-color: {border};
    }}
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {{
        background: {accent}18 !important;
        color: {accent} !important;
        border-color: {accent}44;
    }}

    h1, h2, h3 {{
        font-family: 'Playfair Display', serif !important;
        color: {text} !important;
    }}

    /* ─── Cards ─── */
    .lc-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all .25s;
        position: relative;
        overflow: hidden;
    }}
    .lc-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, {accent}, {accent3}, {accent4});
        opacity: 0;
        transition: opacity .25s;
    }}
    .lc-card:hover {{ border-color: {accent}55; box-shadow: 0 8px 40px {accent}12; }}
    .lc-card:hover::before {{ opacity: 1; }}

    /* ─── Metric Cards ─── */
    .lc-metric-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 22px 18px;
        transition: all .25s;
        position: relative;
        overflow: hidden;
    }}
    .lc-metric-card:hover {{
        border-color: {accent}66;
        box-shadow: 0 0 28px {accent}18;
        transform: translateY(-2px);
    }}
    .lc-metric-icon {{ font-size: 1.6rem; margin-bottom: 10px; }}
    .lc-metric-label {{
        font-size: .65rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: .12em;
        color: {muted}; margin-bottom: 6px;
    }}
    .lc-metric-val {{
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem; font-weight: 800; color: {text};
        line-height: 1;
    }}
    .lc-metric-sub {{ font-size: .72rem; color: {muted}; margin-top: 6px; }}

    /* ─── KPI Cards with color accent ─── */
    .kpi-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all .25s;
    }}
    .kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,.3); }}
    .kpi-val {{
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem; font-weight: 800;
        background: linear-gradient(135deg, {accent}, {accent4});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1;
    }}
    .kpi-label {{
        font-size: .68rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: .1em;
        color: {muted}; margin-top: 6px;
    }}

    /* ─── Hero ─── */
    .lc-hero {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 52px 56px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }}
    .lc-hero::before {{
        content: '';
        position: absolute;
        top: -100px; right: -100px;
        width: 400px; height: 400px;
        background: radial-gradient({accent}20, transparent 65%);
        border-radius: 50%;
    }}
    .lc-hero::after {{
        content: '';
        position: absolute;
        bottom: -80px; left: 30%;
        width: 260px; height: 260px;
        background: radial-gradient({accent3}18, transparent 65%);
        border-radius: 50%;
    }}
    .lc-hero-tag {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {accent}15;
        border: 1px solid {accent}40;
        color: {accent};
        font-size: .68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .12em;
        padding: 5px 14px;
        border-radius: 99px;
        margin-bottom: 20px;
    }}
    .lc-hero h1 {{
        font-family: 'Playfair Display', serif !important;
        font-size: clamp(2rem, 4vw, 3rem) !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 16px !important;
        color: {text} !important;
    }}
    .lc-hero p {{ font-size: 1rem; color: {muted}; max-width: 500px; line-height: 1.7; }}

    /* ─── Accent helpers ─── */
    .accent  {{ color: {accent} !important; }}
    .accent2 {{ color: {accent2} !important; }}
    .accent3 {{ color: {accent3} !important; }}
    .accent4 {{ color: {accent4} !important; }}

    /* ─── Pills ─── */
    .pill {{
        display: inline-block;
        padding: 3px 11px;
        border-radius: 99px;
        font-size: .68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .05em;
    }}
    .pill-ok   {{ background: {accent}18; border: 1px solid {accent}44; color: {accent}; }}
    .pill-low  {{ background: {accent2}18; border: 1px solid {accent2}44; color: {accent2}; }}
    .pill-crit {{ background: {danger}18; border: 1px solid {danger}44; color: {danger}; }}
    .pill-reg  {{ background: {accent3}18; border: 1px solid {accent3}44; color: {accent3}; }}
    .pill-ci   {{ background: {accent}18; border: 1px solid {accent}44; color: {accent}; }}
    .pill-sky  {{ background: {accent4}18; border: 1px solid {accent4}44; color: {accent4}; }}

    /* ─── Slots bar ─── */
    .slots-bar-wrap {{
        background: {surface3};
        border-radius: 99px;
        height: 5px;
        margin-top: 8px;
        overflow: hidden;
    }}
    .slots-bar {{
        height: 5px;
        border-radius: 99px;
        background: linear-gradient(90deg, {accent}, {accent4});
        transition: width .5s ease;
    }}

    /* ─── State boxes ─── */
    .ci-state-box {{ border-radius: 14px; padding: 20px 24px; border: 1px solid; margin-top: 16px; }}
    .ci-registered {{ border-color: {accent}44; background: {accent}0a; }}
    .ci-checkedin  {{ border-color: {accent2}44; background: {accent2}0a; }}

    /* ─── Code box ─── */
    .code-box {{
        font-family: 'DM Mono', monospace;
        font-size: 1.7rem;
        font-weight: 500;
        color: {accent};
        background: {accent}0c;
        border: 1px solid {accent}33;
        border-radius: 12px;
        padding: 12px 28px;
        display: inline-block;
        letter-spacing: .2em;
        margin: 8px 0;
    }}

    /* ─── Login wrap ─── */
    .login-wrap {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 52px 44px;
        max-width: 480px;
        margin: 40px auto;
        box-shadow: 0 0 80px {accent}08;
        position: relative;
        overflow: hidden;
    }}
    .login-wrap::before {{
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient({accent}18, transparent 70%);
        border-radius: 50%;
    }}

    /* ─── Divider ─── */
    .lc-divider {{ border: none; border-top: 1px solid {border}; margin: 28px 0; }}

    /* ─── AI Risk Cards ─── */
    .risk-critical {{
        background: {danger}0a;
        border: 1px solid {danger}44;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }}
    .risk-high {{
        background: {accent2}0a;
        border: 1px solid {accent2}44;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }}
    .risk-moderate {{
        background: {accent4}0a;
        border: 1px solid {accent4}44;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }}

    /* ─── Redistribution card ─── */
    .redist-card {{
        background: {surface2};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 12px;
        border-left: 3px solid {accent3};
    }}

    /* ─── Buttons ─── */
    .stButton > button {{
        background: linear-gradient(135deg, {accent}, {accent4}) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 10px 22px !important;
        letter-spacing: .02em !important;
        transition: all .2s !important;
    }}
    .stButton > button:hover {{ opacity: .88 !important; transform: translateY(-1px) !important; }}

    /* ─── Inputs ─── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: {surface2} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        color: {text} !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px {accent}22 !important;
    }}

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {{
        background: {surface2};
        border-radius: 12px;
        padding: 4px;
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {muted};
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        font-size: .88rem;
    }}
    .stTabs [aria-selected="true"] {{
        background: {surface} !important;
        color: {accent} !important;
    }}

    /* ─── Expanders ─── */
    .streamlit-expanderHeader {{
        background: {surface2} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: {text} !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    .streamlit-expanderContent {{
        background: {surface} !important;
        border: 1px solid {border} !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }}

    /* ─── Alerts ─── */
    .stSuccess {{ background: {accent}12 !important; border-left-color: {accent} !important; }}
    .stWarning {{ background: {accent2}12 !important; border-left-color: {accent2} !important; }}
    .stError   {{ background: {danger}12 !important; border-left-color: {danger} !important; }}
    .stInfo    {{ background: {accent3}12 !important; border-left-color: {accent3} !important; }}

    /* ─── Progress / gauge ─── */
    .gauge-ring {{
        width: 120px; height: 120px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem; font-weight: 800;
        position: relative;
    }}

    /* ─── Section header ─── */
    .section-header {{
        display: flex; align-items: center; gap: 12px;
        margin: 28px 0 16px;
    }}
    .section-header-line {{
        flex: 1;
        height: 1px;
        background: linear-gradient({border}, transparent);
    }}
    .section-header-text {{
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 700;
        white-space: nowrap;
    }}

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: {bg}; }}
    ::-webkit-scrollbar-thumb {{ background: {border}; border-radius: 99px; }}

    footer, #MainMenu, header {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

inject_css(st.session_state.dark_mode)

# ── Shared helpers ────────────────────────────────────────────────────────────
def slots_bar_html(bank):
    cap   = load_capacity().get(bank, 50)
    used  = len(get_bank_registrations(bank))
    left  = max(0, cap - used)
    pct   = int((used / cap) * 100) if cap else 0
    color = "#00e5c0" if left > 10 else "#ff8c42" if left > 0 else "#ff4d6d"
    label = T("open_badge") if left > 10 else T("filling_up") if left > 0 else T("full_badge")
    return left, cap, pct, color, label

def avail_label(days_left):
    if days_left <= 2: return T("running_out_soon")
    if days_left <= 7: return T("limited_visit")
    return T("well_stocked")

def section_header(text):
    st.markdown(f"""
    <div class="section-header">
      <div class="section-header-text">{text}</div>
      <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 14px 10px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:800;
                  background:linear-gradient(135deg,#00e5c0,#38bdf8);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        🥗 {T('app_name')}
      </div>
      <div style="font-size:.62rem;color:#3a5070;margin-top:3px;text-transform:uppercase;letter-spacing:.1em;">
        {T('tagline')}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Language selector
    lang_opts = list(TRANSLATIONS.keys())
    lang_idx  = lang_opts.index(st.session_state.language)
    new_lang  = st.selectbox(T("language"), lang_opts, index=lang_idx, key="lang_select")
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

    dm = st.toggle(T("dark_mode"), value=st.session_state.dark_mode)
    if dm != st.session_state.dark_mode:
        st.session_state.dark_mode = dm
        st.rerun()

    st.markdown("<hr style='border-color:#243048;margin:10px 0'>", unsafe_allow_html=True)

    # Nav
    if not st.session_state.logged_in:
        nav_keys  = ["home","map","food_banks","find_items"]
    elif st.session_state.role == "user":
        nav_keys  = ["home","map","food_banks","find_items","my_checkin"]
    else:
        nav_keys  = ["home","map","food_banks","inventory","dashboard","manage","ai_insights"]

    nav_labels = [T(k) for k in nav_keys]

    if st.session_state.page not in nav_keys:
        st.session_state.page = nav_keys[0]

    page_label = st.radio("nav", nav_labels, label_visibility="collapsed",
                          index=nav_keys.index(st.session_state.page))
    page = nav_keys[nav_labels.index(page_label)]
    st.session_state.page = page

    st.markdown("<hr style='border-color:#243048;margin:10px 0'>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        ca, cb = st.columns(2)
        with ca:
            if st.button(T("visitor"), use_container_width=True):
                st.session_state.show_login = "user"; st.rerun()
        with cb:
            if st.button(T("host"), use_container_width=True):
                st.session_state.show_login = "host"; st.rerun()
    else:
        role_icon = "👤" if st.session_state.role == "user" else "🔑"
        bank_info = ""
        if st.session_state.role == "user" and st.session_state.registered_bank:
            status_txt = T("checked_in") if st.session_state.checked_in else T("registered")
            bank_info  = f'<div style="font-size:.72rem;color:#00e5c0;margin-top:4px;">{status_txt}</div><div style="font-size:.68rem;color:#5a7090;">{st.session_state.registered_bank}</div>'

        st.markdown(f"""
        <div style="padding:12px 14px;background:#0f1623;border-radius:10px;margin-bottom:10px;border:1px solid #243048;">
          <div style="font-size:.62rem;color:#5a7090;text-transform:uppercase;letter-spacing:.08em;">{T('signed_in_as')}</div>
          <div style="font-weight:700;margin-top:2px;">{role_icon} {st.session_state.user_name or st.session_state.role.title()}</div>
          {f'<div style="font-family:DM Mono,monospace;font-size:.78rem;color:#00e5c0;margin-top:4px;">{st.session_state.user_code}</div>' if st.session_state.user_code else ''}
          {bank_info}
        </div>
        """, unsafe_allow_html=True)

        if st.button(T("sign_out"), use_container_width=True):
            lang = st.session_state.language
            dark = st.session_state.dark_mode
            for k, v in defaults.items():
                st.session_state[k] = v
            st.session_state.language = lang
            st.session_state.dark_mode = dark
            st.rerun()

    st.markdown(f"""
    <div style="position:fixed;bottom:14px;left:0;width:240px;text-align:center;
                font-size:.58rem;color:#243048;">
      CalFoodConnect · California · 2026
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.show_login and not st.session_state.logged_in:
    role  = st.session_state.show_login
    icon  = "👤" if role == "user" else "🔑"
    title = T("visitor_login") if role == "user" else T("host_login")
    desc  = T("visitor_desc") if role == "user" else T("host_desc")

    st.markdown(f"""
    <div class="login-wrap">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;margin-bottom:6px;">
        {icon} {title}
      </div>
      <div style="color:#5a7090;font-size:.9rem;margin-bottom:28px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form(f"login_form_{role}"):
        name = st.text_input(T("your_name"), placeholder=T("enter_name"))
        if role == "host":
            pwd = st.text_input(T("host_password"), type="password", placeholder=T("password"))
        go = st.form_submit_button(T("continue_btn"), use_container_width=True)

        if go:
            if role == "host":
                if pwd == "host123":
                    st.session_state.logged_in  = True
                    st.session_state.role       = "host"
                    st.session_state.user_name  = name or "Host"
                    st.session_state.show_login = None
                    st.session_state.page       = "dashboard"
                    st.rerun()
                else:
                    st.error(T("wrong_password"))
            else:
                st.session_state.logged_in   = True
                st.session_state.role        = "user"
                st.session_state.user_name   = name or "Visitor"
                st.session_state.show_login  = None
                st.session_state.page        = "home"
                st.rerun()

    if st.button(T("back")):
        st.session_state.show_login = None; st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# REGISTRATION FORM
# ══════════════════════════════════════════════════════════════════════════════
def render_registration_form(bank):
    accent = "#00e5c0"
    border = "#243048" if st.session_state.dark_mode else "#c8d6e8"
    muted  = "#5a7090"

    st.markdown(f"""
    <div style="background:{'#0f1623' if st.session_state.dark_mode else '#fff'};
                border:1px solid {border};border-radius:18px;
                padding:32px 36px;margin-bottom:24px;">
      <div style="display:inline-block;background:{accent}18;border:1px solid {accent}44;
                  color:{accent};font-size:.65rem;font-weight:700;text-transform:uppercase;
                  letter-spacing:.12em;padding:4px 14px;border-radius:99px;margin-bottom:16px;">
        {T('registration_form')}
      </div>
      <div style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;margin-bottom:6px;">
        {T('register_at_label')} {bank}
      </div>
      <div style="color:{muted};font-size:.85rem;">{T('confidential')}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("client_registration_form", clear_on_submit=False):
        st.markdown(f"#### {T('section_consent')}")
        consent = st.radio(f"{T('consent_question')}  \\*", options=["Yes","No"], horizontal=True, index=0)

        st.markdown("<hr style='border-color:#243048;margin:18px 0'>", unsafe_allow_html=True)
        st.markdown(f"#### {T('section_identity')}")
        col_by, col_id = st.columns(2)
        with col_by:
            birth_year = st.number_input(f"{T('birth_year_label')}  \\*", min_value=1900, max_value=date.today().year, value=1980, step=1)
        with col_id:
            client_id = st.text_input(T("client_id_label"), placeholder=T("client_id_placeholder"))

        col_fn, col_mn, col_ln = st.columns([2,1,2])
        with col_fn:  first_name  = st.text_input(f"{T('first_name')}  \\*", placeholder=T("first_name"))
        with col_mn:  middle_name = st.text_input(T("middle_name"), placeholder=T("optional"))
        with col_ln:  last_name   = st.text_input(f"{T('last_name')}  \\*", placeholder=T("last_name"))

        st.markdown("<hr style='border-color:#243048;margin:18px 0'>", unsafe_allow_html=True)
        st.markdown(f"#### {T('section_contact')}")
        col_ph, col_txt = st.columns([2,1])
        with col_ph: phone    = st.text_input(f"{T('phone_label')}  \\*", placeholder=T("phone_placeholder"))
        with col_txt: can_text = st.radio(f"{T('can_text_question')}  \\*", options=["Yes","No"], horizontal=True, index=0)

        address = st.text_input(f"{T('street_address')}  \\*", placeholder=T("address_placeholder"))
        col_city, col_zip = st.columns([3,1])
        with col_city: city     = st.text_input(f"{T('city_label')}  \\*", placeholder=T("city_label"))
        with col_zip:  zip_code = st.text_input(f"{T('zip_label')}  \\*", placeholder="00000")

        st.markdown("<hr style='border-color:#243048;margin:18px 0'>", unsafe_allow_html=True)
        st.markdown(f"#### {T('section_household')}")
        st.caption(T("household_note"))
        col_ch, col_ad, col_sr = st.columns(3)
        with col_ch: children = st.selectbox(f"{T('children_label')}  \\*", list(range(0,11)), index=0)
        with col_ad: adults   = st.selectbox(f"{T('adults_label')}  \\*",   list(range(0,11)), index=1)
        with col_sr: seniors  = st.selectbox(f"{T('seniors_label')}  \\*",  list(range(0,11)), index=0)

        total_members = int(children)+int(adults)+int(seniors)
        if total_members > 0:
            st.markdown(f"<div style='font-size:.82rem;color:#00e5c0;margin-top:4px;'>{T('total_household')} <b>{total_members}</b></div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#243048;margin:18px 0'>", unsafe_allow_html=True)
        st.markdown(f"#### {T('section_race')}")
        st.caption(T("race_note"))
        race_ethnicity = st.selectbox(f"{T('race_label')}  \\*", options=RACE_OPTIONS)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(T("submit_btn"), use_container_width=True)

    if submitted:
        errors = []
        if consent != "Yes":       errors.append(T("consent_required"))
        if not first_name.strip(): errors.append(T("first_name_required"))
        if not last_name.strip():  errors.append(T("last_name_required"))
        if not phone.strip():      errors.append(T("phone_required"))
        if not address.strip():    errors.append(T("address_required"))
        if not city.strip():       errors.append(T("city_required"))
        if not zip_code.strip():   errors.append(T("zip_required"))
        if total_members == 0:     errors.append(T("household_required"))
        if errors:
            for e in errors: st.error(e)
            return False, None

        return True, {
            "consent": consent, "birth_year": int(birth_year),
            "client_id": client_id.strip() or None,
            "first_name": first_name.strip(), "middle_name": middle_name.strip() or None,
            "last_name": last_name.strip(), "phone": phone.strip(), "can_text": can_text,
            "address": address.strip(), "city": city.strip(), "zip_code": zip_code.strip(),
            "children": int(children), "adults": int(adults), "seniors": int(seniors),
            "race_ethnicity": race_ethnicity,
        }
    return False, None

def reg_button(bank, key_suffix):
    if not (st.session_state.logged_in and st.session_state.role == "user"):
        st.info(T("log_in_visitor")); return
    left = get_slots_left(bank)
    if st.session_state.registered_bank == bank:
        st.info(T("you_are_registered"))
    elif st.session_state.registered_bank:
        st.warning(T("leave_queue_first"))
    elif left == 0:
        st.error(T("no_slots"))
    else:
        if st.button(f"{T('register_at')} {bank}", key=f"reg_{key_suffix}", use_container_width=True):
            st.session_state.show_reg_form   = True
            st.session_state.reg_target_bank = bank
            st.session_state.page            = "my_checkin"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# CHART THEME
# ══════════════════════════════════════════════════════════════════════════════
def chart_layout(dark):
    bg = "#080c12" if dark else "#ffffff"
    fc = "#e2eaf5" if dark else "#0a1628"
    gc = "#243048" if dark else "#c8d6e8"
    return dict(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(family="Space Grotesk", color=fc, size=11),
        xaxis=dict(gridcolor=gc, linecolor=gc),
        yaxis=dict(gridcolor=gc, linecolor=gc),
        margin=dict(t=44, b=20, l=20, r=20),
    )

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ HOME PAGE ████████████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
if page == "home":

    if not st.session_state.logged_in:
        st.markdown(f"""
        <div class="lc-hero">
          <div class="lc-hero-tag">🌎 {T('tagline')}</div>
          <h1>{T('find_food_today')}</h1>
          <p>{T('hero_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

        open_banks  = sum(1 for b in BANKS if get_slots_left(b) > 0)
        total_slots = sum(get_slots_left(b) for b in BANKS)
        c1, c2, c3 = st.columns(3)
        for col, icon, lbl, val, sub in [
            (c1,"🏪",T("food_banks_label"),len(BANKS),T("across_california")),
            (c2,"✅",T("open_today"),open_banks,T("with_slots")),
            (c3,"🎟️",T("slots_available"),total_slots,T("register_to_secure")),
        ]:
            col.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">{icon}</div>
              <div class="lc-metric-label">{lbl}</div>
              <div class="lc-metric-val">{val}</div>
              <div class="lc-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        section_header(T("all_food_banks"))
        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            items = df[df["bank_name"] == bank]
            cats  = " · ".join(items["item_name"].tolist()[:4])
            st.markdown(f"""
            <div class="lc-card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
              <div>
                <div style="font-family:'Playfair Display',serif;font-weight:700;">{bank}</div>
                <div style="font-size:.76rem;color:#5a7090;margin-top:3px;">🥫 {cats}</div>
              </div>
              <div style="text-align:right;">
                <span style="color:{color};font-weight:700;font-size:.85rem;">{badge}</span>
                <div style="font-size:.72rem;color:#5a7090;">{left} {T('slots_left')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        st.info(T("visitor_click"))

    elif st.session_state.role == "user":
        name = st.session_state.user_name
        st.markdown(f"""
        <div class="lc-hero">
          <div class="lc-hero-tag">👋 Welcome</div>
          <h1>{T('hello')}, <span class="accent">{name}</span>.</h1>
          <p>{T('user_hero_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.registered_bank:
            bank = st.session_state.registered_bank
            cls  = "ci-checkedin" if st.session_state.checked_in else "ci-registered"
            stxt = T("checked_in") if st.session_state.checked_in else T("registered")
            st.markdown(f"""
            <div class="ci-state-box {cls}">
              <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.1rem;">{stxt}</div>
              <div style="margin-top:6px;font-size:.88rem;color:#5a7090;">
                {T('food_bank')}: <b style="color:#e2eaf5;">{bank}</b>
              </div>
              <div class="code-box" style="margin-top:12px;">{st.session_state.user_code}</div>
              <div style="font-size:.7rem;color:#5a7090;margin-top:4px;">{T('show_code')}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

            col_ci, col_dr = st.columns(2)
            with col_ci:
                if not st.session_state.checked_in:
                    if st.button(T("im_here"), use_container_width=True, key="home_ci"):
                        if checkin_user(st.session_state.user_code):
                            st.session_state.checked_in = True
                            st.success(T("checked_in_success")); st.rerun()
                else:
                    st.success(T("youre_checked_in"))
            with col_dr:
                if st.session_state.checked_in:
                    st.markdown(f"""<div style="padding:10px 16px;background:#ff4d6d0d;border:1px solid #ff4d6d33;border-radius:10px;font-size:.84rem;color:#ff4d6d;">{T('cannot_leave')}</div>""", unsafe_allow_html=True)
                else:
                    if st.button(T("leave_queue"), use_container_width=True, key="home_dr"):
                        deregister_user(st.session_state.user_code)
                        st.session_state.registered_bank = None
                        st.session_state.user_code = None
                        st.session_state.checked_in = False
                        st.warning(T("left_queue_msg")); st.rerun()

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        section_header(T("available_banks"))
        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            items = df[df["bank_name"] == bank]
            cats  = " · ".join(items["item_name"].tolist()[:5])
            with st.expander(f"🏪  {bank}   ·   {badge}   ({left} {T('slots_left')})"):
                st.markdown(f"**{T('available')}:** {cats}")
                st.markdown(f"""<div style="font-size:.74rem;color:#5a7090;margin-bottom:4px;">{left} {T('of')} {cap} {T('slots_remaining')}</div>
                <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>""", unsafe_allow_html=True)
                st.markdown("")
                if not st.session_state.registered_bank and left > 0:
                    if st.button(f"{T('register_at')} {bank}", key=f"home_reg_{bank}"):
                        st.session_state.show_reg_form = True; st.session_state.reg_target_bank = bank
                        st.session_state.page = "my_checkin"; st.rerun()
                elif st.session_state.registered_bank == bank: st.info(T("you_are_registered"))
                elif st.session_state.registered_bank: st.warning(T("leave_queue_first"))
                elif left == 0: st.error(T("no_slots_left"))

    else:  # host home
        st.markdown(f"""
        <div class="lc-hero">
          <div class="lc-hero-tag">🔑 Host</div>
          <h1>{T('operations_overview')}</h1>
          <p>{T('host_hero_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

        regs   = load_registrations()
        t      = today()
        t_regs = [v for v in regs.values() if v.get("date") == t]
        total_r  = len([v for v in t_regs if v["status"] in ("registered","checked_in")])
        total_ci = len([v for v in t_regs if v["status"] == "checked_in"])
        total_sv = len([v for v in t_regs if v["status"] == "served"])
        total_cx = len([v for v in t_regs if v["status"] == "cancelled"])
        expiring = len(df[df["days_left"] <= 7])

        cols = st.columns(5)
        for col, icon, lbl, val, sub in [
            (cols[0],"📋",T("registered_label"),total_r,T("active_today")),
            (cols[1],"✅",T("checked_in"),total_ci,T("arrived")),
            (cols[2],"🤝","Served",total_sv,T("completed")),
            (cols[3],"❌",T("cancelled"),total_cx,T("left_queue")),
            (cols[4],"⚠️",T("expiring"),expiring,T("items_7_days")),
        ]:
            col.markdown(f"""<div class="lc-metric-card">
              <div class="lc-metric-icon">{icon}</div>
              <div class="lc-metric-label">{lbl}</div>
              <div class="lc-metric-val">{val}</div>
              <div class="lc-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        section_header(T("per_bank_snapshot"))
        cols2 = st.columns(2)
        for i, bank in enumerate(BANKS):
            b_regs = [v for v in t_regs if v.get("bank") == bank]
            b_r  = len([v for v in b_regs if v["status"] == "registered"])
            b_ci = len([v for v in b_regs if v["status"] == "checked_in"])
            b_sv = len([v for v in b_regs if v["status"] == "served"])
            left, cap, pct, color, badge = slots_bar_html(bank)
            with cols2[i % 2]:
                st.markdown(f"""
                <div class="lc-card">
                  <div style="font-family:'Playfair Display',serif;font-weight:700;">{bank}</div>
                  <div style="display:flex;gap:14px;margin:8px 0;font-size:.8rem;flex-wrap:wrap;">
                    <span><b style="color:#a78bfa">{b_r}</b> {T('registered_label')}</span>
                    <span><b style="color:#00e5c0">{b_ci}</b> {T('here_now')}</span>
                    <span><b style="color:#ff8c42">{b_sv}</b> served</span>
                  </div>
                  <div style="font-size:.72rem;color:#5a7090;">{left} {T('of')} {cap} {T('slots_left_label')} · {badge}</div>
                  <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ MAP PAGE █████████████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "map":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('map')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">All California partner locations with live slot availability</div>
    </div>""", unsafe_allow_html=True)

    map_rows = []
    for bank in BANKS:
        lat, lon = BANK_COORDS[bank]
        left, cap, pct, color, badge = slots_bar_html(bank)
        items    = df[df["bank_name"] == bank]
        top_i    = ", ".join(items["item_name"].tolist()[:3])
        min_days = int(items["days_left"].min())
        map_rows.append(dict(Bank=bank,Lat=lat,Lon=lon,Left=left,Cap=cap,
                             Status=badge.split()[1],Color=color,Items=top_i,MinDays=min_days))
    map_df = pd.DataFrame(map_rows)

    dark   = st.session_state.dark_mode
    bg     = "#080c12" if dark else "#f0f4f8"
    land   = "#1c2840" if dark else "#e0e8f0"
    ocean  = "#0f1623" if dark else "#c8d8ee"

    fig_map = go.Figure()
    for _, r in map_df.iterrows():
        size = max(14, r["Left"] // 3 + 12)
        fig_map.add_trace(go.Scattergeo(
            lat=[r["Lat"]], lon=[r["Lon"]],
            mode="markers+text",
            marker=dict(size=size, color=r["Color"], line=dict(width=2, color="rgba(255,255,255,0.1)"), opacity=0.9),
            text=r["Bank"].split()[0], textposition="top center",
            textfont=dict(color="#e2eaf5", size=10),
            hovertemplate=(f"<b>{r['Bank']}</b><br>Status: {r['Status']}<br>"
                           f"Slots: {r['Left']} / {r['Cap']}<br>Top items: {r['Items']}<br>"
                           f"Earliest expiry: {r['MinDays']} days<extra></extra>"),
            showlegend=False,
        ))

    fig_map.update_layout(
        geo=dict(scope="usa", showland=True, landcolor=land, showocean=True, oceancolor=ocean,
                 showlakes=True, lakecolor=ocean, showcountries=True, countrycolor="#243048",
                 showsubunits=True, subunitcolor="#243048",
                 center=dict(lat=37.2, lon=-119.5), projection_scale=4.8),
        paper_bgcolor=bg, margin=dict(l=0,r=0,t=0,b=0), height=440,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    section_header("📍 All Locations")
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
                  <div style="font-family:'Playfair Display',serif;font-weight:700;">{bank}</div>
                  <div style="font-size:.76rem;color:#5a7090;margin-top:3px;">{avail}</div>
                </div>
                <span style="color:{color};font-weight:700;font-size:.82rem;">{badge}</span>
              </div>
              <div style="font-size:.72rem;color:#5a7090;margin-top:8px;">{left} {T('of')} {cap} {T('slots_left_label')}</div>
              <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ FOOD BANKS PAGE ██████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "food_banks":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('food_banks')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">Browse all partner food banks and their available inventory</div>
    </div>""", unsafe_allow_html=True)

    for bank in BANKS:
        left, cap, pct, color, badge = slots_bar_html(bank)
        items = df[df["bank_name"] == bank].copy()
        n_ok  = len(items[items["supply_status"]=="OK"])
        n_low = len(items[items["supply_status"]=="Low"])

        with st.expander(f"🏪  {bank}   ·   {badge}   ·   {left} {T('slots_left')}"):
            col_l, col_r = st.columns([2,1])
            with col_l:
                st.markdown(f"""<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
                  <span class="pill pill-ok">{n_ok} {T('stocked')}</span>
                  <span class="pill pill-low">{n_low} {T('limited')}</span>
                  <span class="pill pill-ci">{left} {T('slots_open')}</span>
                </div>""", unsafe_allow_html=True)
            with col_r:
                st.markdown(f"""<div style="font-size:.7rem;color:#5a7090;">{T('slots_used_today')}</div>
                <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>
                <div style="font-size:.68rem;color:#5a7090;margin-top:2px;">{cap-left}/{cap} {T('taken')}</div>""", unsafe_allow_html=True)

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
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #243048;">
                      <span style="font-weight:500;">{row['item_name']}</span>
                      <span>
                        <span class="pill {pcls}" style="margin-right:8px;">{row['supply_status']}</span>
                        <span style="font-size:.72rem;color:#5a7090;">{av}</span>
                      </span>
                    </div>""", unsafe_allow_html=True)

            st.markdown("")
            reg_button(bank, f"fb_{bank}")

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ FIND ITEMS / INVENTORY ███████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page in ("find_items","inventory"):
    is_host = st.session_state.role == "host"
    title   = T("inventory") if is_host else T("find_items")

    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{title}</div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,2,1])
    with c1: item_q = st.text_input(T("search_item"), placeholder=T("search_placeholder"))
    with c2: bank_f = st.selectbox(T("filter_bank"), [T("all")] + BANKS)
    with c3: stat_f = st.selectbox(T("status"), [T("all"),"OK","Low","Critical"])

    filt = df.copy()
    if item_q:  filt = filt[filt["item_name"].str.contains(item_q, case=False)]
    if bank_f not in (T("all"),"All"): filt = filt[filt["bank_name"] == bank_f]
    if stat_f not in (T("all"),"All"): filt = filt[filt["supply_status"] == stat_f]

    st.markdown(f"**{len(filt)} {T('results')}**")

    if filt.empty:
        st.warning(T("no_items"))
    elif is_host:
        disp = filt[["bank_name","item_name","quantity","days_left","avg_daily_demand","supply_status"]].copy()
        disp.columns = ["Food Bank","Item","Qty","Days Left","Daily Demand","Status"]
        st.dataframe(disp, use_container_width=True, hide_index=True)
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
                  <div style="font-weight:700;font-size:.98rem;">{row['item_name']}</div>
                  <div style="font-size:.8rem;color:#5a7090;margin-top:3px;">📍 {row['bank_name']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {pcls}">{row['supply_status']}</span>
                  <div style="font-size:.72rem;color:#5a7090;margin-top:4px;">{av}</div>
                </div>
              </div>
              <div style="font-size:.75rem;color:{slot_color};margin-top:8px;">🎟️ {left} {T('slots_left')}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ MY CHECK-IN PAGE █████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "my_checkin":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('my_checkin')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">Register, manage your visit, and check in when you arrive</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.show_reg_form and not st.session_state.registered_bank:
        target_bank = st.session_state.reg_target_bank
        if st.button(T("back_to_list"), key="reg_form_back"):
            st.session_state.show_reg_form = False; st.session_state.reg_target_bank = None; st.rerun()
        submitted, profile = render_registration_form(target_bank)
        if submitted and profile:
            code, fam_size = register_user(target_bank, profile)
            st.session_state.registered_bank = target_bank; st.session_state.user_code = code
            st.session_state.family_size = fam_size; st.session_state.user_name = profile["first_name"]
            st.session_state.checked_in = False; st.session_state.show_reg_form = False
            st.session_state.reg_target_bank = None; st.rerun()

    elif not st.session_state.registered_bank:
        st.info(T("not_registered"))
        section_header(T("choose_bank"))
        for bank in BANKS:
            left, cap, pct, color, badge = slots_bar_html(bank)
            with st.expander(f"🏪  {bank}   ·   {badge}   ·   {left} {T('slots_left')}"):
                items = df[df["bank_name"] == bank]
                cats  = " · ".join(items["item_name"].tolist()[:5])
                st.markdown(f"**{T('available')}:** {cats}")
                st.markdown(f"""<div style="font-size:.72rem;color:#5a7090;margin-top:6px;">{left} {T('of')} {cap} {T('slots_remaining')}</div>
                <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>""", unsafe_allow_html=True)
                st.markdown("")
                if left > 0:
                    if st.button(f"{T('register_at')} {bank}", key=f"ci_p_reg_{bank}", use_container_width=True):
                        st.session_state.show_reg_form = True; st.session_state.reg_target_bank = bank; st.rerun()
                else:
                    st.error(T("no_slots"))

    else:
        bank = st.session_state.registered_bank
        code = st.session_state.user_code
        fam  = st.session_state.family_size
        regs = load_registrations()
        profile = regs.get(code, {})
        full_name = " ".join(filter(None,[profile.get("first_name",""),profile.get("middle_name",""),profile.get("last_name","")])) or "—"

        st.markdown(f"""
        <div class="lc-card">
          <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.2rem;margin-bottom:4px;">{T('your_registration')}</div>
          <div style="color:#5a7090;font-size:.83rem;margin-bottom:20px;">{T('show_code')}</div>
          <div style="display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start;">
            <div><div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:#5a7090;">{T('name')}</div><div style="font-weight:700;margin-top:3px;">{full_name}</div></div>
            <div><div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:#5a7090;">{T('food_bank')}</div><div style="font-weight:700;margin-top:3px;">{bank}</div></div>
            <div><div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:#5a7090;">{T('confirmation_code')}</div><div class="code-box">{code}</div></div>
            <div><div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:#5a7090;">{T('household')}</div><div style="font-weight:700;margin-top:3px;">{fam} {T('people')}</div></div>
            <div><div style="font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:#5a7090;">{T('your_status')}</div>
              <div style="font-weight:700;margin-top:3px;color:#00e5c0;">{'✅ ' + T('checked_in_here') if st.session_state.checked_in else '📋 ' + T('not_arrived')}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        section_header(T("your_actions"))
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{T('check_in')}**")
            st.caption(T("press_arrive"))
            st.markdown("")
            if not st.session_state.checked_in:
                if st.button(T("ive_arrived"), use_container_width=True, key="ci_page_ci"):
                    if checkin_user(code):
                        st.session_state.checked_in = True
                        st.success(T("checked_in_success")); st.rerun()
            else:
                st.success(T("youre_checked_in_desk"))
        with col2:
            st.markdown(f"**{T('leave_queue_label')}**")
            st.caption(T("changed_plans"))
            st.markdown("")
            if st.session_state.checked_in:
                st.markdown(f"""<div style="padding:12px 16px;background:#ff4d6d0d;border:1px solid #ff4d6d33;border-radius:10px;font-size:.83rem;color:#ff4d6d;">{T('already_checked_in')}</div>""", unsafe_allow_html=True)
            else:
                if st.button(T("leave_cancel"), use_container_width=True, key="ci_page_dr"):
                    deregister_user(code)
                    st.session_state.registered_bank = None; st.session_state.user_code = None
                    st.session_state.checked_in = False
                    st.warning(T("slot_released")); st.rerun()

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        section_header(T("your_profile"))
        field_map = [
            (T("consent"), profile.get("consent","—")),
            (T("birth_year"), profile.get("birth_year","—")),
            (T("client_id"), profile.get("client_id") or T("new_client")),
            (T("phone"), profile.get("phone","—")),
            (T("can_text"), profile.get("can_text","—")),
            (T("address"), profile.get("address","—")),
            (T("city"), profile.get("city","—")),
            (T("zip_code"), profile.get("zip_code","—")),
            (T("children_018"), profile.get("children","—")),
            (T("adults_1959"), profile.get("adults","—")),
            (T("seniors_60"), profile.get("seniors","—")),
            (T("race_ethnicity"), profile.get("race_ethnicity","—")),
        ]
        col_a, col_b = st.columns(2)
        for i, (label, val) in enumerate(field_map):
            with (col_a if i % 2 == 0 else col_b):
                st.markdown(f"""<div style="padding:9px 0;border-bottom:1px solid #243048;">
                  <span style="font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:#5a7090;">{label}</span><br>
                  <span style="font-weight:600;">{val}</span></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='lc-divider'>", unsafe_allow_html=True)
        section_header(f"{T('whats_at')} {bank} {T('today')}")
        bank_items = df[df["bank_name"] == bank]
        for _, row in bank_items.iterrows():
            s    = row["supply_status"].lower()
            pcls = "pill-ok" if "ok" in s else "pill-low" if "low" in s else "pill-crit"
            av   = avail_label(row["days_left"])
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #243048;">
              <span style="font-weight:500;">{row['item_name']}</span>
              <span><span class="pill {pcls}" style="margin-right:8px;">{row['supply_status']}</span>
              <span style="font-size:.72rem;color:#5a7090;">{av}</span></span></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ DASHBOARD ████████████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "dashboard":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('dashboard')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">{T('live_ops')}</div>
    </div>""", unsafe_allow_html=True)

    regs   = load_registrations()
    t      = today()
    t_regs = [v for v in regs.values() if v.get("date") == t]
    total_r  = len([v for v in t_regs if v["status"] in ("registered","checked_in")])
    total_ci = len([v for v in t_regs if v["status"] == "checked_in"])
    total_sv = len([v for v in t_regs if v["status"] == "served"])
    total_cx = len([v for v in t_regs if v["status"] == "cancelled"])
    ppl_sv   = sum(v.get("family_size",1) for v in t_regs if v["status"] == "served")
    expiring = len(df[df["days_left"] <= 7])

    # KPI row
    kpi_cols = st.columns(6)
    for col, icon, lbl, val in [
        (kpi_cols[0],"📋",T("registered_label"),total_r),
        (kpi_cols[1],"✅","Checked In",total_ci),
        (kpi_cols[2],"🤝","Served",total_sv),
        (kpi_cols[3],"👥",T("people_served"),ppl_sv),
        (kpi_cols[4],"❌",T("cancelled"),total_cx),
        (kpi_cols[5],"⚠️",T("expiring"),expiring),
    ]:
        col.markdown(f"""<div class="lc-metric-card">
          <div class="lc-metric-icon">{icon}</div>
          <div class="lc-metric-label">{lbl}</div>
          <div class="lc-metric-val">{val}</div>
        </div>""", unsafe_allow_html=True)

    section_header(T("per_bank_snapshot"))
    cols2 = st.columns(2)
    for i, bank in enumerate(BANKS):
        b_r  = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="registered"])
        b_ci = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="checked_in"])
        b_sv = len([v for v in t_regs if v.get("bank")==bank and v["status"]=="served"])
        left, cap, pct, color, badge = slots_bar_html(bank)
        with cols2[i % 2]:
            st.markdown(f"""<div class="lc-card">
              <div style="font-family:'Playfair Display',serif;font-weight:700;">{bank}</div>
              <div style="display:flex;gap:14px;margin:8px 0;font-size:.8rem;">
                <span><b style="color:#a78bfa">{b_r}</b> reg</span>
                <span><b style="color:#00e5c0">{b_ci}</b> here</span>
                <span><b style="color:#ff8c42">{b_sv}</b> served</span>
              </div>
              <div style="font-size:.7rem;color:#5a7090;">{left}/{cap} left · {badge}</div>
              <div class="slots-bar-wrap"><div class="slots-bar" style="width:{pct}%;"></div></div>
            </div>""", unsafe_allow_html=True)

    dark = st.session_state.dark_mode
    cl   = chart_layout(dark)
    section_header(T("analytics"))

    # Row 1: Supply vs Demand + Pie
    ca, cb = st.columns(2)
    with ca:
        grp = df.groupby("bank_name").agg(
            Supply=("quantity","sum"),
            Demand=("avg_daily_demand", lambda x: x.sum()*7),
        ).reset_index()
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name="Supply",x=grp["bank_name"],y=grp["Supply"],
                              marker_color="#00e5c0",marker_line_width=0))
        fig1.add_trace(go.Bar(name="7-Day Demand",x=grp["bank_name"],y=grp["Demand"],
                              marker_color="#ff8c42",marker_line_width=0))
        fig1.update_layout(**cl, barmode="group", title=dict(text=T("supply_weekly"),font=dict(size=14)),
                           legend=dict(orientation="h",y=-0.35))
        fig1.update_xaxes(tickangle=-30)
        st.plotly_chart(fig1, use_container_width=True)

    with cb:
        sc = df["supply_status"].value_counts().reset_index()
        sc.columns = ["Status","Count"]
        fig2 = px.pie(sc, names="Status", values="Count", hole=0.58,
                      color="Status", color_discrete_map={"OK":"#00e5c0","Low":"#ff8c42","Critical":"#ff4d6d"},
                      title=T("inventory_status"))
        fig2.update_traces(textfont_size=12, marker=dict(line=dict(color="#080c12",width=2)))
        fig2.update_layout(**{k:v for k,v in cl.items() if k in ("paper_bgcolor","font","margin")},
                           title=dict(text=T("inventory_status"),font=dict(size=14)))
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Days expiry histogram + Scatter bubble
    cc, cd = st.columns(2)
    with cc:
        fig3 = px.histogram(df, x="days_left", nbins=15, title=T("days_expiry"),
                            color_discrete_sequence=["#a78bfa"], labels={"days_left":"Days Left"})
        fig3.update_layout(**cl, bargap=0.08, title=dict(text=T("days_expiry"),font=dict(size=14)))
        st.plotly_chart(fig3, use_container_width=True)

    with cd:
        # Bubble: quantity vs demand colored by status
        color_map = {"OK":"#00e5c0","Low":"#ff8c42","Critical":"#ff4d6d"}
        fig4 = go.Figure()
        for status, grp in df.groupby("supply_status"):
            fig4.add_trace(go.Scatter(
                x=grp["avg_daily_demand"], y=grp["quantity"],
                mode="markers",
                name=status,
                marker=dict(
                    size=grp["days_left"].clip(upper=30) * 1.5,
                    color=color_map.get(status, "#38bdf8"),
                    opacity=0.75,
                    line=dict(width=1, color="#080c12"),
                ),
                text=grp["item_name"] + " @ " + grp["bank_name"],
                hovertemplate="%{text}<br>Daily demand: %{x}<br>Quantity: %{y}<extra></extra>",
            ))
        fig4.update_layout(**cl, title=dict(text="Quantity vs Daily Demand",font=dict(size=14)),
                           xaxis_title="Daily Demand", yaxis_title="Quantity",
                           legend=dict(orientation="h",y=-0.3))
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: Bank heatmap
    section_header("📊 Inventory Heatmap by Bank")
    pivot = df.pivot_table(index="bank_name", columns="item_name", values="days_left", aggfunc="min")
    fig5  = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,"#ff4d6d"],[0.3,"#ff8c42"],[0.7,"#38bdf8"],[1,"#00e5c0"]],
        text=pivot.values.round(0), texttemplate="%{text}d",
        hoverongaps=False,
    ))
    bg_c = "#080c12" if dark else "#ffffff"
    fc   = "#e2eaf5" if dark else "#0a1628"
    fig5.update_layout(paper_bgcolor=bg_c, font=dict(family="Space Grotesk",color=fc),
                       margin=dict(t=20,b=80,l=120,r=20), height=340,
                       xaxis=dict(tickangle=-30))
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ MANAGE PAGE ██████████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "manage":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('manage')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">{T('manage_desc')}</div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([T("live_queue"), T("capacity"), T("full_log")])

    with tab1:
        st.markdown(f"#### {T('mark_served_label')}")
        sel_bank = st.selectbox(T("food_bank"), BANKS, key="mgmt_bank")
        regs = load_registrations()
        t    = today()
        active = {k: v for k, v in regs.items()
                  if v.get("bank") == sel_bank and v.get("date") == t
                  and v["status"] in ("registered","checked_in")}

        if not active:
            st.info(f"{T('no_active_regs')} {sel_bank}.")
        else:
            for code, info in active.items():
                status = info["status"]
                pcls   = "pill-ci" if status == "checked_in" else "pill-reg"
                slbl   = T("checked_in") if status == "checked_in" else T("registered")
                col_i, col_a = st.columns([3,1])
                with col_i:
                    st.markdown(f"""<div style="padding:12px 0;border-bottom:1px solid #243048;">
                      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                        <code style="font-family:'DM Mono',monospace;color:#00e5c0;font-size:.9rem;">{code}</code>
                        <span class="pill {pcls}">{slbl}</span>
                        <span style="font-size:.78rem;color:#5a7090;">
                          {info.get('name','Anon')} · {info.get('family_size',1)} {T('people')}
                          · {info.get('registered_at','—')}
                          {' · ' + info['checked_in_at'] if info.get('checked_in_at') else ''}
                        </span>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with col_a:
                    if st.button(T("served_btn"), key=f"srv_{code}", use_container_width=True):
                        mark_served(code)
                        st.success(f"{code} {T('marked_served')}"); st.rerun()

    with tab2:
        st.markdown(f"#### {T('daily_capacity')}")
        st.caption(T("max_families"))
        cap_data = load_capacity()
        new_caps = {}
        cols = st.columns(2)
        for i, bank in enumerate(BANKS):
            with cols[i % 2]:
                new_caps[bank] = st.number_input(bank, min_value=10, max_value=500,
                                                  value=cap_data.get(bank,50), step=5, key=f"cap_{bank}")
        if st.button(T("save_capacity"), use_container_width=True):
            save_capacity(new_caps); st.success(T("capacity_updated"))

    with tab3:
        st.markdown(f"#### {T('todays_log')}")
        regs = load_registrations()
        t    = today()
        rows = []
        for code, v in regs.items():
            if v.get("date") == t:
                rows.append({
                    "Code": code, "First Name": v.get("first_name","—"),
                    "Last Name": v.get("last_name","—"), "Client ID": v.get("client_id") or "New",
                    "Bank": v.get("bank","—"), "Status": v.get("status","—"),
                    "Household": v.get("family_size",1), "Children": v.get("children","—"),
                    "Adults": v.get("adults","—"), "Seniors": v.get("seniors","—"),
                    "Phone": v.get("phone","—"), "Can Text": v.get("can_text","—"),
                    "City": v.get("city","—"), "Zip": v.get("zip_code","—"),
                    "Race/Ethnicity": v.get("race_ethnicity","—"), "Consent": v.get("consent","—"),
                    "Registered": v.get("registered_at","—"), "Checked In": v.get("checked_in_at","—"),
                    "Served": v.get("served_at","—"),
                })
        if rows:
            log_df = pd.DataFrame(rows)
            st.dataframe(log_df, use_container_width=True, hide_index=True)
            st.download_button(T("download_csv"), log_df.to_csv(index=False),
                               file_name=f"checkins_{t}.csv", mime="text/csv")
        else:
            st.info(T("no_regs_today"))

# ══════════════════════════════════════════════════════════════════════════════
# ██████████ AI INSIGHTS PAGE █████████████████████████████████████████████████
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ai_insights":
    st.markdown(f"""<div style="padding:8px 0 20px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:800;">{T('ai_insights_title')}</div>
      <div style="color:#5a7090;font-size:.88rem;margin-top:4px;">{T('ai_insights_desc')}</div>
    </div>""", unsafe_allow_html=True)

    dark = st.session_state.dark_mode
    cl   = chart_layout(dark)

    # ── AI KPI Dashboard ──────────────────────────────────────────────────────
    section_header(T("ai_dashboard"))
    kpis = compute_network_kpis(df)

    k1, k2, k3, k4 = st.columns(4)
    def kpi_card(col, label, val, unit="", color="#00e5c0"):
        col.markdown(f"""<div class="kpi-card">
          <div class="kpi-val" style="background:linear-gradient(135deg,{color},{color}99);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            {val}{unit}
          </div>
          <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    kpi_card(k1, T("network_health"),   kpis["health"],    "%", "#00e5c0")
    kpi_card(k2, T("waste_risk"),       kpis["waste_risk"],"%", "#ff4d6d")
    kpi_card(k3, T("coverage_rate"),    kpis["coverage"],  "%", "#38bdf8")
    kpi_card(k4, T("efficiency"),       kpis["efficiency"],"%", "#a78bfa")

    # Gauge chart for network health
    st.markdown("<br>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=kpis["health"],
        delta={"reference": 75, "increasing": {"color": "#00e5c0"}, "decreasing": {"color": "#ff4d6d"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#5a7090"},
            "bar": {"color": "#00e5c0"},
            "steps": [
                {"range": [0, 40],  "color": "rgba(255,77,109,0.13)"},
                {"range": [40, 70], "color": "rgba(255,140,66,0.13)"},
                {"range": [70, 100],"color": "rgba(0,229,192,0.13)"},
            ],
            "threshold": {"line": {"color": "#a78bfa", "width": 3}, "thickness": 0.8, "value": 85},
        },
        title={"text": T("network_health"), "font": {"size": 14, "color": "#5a7090"}},
        number={"suffix": "%", "font": {"size": 32}},
    ))
    bg_c = "#080c12" if dark else "#ffffff"
    fc   = "#e2eaf5" if dark else "#0a1628"
    fig_gauge.update_layout(paper_bgcolor=bg_c, font=dict(family="Space Grotesk",color=fc),
                             margin=dict(t=60,b=20,l=60,r=60), height=280)
    st.plotly_chart(fig_gauge, use_container_width=True)

    # ── Tab layout for AI features ────────────────────────────────────────────
    ai_tab1, ai_tab2, ai_tab3 = st.tabs([T("expiry_risk"), T("redistribution"), T("demand_forecast")])

    # ── EXPIRY RISK ───────────────────────────────────────────────────────────
    with ai_tab1:
        st.markdown(f"#### {T('expiry_risk')}")
        st.caption("Items ranked by expiration risk. Prioritize redistribution or use of critical items.")

        risk_df = compute_expiry_risk(df)
        critical = risk_df[risk_df["risk_level"] == "Critical"]
        high     = risk_df[risk_df["risk_level"] == "High"]
        moderate = risk_df[risk_df["risk_level"] == "Moderate"]

        col_r1, col_r2 = st.columns([1,2])
        with col_r1:
            for label, cnt, color in [
                (T("critical_risk"), len(critical), "#ff4d6d"),
                (T("high_risk"),     len(high),     "#ff8c42"),
                (T("moderate_risk"), len(moderate), "#38bdf8"),
            ]:
                st.markdown(f"""<div style="background:{color}0a;border:1px solid {color}44;border-radius:12px;
                  padding:16px 20px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;">
                  <span style="font-weight:600;">{label}</span>
                  <span style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:800;color:{color};">{cnt}</span>
                </div>""", unsafe_allow_html=True)

        with col_r2:
            # Risk timeline chart
            risk_plot = risk_df[risk_df["days_left"] <= 21].copy()
            color_map = {"Critical":"#ff4d6d","High":"#ff8c42","Moderate":"#38bdf8","Low":"#00e5c0"}
            fig_risk = go.Figure()
            for level, grp in risk_plot.groupby("risk_level"):
                fig_risk.add_trace(go.Scatter(
                    x=grp["days_left"], y=grp["quantity"],
                    mode="markers",
                    name=str(level),
                    marker=dict(size=10, color=color_map.get(str(level),"#5a7090"),
                                line=dict(width=1,color="#080c12")),
                    text=grp["item_name"] + " @ " + grp["bank_name"],
                    hovertemplate="%{text}<br>%{x} days · %{y} units<extra></extra>",
                ))
            fig_risk.update_layout(**cl, title=dict(text="Risk Scatter: Days Left vs Quantity",font=dict(size=13)),
                                   xaxis_title="Days Until Expiry", yaxis_title="Quantity in Stock",
                                   legend=dict(orientation="h",y=-0.3))
            st.plotly_chart(fig_risk, use_container_width=True)

        # Critical items list
        if not critical.empty:
            st.markdown(f"##### 🔴 {T('critical_risk')} Items")
            for _, row in critical.iterrows():
                st.markdown(f"""<div class="risk-critical">
                  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                      <span style="font-weight:700;">{row['item_name']}</span>
                      <span style="font-size:.78rem;color:#5a7090;margin-left:10px;">@ {row['bank_name']}</span>
                    </div>
                    <div style="text-align:right;">
                      <span class="pill pill-crit">{row['days_left']} {T('days_remaining')}</span>
                      <div style="font-size:.72rem;color:#5a7090;margin-top:3px;">{int(row['quantity'])} units · {row['avg_daily_demand']}/day demand</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

        if not high.empty:
            st.markdown(f"##### 🟠 {T('high_risk')} Items")
            for _, row in high.head(6).iterrows():
                st.markdown(f"""<div class="risk-high">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><span style="font-weight:600;">{row['item_name']}</span>
                    <span style="font-size:.76rem;color:#5a7090;margin-left:8px;">@ {row['bank_name']}</span></div>
                    <span class="pill pill-low">{row['days_left']} {T('days_remaining')}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── REDISTRIBUTION ────────────────────────────────────────────────────────
    with ai_tab2:
        st.markdown(f"#### {T('redistribution')}")
        st.caption("AI-detected surplus-shortage pairs across banks. Act on urgent recommendations first.")

        recs = compute_redistribution(df)

        if not recs:
            st.success("✅ No redistribution needed — supply is well-balanced across the network.")
        else:
            urgent   = [r for r in recs if "Urgent" in r["urgency"]]
            rec_only = [r for r in recs if "Recommended" in r["urgency"]]

            if urgent:
                st.markdown(f"##### 🔴 Urgent ({len(urgent)})")
                for r in urgent:
                    st.markdown(f"""<div class="redist-card" style="border-left-color:#ff4d6d;">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                        <div>
                          <div style="font-weight:700;font-size:1rem;">{r['item']}</div>
                          <div style="font-size:.8rem;color:#5a7090;margin-top:4px;">
                            📤 {T('surplus_at')}: <b style="color:#e2eaf5;">{r['from_bank']}</b> ({r['from_qty']} units)<br>
                            📥 {T('shortage_at')}: <b style="color:#ff4d6d;">{r['to_bank']}</b> ({r['to_days']} days left)
                          </div>
                        </div>
                        <div style="text-align:right;">
                          <span class="pill pill-crit">{r['urgency']}</span>
                          <div style="font-size:.82rem;font-weight:700;margin-top:6px;color:#00e5c0;">
                            → Transfer ~{r['transfer_qty']} {T('units')}
                          </div>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            if rec_only:
                st.markdown(f"##### 🟡 Recommended ({len(rec_only)})")
                for r in rec_only:
                    st.markdown(f"""<div class="redist-card">
                      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                          <span style="font-weight:600;">{r['item']}</span>
                          <span style="font-size:.76rem;color:#5a7090;margin-left:8px;">{r['from_bank']} → {r['to_bank']}</span>
                        </div>
                        <div>
                          <span class="pill pill-low">{r['urgency']}</span>
                          <span style="font-size:.8rem;color:#00e5c0;margin-left:8px;">~{r['transfer_qty']} {T('units')}</span>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            # Sankey diagram
            if len(recs) >= 2:
                st.markdown("##### 🔄 Flow Diagram")
                all_nodes  = list(set([r["from_bank"] for r in recs] + [r["to_bank"] for r in recs]))
                node_idx   = {n: i for i, n in enumerate(all_nodes)}
                src_idx    = [node_idx[r["from_bank"]] for r in recs]
                tgt_idx    = [node_idx[r["to_bank"]]   for r in recs]
                values     = [r["transfer_qty"]         for r in recs]
                labels_san = [r["item"]                 for r in recs]

                bg_c = "#080c12" if dark else "#ffffff"
                fc   = "#e2eaf5" if dark else "#0a1628"
                fig_sankey = go.Figure(go.Sankey(
                    node=dict(
                        label=all_nodes,
                        color=["#00e5c0" if n in [r["from_bank"] for r in recs] else "#ff8c42" for n in all_nodes],
                        pad=15, thickness=18,
                    ),
                    link=dict(source=src_idx, target=tgt_idx, value=values,
                              label=labels_san, color="rgba(0,229,192,0.25)"),
                ))
                fig_sankey.update_layout(paper_bgcolor=bg_c, font=dict(family="Space Grotesk",color=fc),
                                         margin=dict(t=20,b=20,l=20,r=20), height=340)
                st.plotly_chart(fig_sankey, use_container_width=True)

    # ── DEMAND FORECAST ───────────────────────────────────────────────────────
    with ai_tab3:
        st.markdown(f"#### {T('demand_forecast')}")
        st.caption("7-day demand simulation per bank. Items flagged in red are predicted to run short.")

        sel_bank_fc = st.selectbox("Select Bank", BANKS, key="fc_bank")
        fc_days     = st.slider("Forecast horizon (days)", 7, 30, 7, key="fc_days")

        bank_df = df[df["bank_name"] == sel_bank_fc].copy()
        forecasts = compute_demand_forecast(bank_df, days=fc_days)

        # Summary flags
        short_items = [f for f in forecasts if f["will_run_short"]]
        ok_items    = [f for f in forecasts if not f["will_run_short"]]

        flag_cols = st.columns(2)
        with flag_cols[0]:
            st.markdown(f"""<div style="background:#ff4d6d0a;border:1px solid #ff4d6d44;border-radius:12px;
              padding:16px 20px;text-align:center;">
              <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;color:#ff4d6d;">{len(short_items)}</div>
              <div style="font-size:.72rem;color:#5a7090;text-transform:uppercase;letter-spacing:.08em;">Items predicted to run short</div>
            </div>""", unsafe_allow_html=True)
        with flag_cols[1]:
            st.markdown(f"""<div style="background:#00e5c00a;border:1px solid #00e5c044;border-radius:12px;
              padding:16px 20px;text-align:center;">
              <div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;color:#00e5c0;">{len(ok_items)}</div>
              <div style="font-size:.72rem;color:#5a7090;text-transform:uppercase;letter-spacing:.08em;">Items with sufficient stock</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Line chart: daily forecast per item
        fig_fc = go.Figure()
        days_x = [f"Day {i+1}" for i in range(fc_days)]
        colors = ["#00e5c0","#38bdf8","#a78bfa","#ff8c42","#ff4d6d","#f472b6","#facc15"]

        for idx, fc in enumerate(forecasts):
            color = "#ff4d6d" if fc["will_run_short"] else colors[idx % len(colors)]
            fig_fc.add_trace(go.Scatter(
                x=days_x, y=fc["daily_forecasts"],
                name=fc["item"],
                mode="lines+markers",
                line=dict(color=color, width=2),
                marker=dict(size=5),
                hovertemplate=f"<b>{fc['item']}</b><br>%{{x}}: %{{y:.0f}} units<extra></extra>",
            ))

        fig_fc.update_layout(**cl, title=dict(text=f"{T('forecast_7')} — {sel_bank_fc}", font=dict(size=13)),
                             legend=dict(orientation="h", y=-0.4, xanchor="left"),
                             yaxis_title="Projected Daily Demand")
        st.plotly_chart(fig_fc, use_container_width=True)

        # Bar chart: total forecast vs current stock
        items_names = [f["item"] for f in forecasts]
        total_fc    = [f["total_7d"] for f in forecasts]
        current     = [f["current_qty"] for f in forecasts]
        bar_colors  = ["#ff4d6d" if f["will_run_short"] else "#00e5c0" for f in forecasts]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Current Stock", x=items_names, y=current,
                                 marker_color="#a78bfa", marker_line_width=0))
        fig_bar.add_trace(go.Bar(name=f"{fc_days}-Day Forecast", x=items_names, y=total_fc,
                                 marker_color=bar_colors, marker_line_width=0, opacity=0.8))
        fig_bar.update_layout(**cl, barmode="group",
                              title=dict(text=f"Stock vs {fc_days}-Day Projected Demand",font=dict(size=13)),
                              legend=dict(orientation="h",y=-0.35))
        fig_bar.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Item-level table
        if short_items:
            st.markdown("##### ⚠️ Items to Watch")
            for fc in short_items:
                shortage = fc["total_7d"] - fc["current_qty"]
                st.markdown(f"""<div class="risk-critical">
                  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                      <span style="font-weight:700;">{fc['item']}</span>
                      <span style="font-size:.76rem;color:#5a7090;margin-left:8px;">@ {fc['bank']}</span>
                    </div>
                    <div style="text-align:right;font-size:.8rem;">
                      <div>Current: <b style="color:#e2eaf5;">{fc['current_qty']} units</b></div>
                      <div>Forecast need: <b style="color:#ff8c42;">{fc['total_7d']:.0f} units</b></div>
                      <div>Predicted shortage: <b style="color:#ff4d6d;">{shortage:.0f} units</b></div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
