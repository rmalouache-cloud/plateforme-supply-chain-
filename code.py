import streamlit as st
import os

# AFFICHAGE DE DIAGNOSTIC - À SUPPRIMER PLUS TARD
st.write("=== DIAGNOSTIC ===")
st.write(f"Dossier courant: {os.getcwd()}")
st.write("Contenu du dossier courant:")
for item in os.listdir('.'):
    st.write(f"  - {item}")
    if os.path.isdir(item):
        try:
            st.write(f"    Contenu de {item}:")
            for subitem in os.listdir(item):
                st.write(f"      - {subitem}")
        except:
            pass

# ... reste de votre code
