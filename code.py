import streamlit as st
import sys
import os

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
        color: #1a1a2e;
    }
    .about-section li {
        color: #1a1a2e;
        margin: 0.5rem 0;
    }
    .about-section p {
        color: #1a1a2e;
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

def find_file_in_directory(directory, filename):
    """Recherche un fichier dans un dossier et ses sous-dossiers"""
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def load_tool_from_path(tool_name, folder_name, file_name):
    """Charge un outil en cherchant le fichier"""
    # Obtenir le dossier actuel
    current_dir = os.getcwd()
    
    # Essayer différents chemins
    possible_paths = [
        os.path.join(current_dir, folder_name, file_name),
        os.path.join(current_dir, folder_name),
        os.path.join(current_dir, file_name),
        os.path.join(current_dir, folder_name, "app.py"),
        os.path.join(current_dir, folder_name, "code.py"),
        os.path.join(current_dir, folder_name, "main.py"),
    ]
    
    # Si le fichier a un nom spécifique, l'ajouter aux recherches
    if file_name:
        possible_paths.insert(0, os.path.join(current_dir, folder_name, file_name))
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                exec(code, globals())
                return True
            except Exception as e:
                st.error(f"Erreur d'execution: {str(e)}")
                return False
    
    # Si non trouvé, afficher le contenu du dossier pour déboguer
    st.error(f"Fichier non trouve: {folder_name}/{file_name}")
    st.write(f"📁 Dossier courant: {current_dir}")
    
    # Lister les dossiers présents
    if os.path.exists(current_dir):
        items = os.listdir(current_dir)
        st.write(f"📁 Contenu du dossier courant: {items}")
        
        # Vérifier si le dossier existe
        if os.path.exists(folder_name):
            st.write(f"📁 Contenu de {folder_name}: {os.listdir(folder_name)}")
        else:
            st.warning(f"Le dossier '{folder_name}' n'existe pas")
    
    return False

# ==================== PAGE D'ACCUEIL ====================

def show_home():
    # En-tête
    st.markdown('<div class="hero"><h1>🏭 Suite Outils Fournisseur</h1><p>Plateforme integree pour la verification et l analyse des documents d expedition</p></div>', unsafe_allow_html=True)
    
    # Présentation
    st.markdown('<div class="about-section"><h3>🎯 A propos</h3><p>Cette plateforme centralise tous vos outils de verification fournisseur :</p><ul><li>📊 Container Dashboard - Tableau de bord des indicateurs et KPIs fournisseur</li><li>📦 Comparateur BOM vs Packing - Verification des quantites entre BOM et packing list</li><li>🔄 Comparateur BOM vs BOM - Analyse et comparaison des versions BOM</li><li>📍 Check Position - Verification des positions et emplacements</li><li>✅ Checking Reply - Verification et analyse des reponses fournisseur</li><li>📐 Box Calculator - Calcul du nombre de cartons selon le type d article et le modele TV</li></ul><p>Selectionnez l outil ci-dessous pour commencer.</p></div>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center; margin-bottom: 1.5rem; color: #1e3c72;">📌 Outils disponibles</h2>', unsafe_allow_html=True)
    
    # Definition des outils (folder, filename)
    tools = [
        {"name": "Container Dashboard", "icon": "📊", "desc": "Tableau de bord des indicateurs et KPIs fournisseur", "folder": "container-dashboard", "file": "code.py"},
        {"name": "Comparateur BOM vs Packing", "icon": "📦", "desc": "Verification des quantites entre BOM et packing list", "folder": "comparator-bom_packing", "file": "app.py"},
        {"name": "Comparateur BOM vs BOM", "icon": "🔄", "desc": "Analyse et comparaison des versions BOM", "folder": "comparator-bom_bom", "file": "bom_old and new.py"},
        {"name": "Check Position", "icon": "📍", "desc": "Verification des positions et emplacements", "folder": "check_position", "file": "code.py"},
        {"name": "Checking Reply", "icon": "✅", "desc": "Verification et analyse des reponses fournisseur", "folder": "checking-reply", "file": "checke replay.py"},
        {"name": "Box Calculator", "icon": "📐", "desc": "Calcul du nombre de cartons selon le type d article et le modele TV", "folder": "Box-calculator", "file": "app.py"}
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
                        st.session_state.selected_tool = tool["name"]
                        st.session_state.tool_folder = tool["folder"]
                        st.session_state.tool_file = tool["file"]
                        st.rerun()
    
    # Pied de page
    st.markdown('<div class="footer"><p>© 2024 - Suite Outils Fournisseur | Version 2.0</p><p>Développé pour les équipes ingénierie</p></div>', unsafe_allow_html=True)

# ==================== CHARGEMENT DES OUTILS ====================

def show_tool(tool_name, tool_folder, tool_file):
    # Bouton retour
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("← Accueil", key="back_home"):
            go_home()
    
    # En-tête
    st.markdown(f'<div class="tool-header"><h2>🛠️ {tool_name}</h2></div>', unsafe_allow_html=True)
    
    # Chargement
    with st.spinner(f"Chargement de {tool_name}..."):
        success = load_tool_from_path(tool_name, tool_folder, tool_file)
        
        if not success:
            st.error(f"Impossible de charger {tool_name}")
            st.info("Verifiez que le fichier existe bien dans le dossier correspondant")

# ==================== ROUTAGE PRINCIPAL ====================

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'tool':
    if st.session_state.selected_tool:
        show_tool(st.session_state.selected_tool, st.session_state.tool_folder, st.session_state.tool_file)
