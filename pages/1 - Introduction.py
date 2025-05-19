import streamlit as st

st.set_page_config(page_title="📘 Introduction", layout="wide")

st.title("📘 Welcome to DocuBot: PDF Analyzer")

st.markdown("""
DocuBot is a lightweight, efficient, and interpretable PDF document analysis tool built for academic and technical materials.

### 🎯 Objective
To build a reliable system that:
- Extracts text from PDF and PPTX-based lecture slides.
- Applies Named Entity Recognition (NER) to highlight important people, places, and organizations.
- Performs document-level question answering using TF-IDF.
- Summarizes content extractively using TextRank.

### 🔍 Use Case
Whether you're studying, reviewing a report, or evaluating a research paper, DocuBot helps you:
- Quickly understand the core topics.
- Search through document segments using natural questions.
- Get concise summaries without reading everything manually.

### 💡 Why This Matters
Many educational PDFs (especially slides) are dense with fragmented bullets and equations. DocuBot is designed to cleanly parse and analyze these, helping users:
- Save time
- Focus on relevant content
- Extract technical insights

### 🌐 Features
- Upload .pdf and .pptx.pdf files
- Named Entity Recognition (NER)
- Relevance-based document QA
- Extractive summarization (no LLMs!)
- Optional light/dark UI themes
- Downloadable summary in .txt and .pdf

Jump to the "Demo" tab to try it yourself! 🚀
""")
