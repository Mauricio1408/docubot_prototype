# == app.py ==
import streamlit as st

st.set_page_config(page_title="DocuBot", layout="wide", initial_sidebar_state="expanded")
st.title("🤖 DocuBot")
st.markdown("""
Welcome to the **DocuBot**!. Navigate using the sidebar.
- Learn about the app on the **Introduction** page
- Understand its design on the **Methodology** page
- Try it out on the **Demo** page

✨ Features:
- PDF upload and document analysis (NER, summarization)
- Custom user query support for QA
- Downloadable summary report
- Light/dark mode compatible
""")
