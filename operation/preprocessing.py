from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Function to get relevant chunks using TF-IDF and cosine similarity
def get_relevant_chunks(query, chunks, top_n=3):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks + [query])
    cosine_sim = cosine_similarity(vectors[-1:], vectors[:-1])
    relevant_indices = cosine_sim[0].argsort()[-top_n:][::-1]
    return [chunks[i] for i in relevant_indices]

def create_combined_prompt(question, sql_prompt):
    # Define keywords for user-specific queries
    user_specific_keywords = ["my department", "my course", "my details", "give me"]

    # Define keywords for non-user-specific queries
    general_keywords = [
        "department names", "course names", "college history", 
        "programmes of study", "infrastructure", "placement", "facilities"
    ]

    # Check if the question matches user-specific keywords
    if any(keyword in question.lower() for keyword in user_specific_keywords):
        return f"{sql_prompt}\n\nWrite a query to fetch the relevant information using user_id='{st.session_state.id}'.\n\nQuestion: {question}\n\n"

    # Check if the question matches general keywords
    elif any(keyword in question.lower() for keyword in general_keywords):
        return f"{sql_prompt}\n\nWrite a query to fetch the relevant information without using user_id or any specific filters.\n\nQuestion: {question}\n\n"

    # Default behavior
    return f"{sql_prompt}\n\n{question}\n\n"
