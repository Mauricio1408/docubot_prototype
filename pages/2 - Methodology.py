import streamlit as st

st.set_page_config(page_title="🧪 Methodology", layout="wide")

st.title("🧪 Methodology")

st.markdown("""
This section outlines the techniques and processes that power DocuBot. The system uses classical NLP techniques (not large language models) for transparency, efficiency, and reproducibility.

---

## 🧠 Named Entity Recognition (NER)

We use spaCy's en_core_web_trf transformer model to identify:

- 👤 People (e.g., scientists, authors, historical figures)
- 🌍 Locations (cities, countries, geographic entities)
- 🏢 Organizations (institutions, universities, companies)

NER helps highlight key actors and topics within the document.

▶️ Example:  
"Bayes Theorem was developed by Thomas Bayes"  ⟶  PERSON: Thomas Bayes

---

## 🔎 Document Search (QA by TF-IDF)

We divide the document into sentences, then compute TF-IDF scores:

1. 📜 Tokenize the document into sentences  
2. 📈 Compute TF-IDF for each sentence and the query
3. 📏 Rank sentences by cosine similarity to the query

This lets the system find the most relevant chunks to a user's question.

▶️ Example Query: "What is Naive Bayes?"  
Returns the 3-5 sentences best matching the question.

---

## 📝 Extractive Summarization (TextRank)

We use the TextRank algorithm to select the most central sentences:

1. ✂️ Tokenize into sentences
2. 🔗 Build a similarity graph of sentence vectors
3. 📊 Rank using PageRank-style weights
4. 🧾 Return top-ranked sentences as summary

No neural generation — just high-signal extracts.

▶️ Why TextRank?  
- No training needed
- Fast and interpretable
- Works well on lecture slides and academic content

---

## ⚙️ Development Workflow

📁 File Types Supported:
- PDF (.pdf)
- PPTX exported as PDF (.pptx.pdf)

⚒️ Libraries Used:
- pdfplumber (PDF parsing)
- spaCy (NER)
- sklearn (TF-IDF, cosine similarity)
- sumy (TextRank)
- streamlit (Web UI)

📦 Output:
- Named Entities (👤🌍🏢)
- Relevant Text Chunks (🔍)
- Summary Sentences (📝)
- Download buttons (.txt / .pdf)

---

Use the "Demo" page to explore this pipeline in action! ✨
""")
