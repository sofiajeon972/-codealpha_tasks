import spacy
import numpy as np
import random

# Load SpaCy's medium English model with word vectors
nlp = spacy.load("en_core_web_md")

# Greeting and farewell responses
greeting_responses = [
    "Hello! How can I help you?",
    "Hi there! What can I do for you?",
    "Good day! Ask me anything about our services."
]

farewells = ["goodbye", "see you", "later", "bye", "quit", "exit"]

# Sample FAQs
faqs = [
    {"question": "How do I reset my password?", "answer": "You can reset your password by visiting the account settings page and clicking 'Forgot Password'."},
    {"question": "What is your return policy?", "answer": "Our return policy allows you to return products within 30 days of purchase."},
    {"question": "How can I track my order?", "answer": "You can track your order using the tracking number sent to your email."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we offer shipping to most countries worldwide."}
]

conversation_context = {}


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


def add_faq(new_question, new_answer):
    """Add a new FAQ to the list"""
    processed_question = preprocess_text(new_question)
    new_vector = nlp(processed_question).vector
    processed_faqs.append({
        "original": new_question,
        "answer": new_answer,
        "vector": new_vector
    })


def handle_context(user_input):
    """Handle contextual follow-ups"""
    global conversation_context

    if "track order" in user_input.lower():
        conversation_context["topic"] = "order_tracking"
        return "Sure! Can you provide your order number?"
    
    if conversation_context.get("topic") == "order_tracking":
        conversation_context.clear()
        return "Tracking your order... (simulate API call)"

    return None


def log_unanswered_question(question):
    """Log unanswered questions to a file"""
    with open("unanswered_questions.txt", "a") as file:
        file.write(f"{question}\n")


# Chat interface
print("FAQ Bot: Hello! I can answer questions about our services. Type 'exit' to end.")
while True:
    user_input = input("\nYou: ")

    if user_input.lower() in farewells:
        print("FAQ Bot: Goodbye! Take care!")
        break

    if any(greet in user_input.lower() for greet in ["hello", "hi", "hey"]):
        print(f"FAQ Bot: {random.choice(greeting_responses)}")
        continue

    if not user_input.strip():
        print("FAQ Bot: Please type your question.")
        continue

    context_response = handle_context(user_input)
    if context_response:
        print(f"FAQ Bot: {context_response}")
        continue

    best_match, similarity = get_most_similar(user_input)

    if similarity > 0.85:
        print(f"FAQ Bot: {best_match['answer']}")
    elif similarity > 0.7:
        print(f"FAQ Bot: I think you’re asking: '{best_match['original']}'. Is this what you meant?")
    else:
        print("FAQ Bot: I’m not sure about that. Would you like me to connect you to a support agent or give you our contact details?")
        log_unanswered_question(user_input)

    print("\nFAQ Bot: You can also add new questions if you'd like!")
    new_question = input("New question (or press Enter to skip): ")
    if new_question:
        new_answer = input("Answer to your new question: ")
        add_faq(new_question, new_answer)
        print("FAQ Bot: New question added! 🚀")

    conversation_context.clear()


