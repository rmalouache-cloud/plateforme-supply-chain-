import streamlit as st
import os

# ===== DIAGNOSTIC TEMPORAIRE - À SUPPRIMER PLUS TARD =====
st.write("### Diagnostic - Structure des dossiers")
st.write(f"Dossier courant: {os.getcwd()}")

# Lister tous les fichiers et dossiers
st.write("Contenu du dossier courant:")
for item in sorted(os.listdir('.')):
    if os.path.isdir(item):
        st.write(f"📁 {item}/")
        try:
            for subitem in sorted(os.listdir(item)):
                st.write(f"    📄 {subitem}")
        except:
            pass
    else:
        st.write(f"📄 {item}")

st.markdown("---")
# ===== FIN DIAGNOSTIC =====

# ... reste de votre code
