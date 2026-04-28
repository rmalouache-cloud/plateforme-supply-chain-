import streamlit as st
import os
import subprocess
import sys

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
        cursor: pointer;
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
if 'tool_file' not in st.session_state:
    st.session_state.tool_file = None

# ==================== FONCTIONS ====================

def go_home():
    st.session_state.page = 'home'
    st.session_state.selected_tool = None
    st.session_state.tool_file = None
    st.rerun()

def load_tool(tool_name, folder, filename):
    """Charge un outil depuis son dossier"""
    # Construire le chemin complet
    file_path = os.path.join(folder, filename)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            # Exécuter le code
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
    # En-tête avec logo
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
    
    # Présentation
    st.markdown("""
    <div class="about-section">
        <h3>🎯 A propos</h3>
        <p>Cette plateforme centralise tous vos outils de verification fournisseur :</p>
        <ul>
            <li>📊 <strong>Container Dashboard</strong> - Tableau de bord des indicateurs et KPIs</li>
            <li>📦 <strong>Comparateur BOM vs Packing</strong> - Verification des quantites entre BOM et packing list</li>
            <li>🔄 <strong>Comparateur BOM vs BOM</strong> - Analyse et comparaison des versions BOM</li>
            <li>📍 <strong>Check Position</strong> - Verification des positions et emplacements</li>
            <li>✅ <strong>Checking Reply</strong> - Verification et analyse des reponses fournisseur</li>
            <li>📐 <strong>Box Calculator</strong> - Calcul du nombre de cartons selon le type d article</li>
        </ul>
        <p>Selectionnez l'outil ci-dessous pour commencer.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center; margin-bottom: 1.5rem;">📌 Outils disponibles</h2>', unsafe_allow_html=True)
    
    # Liste des outils avec les bons chemins
    tools = [
        {"name": "Container Dashboard", "icon": "📊", "desc": "Tableau de bord des KPIs fournisseur", "folder": "container-dashboard", "file": "code.py"},
        {"name": "Comparateur BOM vs Packing", "icon": "📦", "desc": "Verification des quantites BOM / Packing list", "folder": "comparator-bom_packing", "file": "app.py"},
        {"name": "Comparateur BOM vs BOM", "icon": "🔄", "desc": "Analyse et comparaison des versions BOM", "folder": "comparator-bom_bom", "file": "bom_old and new.py"},
        {"name": "Check Position", "icon": "📍", "desc": "Verification des positions et emplacements", "folder": "check_position", "file": "code.py"},
        {"name": "Checking Reply", "icon": "✅", "desc": "Verification et analyse des reponses fournisseur", "folder": "checking-reply", "file": "checke replay.py"},
        {"name": "Box Calculator", "icon": "📐", "desc": "Calcul du nombre de cartons", "folder": "Box-calculator", "file": "app.py"}
    ]
    
    # Affichage en grille (2 lignes de 3 colonnes)
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
                        st.session_state.selected_tool = tool['name']
                        st.session_state.tool_folder = tool['folder']
                        st.session_state.tool_file = tool['file']
                        st.rerun()
    
    # Pied de page
    st.markdown("""
    <div class="footer">
        <p>© 2024 - Suite Outils Fournisseur | Version 2.0</p>
        <p>Developpe pour les equipes ingenierie</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== CHARGEMENT DES OUTILS ====================

def show_tool():
    # Bouton retour
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Retour a l'accueil", use_container_width=True):
            go_home()
    
    # En-tete
    st.markdown(f"""
    <div class="tool-header">
        <h2>🛠️ {st.session_state.selected_tool}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement
    with st.spinner(f"Chargement de {st.session_state.selected_tool}..."):
        success = load_tool(
            st.session_state.selected_tool,
            st.session_state.tool_folder,
            st.session_state.tool_file
        )
        
        if not success:
            st.error(f"Impossible de charger {st.session_state.selected_tool}")
            st.info(f"""
            **Verifiez que la structure est correcte :**
            
