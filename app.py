from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import sqlite3

app = Flask(__name__)

# Load NLP Model
qa_model = pipeline("question-answering",
                    model="distilbert-base-uncased-distilled-squad")

# Load FAQ context
context = """
Admission opens in June.
Tuition fee is $2000 per semester.
Scholarships are available for merit students.
Hostel facilities include WiFi and mess.
Library is open from 9AM to 5PM.
"""

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            confidence REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- CHAT API ----------
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json["message"]

    result = qa_model(
        question=user_question,
        context=context
    )

    answer = result["answer"]
    score = result["score"]

    if score < 0.2:
        answer = "Sorry, I don't have information about that."

    save_log(user_question, answer, score)

    return jsonify({
        "reply": answer,
        "confidence": round(score, 2)
    })

# ---------- SAVE LOG ----------
def save_log(question, answer, confidence):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (question, answer, confidence)
        VALUES (?, ?, ?)
    """, (question, answer, confidence))
    conn.commit()
    conn.close()

# ---------- VIEW LOGS ----------
@app.route("/logs")
def logs():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer, confidence FROM logs")
    data = cursor.fetchall()
    conn.close()
    return render_template("logs.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
