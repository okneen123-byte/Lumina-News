import streamlit as st
import requests

# --------------------
# App Titel
# --------------------
st.set_page_config(page_title="Lumina News KI", layout="wide")

st.title("📰 Lumina News KI")
st.write("Erhalte aktuelle Nachrichten aus allen Kategorien – automatisch aktualisiert.")

# --------------------
# E-Mail für Login / Trial / Paid
# --------------------
email = st.text_input("📧 Deine E-Mail-Adresse (für Free Trial oder Premium-Zugang):")

# --------------------
# Kategorien Auswahl
# --------------------
categories = ["general", "technology", "business", "sports", "science", "entertainment"]
category = st.selectbox("Kategorie auswählen:", categories)

# --------------------
# Button für News
# --------------------
if st.button("🔍 News anzeigen"):
    if email.strip() == "":
        st.warning("Bitte gib deine E-Mail-Adresse ein.")
    else:
        url = f"http://127.0.0.1:8000/news?email={email}&category={category}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for article in data:
                st.subheader(article["title"])
                st.write(article["description"])
                st.write(f"[Artikel lesen]({article['url']})")
                st.divider()
        else:
            st.error("Fehler beim Abrufen der News. Bitte später erneut versuchen.")