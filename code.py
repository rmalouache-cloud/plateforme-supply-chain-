import streamlit as st
import os

# Configuration
st.set_page_config(
    page_title="Suite Outils Fournisseur",
    page_icon="🏭",
    layout="wide"
)

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
    .hero h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .hero p {
        font-size: 1rem;
        opacity: 0.9;
    }
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
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.8rem;
        color: #666;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #666;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30,60,114,0.3);
    }
    .tool-header {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    .tool-header h2 {
        margin: 0;
        color: #1e3c72;
        font-size: 1.3rem;
    }
    .about-section {
        background: #e8f0fe;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: #1a1a2e;
        border: 1px solid #c5d5e8;
    }
    .about-section h3 {
        color: #1e3c72;
        margin-top: 0;
    }
    .about-section ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    .about-section li {
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = None
if 'tool_path' not in st.session_state:
    st.session_state.tool_path = None

# ==================== FONCTIONS ====================

def go_home():
    st.session_state.page = 'home'
    st.session_state.selected_tool = None
    st.session_state.tool_path = None
    st.rerun()

def load_tool(tool_name, file_path):
    """Charge un outil depuis son chemin"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(code, globals())
            return True
        except Exception as e:
            st.error(f"Erreur d execution: {str(e)}")
            return False
    else:
        st.error(f"Fichier non trouve: {file_path}")
        return False

# ==================== PAGE D'ACCUEIL ====================

def show_home():
    st.markdown('<div class="hero"><h1>🏭 Suite Outils Fournisseur</h1><p>Plateforme integree pour la verification des documents d expedition</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-section">
        <h3>🎯 A propos</h3>
        <p>Cette plateforme centralise tous vos outils de verification fournisseur :</p>
        <ul>
            <li>📊 Container Dashboard - Tableau de bord des indicateurs</li>
            <li>📦 Comparateur BOM vs Packing - Verification des quantites</li>
            <li>🔄 Comparateur BOM vs BOM - Analyse des versions</li>
            <li>📍 Check Position - Verification des positions</li>
            <li>✅ Checking Reply - Analyse des reponses fournisseur</li>
            <li>📐 Box Calculator - Calcul du nombre de cartons</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center;">📌 Outils disponibles</h2>', unsafe_allow_html=True)
    
    # Definition des outils avec les bons chemins (dossier rmalouache-cloud)
    tools = [
        {"name": "Container Dashboard", "icon": "📊", "desc": "Tableau de bord des KPIs", "path": "../rmalouache-cloud/container-dashboard/code.py"},
        {"name": "Comparateur BOM vs Packing", "icon": "📦", "desc": "Verification des quantites BOM/Packing", "path": "../rmalouache-cloud/comparator-bom_packing/app.py"},
        {"name": "Comparateur BOM vs BOM", "icon": "🔄", "desc": "Analyse et comparaison des versions BOM", "path": "../rmalouache-cloud/comparator-bom_bom/bom_old and new.py"},
        {"name": "Check Position", "icon": "📍", "desc": "Verification des positions", "path": "../rmalouache-cloud/check_position/code.py"},
        {"name": "Checking Reply", "icon": "✅", "desc": "Analyse des reponses fournisseur", "path": "../rmalouache-cloud/checking-reply/checke replay.py"},
        {"name": "Box Calculator", "icon": "📐", "desc": "Calcul du nombre de cartons", "path": "../rmalouache-cloud/Box-calculator/app.py"}
    ]
    
    # Affichage en grille
    for i in range(0, len(tools), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(tools):
                tool = tools[idx]
                with cols[j]:
                    st.markdown(f'<div class="feature-card"><div class="feature-icon">{tool["icon"]}</div><div class="feature-title">{tool["name"]}</div><div class="feature-desc">{tool["desc"]}</div></div>', unsafe_allow_html=True)
                    if st.button(f"Lancer {tool['name']}", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.page = 'tool'
                        st.session_state.selected_tool = tool['name']
                        st.session_state.tool_path = tool['path']
                        st.rerun()
    
    # Pied de page
    st.markdown('<div class="footer"><p>© 2024 - Suite Outils Fournisseur | Version 2.0</p></div>', unsafe_allow_html=True)

# ==================== CHARGEMENT DES OUTILS ====================

def show_tool():
    # Bouton retour
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Retour a l accueil", key="back_home"):
            go_home()
    
    # En-tete
    st.markdown(f'<div class="tool-header"><h2>🛠️ {st.session_state.selected_tool}</h2></div>', unsafe_allow_html=True)
    
    # Chargement
    with st.spinner(f"Chargement de {st.session_state.selected_tool}..."):
        success = load_tool(st.session_state.selected_tool, st.session_state.tool_path)
        
        if not success:
            st.error(f"Impossible de charger {st.session_state.selected_tool}")
            st.info(f"Chemin recherche: {st.session_state.tool_path}")

# ==================== ROUTAGE PRINCIPAL ====================

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'tool':
    show_tool()
