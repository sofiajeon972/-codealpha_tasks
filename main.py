# -codealpha_tasks/faqs chatbot
import spacy
import numpy as np

greeting_responses = [
    "Hello! How can I help you?",
    "Hi there! What can I do for you?",
    "Good day! Ask me anything about our services."
]

farewells = ["goodbye", "see you", "later"]

# Load SpaCy's medium English model with word vectors
nlp = spacy.load("en_core_web_md")

# Sample FAQs - replace with your actual questions and answers
faqs = [  
      {
        "question": "How do I reset my password?",
        "answer": "You can reset your password by visiting the account settings page and clicking 'Forgot Password'."
    },
    {
        "question": "What is your return policy?",
        "answer": "Our return policy allows you to return products within 30 days of purchase."
    },
    {
        "question": "How can I track my order?",
        "answer": "You can track your order using the tracking number sent to your email."
    },
    {
        "question": "Do you offer international shipping?",
        "answer": "Yes, we offer shipping to most countries worldwide."}
]



import streamlit as st
import requests

st.title("AI FAQs Chatbot")

question = st.text_input("Ask a question:")
if st.button("Submit"):
    response = requests.post("http://localhost:5000/chat", json={"question": question})
    st.write(response.json()["answer"])










  

def preprocess_text(text):
    """Process text by lemmatizing, removing stopwords and punctuation"""
    doc = nlp(text)
    processed_tokens = [
        token.lemma_.lower() 
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(processed_tokens)

# Preprocess FAQs and store vectors
processed_faqs = []
for faq in faqs:
    processed = preprocess_text(faq["question"])
    vector = nlp(processed).vector
    processed_faqs.append({
        "original": faq["question"],
        "answer": faq["answer"],
        "vector": vector
    })

def get_most_similar(user_input, threshold=0.7):
    """Find the most similar FAQ entry to the user input"""
    processed_input = preprocess_text(user_input)
    input_vector = nlp(processed_input).vector
    
    max_similarity = -1
    best_match = None
    
    for faq in processed_faqs:
        similarity = np.dot(input_vector, faq["vector"]) / (
            np.linalg.norm(input_vector) * np.linalg.norm(faq["vector"])
        )
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = faq
    
    return best_match, max_similarity

# Chat interface
print("FAQ Bot: Hello! I can answer questions about our services. Type 'exit' to end.")
while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("FAQ Bot: Goodbye!")
        break
        
    # Check for empty input
    if not user_input.strip():
        print("FAQ Bot: Please type your question.")
        continue
        
    best_match, similarity = get_most_similar(user_input)
    
    if similarity > 0.7:
        print(f"FAQ Bot: {best_match['answer']}")
    else:
        print("FAQ Bot: I'm sorry, I don't understand that question. Could you rephrase it?")

conversation_context = {}

def handle_context(user_input):
    # Implement context tracking logic
    pass
