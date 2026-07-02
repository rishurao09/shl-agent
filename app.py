import streamlit as st
import json
from difflib import get_close_matches

# 🔹 Load data
def load_catalog():
    with open("data/shl_catalog.json", "r", encoding="utf-8") as file:
        return json.load(file)

# 🔹 Process query (with typo handling)
def process_query(query):
    query = query.lower().strip()
    words = query.split()

    known_words = [
        "python", "java", "developer", "backend",
        "frontend", "data", "analyst", "cognitive",
        "test", "engineer"
    ]

    corrected = []

    for w in words:
        match = get_close_matches(w, known_words, n=1, cutoff=0.7)
        if match:
            corrected.append(match[0])
        else:
            corrected.append(w)

    return corrected

# 🔹 Recommendation system
def recommend_assessments(query):
    catalog = load_catalog()
    keywords = process_query(query)

    results = []

    for item in catalog:
        name = item.get("name", "").lower()
        description = item.get("description", "").lower()

        score = 0

        for word in keywords:
            if word in name:
                score += 4
            if word in description:
                score += 2

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])
    return [item for score, item in results]

# 🔹 UI
st.set_page_config(page_title="SHL Recommender", layout="centered")

st.title("🤖 SHL Assessment Recommender")
st.write("Enter a job role or skill to get relevant assessments.")

query = st.text_input("🔍 Enter job role or skill:")

if query:
    results = recommend_assessments(query)

    if results:
        st.subheader("🎯 Top Recommendations")

        for r in results[:5]:
            name = r.get("name")
            duration = r.get("duration")

            # ✅ FIX: handle different possible URL keys
            url = r.get("url") or r.get("productUrl") or r.get("link")

            # fix missing https
            if url and not str(url).startswith("http"):
                url = "https://" + str(url)

            st.markdown(f"### {name}")
            st.write(f"⏱ Duration: {duration}")

            if url:
                st.markdown(f"🔗 [Open Assessment]({url})")
            else:
                st.write("No link available")

            st.write("---")

    else:
        st.warning("No results found. Try different keywords.")