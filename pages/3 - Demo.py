import streamlit as st
from analyzer import analyze_pdf
from pathlib import Path
from io import BytesIO
import base64
import nltk

nltk.download('punkt')

# Set up page
st.set_page_config(page_title="📂 Demo - PDF Analyzer", layout="wide")
st.title("📂 DocuBot Demo")

# Sidebar info
with st.sidebar:
    st.info("""
    👈 Upload a PDF or use the sample provided.
    Ask a question (optional) and click Analyze.
    You'll receive named entities, relevant chunks, and a summary.
    """)

# File upload
st.subheader("📤 Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Use default sample PDF if no upload
if uploaded_file is None:
    sample_path = Path("Part-Unit-2-lecture.pptx.pdf")
    if sample_path.exists():
        uploaded_file = open(sample_path, "rb")
        st.caption("ℹ️ Using default sample: Part-Unit-2-lecture.pptx.pdf")
    else:
        st.warning("Please upload a PDF file to begin.")
        st.stop()

# User query
query = st.text_input("🔎 Ask a question about the document (optional)", value="What is the main topic of the document?")

if st.button("🚀 Analyze Document"):
    with st.spinner("Analyzing... this may take a few seconds..."):
        result = analyze_pdf(uploaded_file, query)

    st.markdown("---")
    st.subheader("🧠 Named Entities")
    col1, col2, col3 = st.columns(3)
    col1.markdown("👤 People")
    col1.write(result["entities"].get("people", []))
    col2.markdown("🌍 Places")
    col2.write(result["entities"].get("places", []))
    col3.markdown("🏢 Organizations")
    col3.write(result["entities"].get("organizations", []))

    st.markdown("---")
    st.subheader("📌 Relevant Chunks")
    for i, chunk in enumerate(result["relevant_chunks"], 1):
        st.markdown(f"{i}. {chunk}")

    st.markdown("---")
    st.subheader("📝 Summary")
    for i, sentence in enumerate(result["summary"], 1):
        st.markdown(f"{i}. {sentence}")

    # Downloads
    def get_binary_file_downloader_html(bin_data, filename, label):
        b64 = base64.b64encode(bin_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{label}</a>'
        return href

    st.markdown("---")
    st.subheader("⬇️ Download Summary")

    # .txt
    txt_bytes = "\n".join(result["summary"]).encode("utf-8")
    st.markdown(get_binary_file_downloader_html(txt_bytes, "summary.txt", "📄 Download as .txt"), unsafe_allow_html=True)

    # .pdf (optional)
    from fpdf import FPDF

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in result["summary"]:
        pdf.multi_cell(0, 10, line)

    # Fix: use dest='S' and encode to bytes, then wrap in BytesIO
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer = BytesIO(pdf_output)

    # Now use this to create downloadable content
    st.markdown(get_binary_file_downloader_html(pdf_buffer.getvalue(), "summary.pdf", "📑 Download as .pdf"), unsafe_allow_html=True)


    st.markdown("---")
    st.subheader("⭐ Rate This App")
    rating = st.radio("How satisfied are you with this analysis?", ["😡 1", "😕 2", "😐 3", "🙂 4", "🤩 5"])
    feedback = st.text_area("💬 Any feedback you'd like to share?")
    if st.button("📩 Submit Feedback"):
        st.success("✅ Thank you! Your response has been recorded.")
