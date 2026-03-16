import streamlit as st
from textblob import TextBlob
import pandas as pd

# ── Configuration de la page ──────────────────
st.set_page_config(
    page_title='Analyseur de Sentiments',
    page_icon='🎭',
    layout='centered'
)

# ── Initialiser l'historique dans session_state ─
if 'historique' not in st.session_state:
    st.session_state['historique'] = []

# ── En-tête ────────────────────────────────────
st.title('🎭 Analyseur de Sentiments IA')
st.write('Entrez un texte et découvrez son sentiment !')
st.divider()

# ── Zone de saisie ─────────────────────────────
texte = st.text_area(
    'Votre texte à analyser :',
    placeholder='Ex: This product is absolutely amazing!',
    height=150
)

# ── Bouton d'action ────────────────────────────
if st.button('🔍 Analyser le sentiment', type='primary'):
    if texte:

        # Analyse
        blob = TextBlob(texte)
        score = blob.sentiment.polarity

        # Classer le sentiment
        if score > 0.1:
            sentiment = 'POSITIF'
            emoji = '😊'
        elif score < -0.1:
            sentiment = 'NÉGATIF'
            emoji = '😠'
        else:
            sentiment = 'NEUTRE'
            emoji = '😐'

        # Afficher les résultats
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric('Score de sentiment', f'{score:.2f}')
        col2.metric('Résultat', f'{emoji} {sentiment}')

        # Message coloré
        if score > 0.1:
            st.success(f'Texte POSITIF détecté {emoji}')
        elif score < -0.1:
            st.error(f'Texte NÉGATIF détecté {emoji}')
        else:
            st.info(f'Texte NEUTRE détecté {emoji}')

        # ── Historique : ajouter l'analyse ─────────
        st.session_state['historique'].append({
            'Texte': texte[:50],
            'Score': round(score, 2),
            'Sentiment': f'{emoji} {sentiment}'
        })
        # Garder seulement les 5 dernières analyses
        st.session_state['historique'] = st.session_state['historique'][-5:]

    else:
        st.warning('Veuillez entrer du texte !')

# ── Afficher l'historique ──────────────────────
if st.session_state['historique']:
    st.divider()
    st.subheader('📋 Historique des analyses')
    df = pd.DataFrame(st.session_state['historique'])
    st.dataframe(df, use_container_width=True)

    # ── Graphique d'évolution des scores ───────
    st.subheader('📈 Évolution des scores')
    st.line_chart(df['Score'])

    # ── Export CSV ─────────────────────────────
    csv = df.to_csv(index=False)
    st.download_button(
        label='📥 Télécharger l\'historique (CSV)',
        data=csv,
        file_name='historique_sentiments.csv',
        mime='text/csv'
    )