import streamlit as st
import os
import sys
import subprocess

# Configuration
st.set_page_config(
    page_title="Suite Outils Fournisseur",
    page_icon="🏭",
    layout="wide"
)

# ==================== INSTALLATION DES MODULES MANQUANTS ====================
def install_missing_modules():
    """Installe les modules manquants"""
    modules_necessaires = ['fpdf', 'pandas', 'openpyxl', 'numpy']
    modules_installed = []
    
    for module in modules_necessaires:
        try:
            __import__(module)
        except ImportError:
            modules_installed.append(module)
            st.warning(f"Installation de {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    
    if modules_installed:
        st.success(f"Modules installes: {', '.join(modules_installed)}")
        st.rerun()

# Installer les modules manquants
install_missing_modules()

# ==================== CSS ====================
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .hero h1 { font-size: 2rem; margin-bottom: 0.5rem; }
    .hero p { font-size: 1rem; opacity: 0.9; }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin-bottom: 1rem;
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        border-color: #2a5298;
    }
    .feature-icon { font-size: 3rem; margin-bottom: 1rem; }
    .feature-title { font-size: 1.1rem; font-weight: 600; color: #1e3c72; margin-bottom: 0.5rem; }
    .feature-desc { font-size: 0.8rem; color: #666; }
    .footer { text-align: center; padding: 1.5rem; margin-top: 2rem; border-top: 1px solid #e0e0e0; color: #666; }
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    .tool-header {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    .tool-header h2 { margin: 0; color: #1e3c72; font-size: 1.3rem; }
    .about-section {
        background: #e8f0fe;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: #1a1a2e;
        border: 1px solid #c5d5e8;
    }
    .about-section h3 { color: #1e3c72; margin-top: 0; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ==================== FONCTIONS ====================

def go_home():
    st.session_state.page = 'home'
    st.rerun()

def load_tool(folder, filename):
    """Charge un outil depuis son dossier avec gestion des erreurs"""
    file_path = os.path.join(folder, filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(code, globals())
            return True
        except Exception as e:
            st.error(f"Erreur: {str(e)}")
            st.info("Module manquant ? Contactez l'administrateur.")
            return False
    else:
        st.error(f"Fichier non trouve: {file_path}")
        return False

# ==================== PAGE D'ACCUEIL ====================

def show_home():
    # En-tete
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("logo.jfif", width=80)
        except:
            st.markdown("<h1 style='font-size: 3rem;'>🏭</h1>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="hero">
            <h1>Suite Outils Fournisseur</h1>
            <p>Plateforme integree pour la verification des documents d expedition</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-section">
        <h3>🎯 A propos</h3>
        <p>Cette plateforme centralise tous vos outils de verification fournisseur</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">📌 Outils disponibles</h2>', unsafe_allow_html=True)
    
    tools = [
        {"name": "Container Dashboard", "icon": "📊", "desc": "Tableau de bord", "folder": "container-dashboard", "file": "code.py"},
        {"name": "BOM vs Packing", "icon": "📦", "desc": "Comparaison BOM/Packing", "folder": "comparator-bom_packing", "file": "app.py"},
        {"name": "BOM vs BOM", "icon": "🔄", "desc": "Comparaison versions BOM", "folder": "comparator-bom_bom", "file": "bom_old and new.py"},
        {"name": "Check Position", "icon": "📍", "desc": "Verification positions", "folder": "check_position", "file": "code.py"},
        {"name": "Checking Reply", "icon": "✅", "desc": "Analyse reponses", "folder": "checking-reply", "file": "checke replay.py"},
        {"name": "Box Calculator", "icon": "📐", "desc": "Calcul cartons", "folder": "Box-calculator", "file": "app.py"}
    ]
    
    for i in range(0, len(tools), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(tools):
                tool = tools[idx]
                with cols[j]:
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{tool['icon']}</div>
                        <div class="feature-title">{tool['name']}</div>
                        <div class="feature-desc">{tool['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Lancer {tool['name']}", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.page = 'tool'
                        st.session_state.tool_folder = tool['folder']
                        st.session_state.tool_file = tool['file']
                        st.rerun()
    
    st.markdown('<div class="footer"><p>© 2024 - Suite Outils Fournisseur</p></div>', unsafe_allow_html=True)

# ==================== CHARGEMENT ====================

def show_tool():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Retour", use_container_width=True):
            go_home()
    
    st.markdown(f'<div class="tool-header"><h2>🛠️ Outil</h2></div>', unsafe_allow_html=True)
    
    with st.spinner("Chargement..."):
        success = load_tool(st.session_state.tool_folder, st.session_state.tool_file)
        if not success:
            st.error("Echec du chargement")

# ==================== ROUTAGE ====================

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'tool':
    show_tool()
