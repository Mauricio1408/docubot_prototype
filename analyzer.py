import pdfplumber
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import re
import numpy as np

# Load spaCy transformer model
nlp = spacy.load("en_core_web_trf")

# if u want to use our model, uncomment line 15-19 and change spacy load directory to model-best on ur local machine (p.s. our machine kinda works but needs more dataset haha)
# nlp = spacy.load(r'C:\Users\Mauricio\Documents\3rd Year 2nd Semester\Natural Language Processing\docubot_backend\docubot\output_ner_model_two\model-best')

# # Check and add the sentencizer if it's missing
# if "sentencizer" not in nlp.pipe_names:
#     nlp.add_pipe("sentencizer")

# === Text Cleaning ===
def clean_text(text):
    text = re.sub(r"•", "", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# === PDF Extraction ===
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return clean_text(text)

# === Named Entity Recognition ===
def perform_ner(text):
    doc = nlp(text)
    return {
        "people": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "places": [ent.text for ent in doc.ents if ent.label_ in {"GPE", "LOC"}],
        "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    }

# === TF-IDF Relevance ===
def get_relevant_chunks(query, text, num_chunks=5):
    sentences = [sent.text.strip() for sent in nlp(text).sents if len(sent.text.strip()) > 10]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(sentences + [query])
    cosine_sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
    indices = cosine_sim.argsort()[0, -num_chunks:][::-1]
    return [sentences[i] for i in indices]

# === Summary Cleanup ===
def deduplicate(sentences):
    seen = set()
    result = []
    for s in sentences:
        s = s.strip()
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result

def is_too_technical(s):
    return s.count("=") > 3 or len(s) > 300

def is_tabular(s):
    return bool(re.match(r'^\d', s)) or len(re.findall(r'\d+', s)) > 6

def shorten(s, limit=250):
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "..."

def filter_summary(summary):
    return [shorten(s) for s in deduplicate(summary) if not is_too_technical(s) and not is_tabular(s)]

# === TextRank Summarizer ===
def summarize_text(text, num_sentences=10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return filter_summary([str(sentence) for sentence in summary])

# === Top-Level Function ===
def analyze_pdf(file, query):
    text = extract_text_from_pdf(file)
    entities = perform_ner(text)
    chunks = get_relevant_chunks(query, text)
    summary = summarize_text(text)
    return {
        "entities": entities,
        "relevant_chunks": chunks,
        "summary": summary
    }
