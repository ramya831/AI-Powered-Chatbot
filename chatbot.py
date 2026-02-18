import nltk
from transformers import pipeline

nltk.download('punkt')

qa_model = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)

def get_context():
    with open("data/faq.txt", "r") as file:
        return file.read()

def get_response(user_question):
    context = get_context()

    result = qa_model(
        question=user_question,
        context=context
    )

    answer = result["answer"]
    score = result["score"]

    # Confidence check
    if score < 0.2:
        return "Sorry, I could not understand your question."
    else:
        return answer
