import streamlit as st
import sys
import os
import importlib.util

# Configuration
st.set_page_config(
    page_title="Suite Outils Fournisseur",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .hero p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        text-align: center;
        margin-bottom: 1rem;
        height: 100%;
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
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.85rem;
        color: #666;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #666;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
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

def load_tool_from_path(tool_path, tool_name):
    """Charge et exécute un fichier Python depuis un chemin"""
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(tool_path):
            st.error(f"Fichier non trouve: {tool_path}")
            return False
        
        # Lire et exécuter le fichier
        with open(tool_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Exécuter le code
        exec(code, globals())
        return True
        
    except Exception as e:
        st.error(f"Erreur lors du chargement de {tool_name}: {str(e)}")
        return False

# ==================== PAGE D'ACCUEIL ====================

def show_home():
    # En-tête
    st.markdown("""
    <div class="hero">
        <h1>🏭 Suite Outils Fournisseur</h1>
        <p>Plateforme intégrée pour la vérification et l'analyse des documents d'expédition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Présentation
    st.markdown("""
    <div style="background: #f0f4f8; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3>🎯 À propos</h3>
        <p>Cette plateforme centralise tous vos outils de vérification fournisseur :</p>
        <ul>
            <li>✅ Dashboard - Vue d'ensemble des indicateurs</li>
            <li>✅ Comparateur BOM vs Packing - Vérification des quantités</li>
            <li>✅ Comparateur BOM vs BOM - Analyse des versions</li>
            <li>✅ Check position - Vérification des positions</li>
            <li>✅ Checking reply - Analyse des réponses fournisseur</li>
        </ul>
        <p>Sélectionnez l'outil ci-dessous pour commencer.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>📌 Outils disponibles</h2>", unsafe_allow_html=True)
    
    # Définition des outils
    tools = [
        {
            "name": "Container Dashboard",
            "icon": "📊",
            "desc": "Tableau de bord des indicateurs et KPIs fournisseur",
            "path": "container-dashboard/app.py"
        },
        {
            "name": "Comparateur BOM vs Packing",
            "icon": "📦",
            "desc": "Verification des quantites entre BOM et packing list",
            "path": "comparator-bom_packing/app.py"
        },
        {
            "name": "Comparateur BOM vs BOM",
            "icon": "🔄",
            "desc": "Analyse et comparaison des versions BOM",
            "path": "comparator-bom_bom/app.py"
        },
        {
            "name": "Check Position",
            "icon": "📍",
            "desc": "Verification des positions et emplacements",
            "path": "check_position/app.py"
        },
        {
            "name": "Checking Reply",
            "icon": "✅",
            "desc": "Verification et analyse des reponses fournisseur",
            "path": "checking-reply/app.py"
        }
    ]
    
    # Affichage en grille
    for i in range(0, len(tools), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(tools):
                tool = tools[idx]
                with cols[j]:
                    # Carte
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{tool['icon']}</div>
                        <div class="feature-title">{tool['name']}</div>
                        <div class="feature-desc">{tool['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bouton
                    if st.button(f"Lancer {tool['name']}", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.page = 'tool'
                        st.session_state.selected_tool = tool['name']
                        st.session_state.tool_path = tool['path']
                        st.rerun()
    
    # Pied de page
    st.markdown("""
    <div class="footer">
        <p>© 2024 - Suite Outils Fournisseur | Version 2.0</p>
        <p>Développé pour les équipes ingénierie</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== CHARGEMENT DES OUTILS ====================

def show_tool(tool_name, tool_path):
    """Affiche l'outil sélectionné"""
    
    # Bouton retour
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("← Accueil", key="back_home"):
            go_home()
    
    # En-tête de l'outil
    st.markdown(f"""
    <div class="tool-header">
        <h2>🛠️ {tool_name}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement de l'outil
    with st.spinner(f"Chargement de {tool_name}..."):
        success = load_tool_from_path(tool_path, tool_name)
        
        if not success:
            st.error(f"Impossible de charger {tool_name}")
            st.markdown("""
            **Verifications :**
            1. Le dossier existe-t-il ?
            2. Contient-il un fichier app.py ?
            
            **Structure attendue :**
