import streamlit as st
import os
from collections import Counter
import re
import pandas as pd

# ── Configuration ──────────────────────────────────────────
# os.getenv() lit depuis .env en local, depuis les variables
# d'environnement du serveur en production
APP_TITLE = os.getenv('APP_TITLE', 'Analyseur de Texte IA')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

st.set_page_config(
    page_title=APP_TITLE,
    page_icon='📝',
    layout='centered'
)

# ── En-tête ────────────────────────────────────────────────
st.title(f'📝 {APP_TITLE}')
st.caption(f'Version {APP_VERSION} — Déployée avec Streamlit')
st.divider()

# ── Saisie utilisateur ─────────────────────────────────────
texte = st.text_area(
    'Entrez votre texte à analyser :',
    placeholder='Copiez ici n\'importe quel texte...',
    height=200
)

# ── Analyse ────────────────────────────────────────────────
if st.button('Analyser', type='primary'):
    if not texte:
        st.warning('Entrez un texte avant d\'analyser.')
    else:
        # Nettoyage
        mots = re.findall(r'\b\w+\b', texte.lower())
        phrases = [s.strip() for s in re.split(r'[.!?]', texte) if s.strip()]
        freq = Counter(mots)
        
        # KPIs
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Caractères', len(texte))
        col2.metric('Mots', len(mots))
        col3.metric('Phrases', len(phrases))
        col4.metric('Mots uniques', len(set(mots)))
        
        # Mots les plus fréquents
        st.subheader('Mots les plus fréquents')
        top10 = freq.most_common(10)
        mots_label = [m for m, _ in top10]
        mots_count = [c for _, c in top10]
        
        df = pd.DataFrame({'Mot': mots_label, 'Fréquence': mots_count})
        st.bar_chart(df.set_index('Mot'))
        
        # Densité lexicale
        densite = len(set(mots)) / len(mots) * 100 if mots else 0
        st.metric('Densité lexicale', f'{densite:.1f}%',
            help='% de mots différents — plus c\'est élevé, plus le texte est riche')

# ── Footer ─────────────────────────────────────────────────
st.divider()
st.caption('Formation IA Professionnelle — Module Déploiement')
