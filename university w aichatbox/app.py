from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import traceback
import os

app = Flask(__name__)


API_KEY = "AIzaSyDQU54zYrDtkyAS8axL_YUONGA-Nmf-hXY"
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-2.5-flash")

def load_knowledge():
    knowledge_text = ""
    try:
       
        knowledge_dir = os.path.join(app.root_path, "knowledge")

        for filename in os.listdir(knowledge_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(knowledge_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    knowledge_text += f"\n\n--- {filename} ---\n{file_content}"

        print("✅ Knowledge base loaded successfully.")
    except Exception as e:
        print("⚠️ Error loading knowledge files:", e)

    return knowledge_text


site_knowledge = load_knowledge()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        user_message = request.json.get("message")

        context = f"""
        You are the official WVSU Cybersecurity AI Assistant.
        Use only the following information to answer questions accurately.
        If the answer isn’t found, politely say you don’t know yet.

        Knowledge Base:
        {site_knowledge}
        """

        response = model.generate_content(f"{context}\nUser: {user_message}")
        return jsonify({"reply": response.text})

    except Exception as e:
        print("⚠️ FULL ERROR TRACE:")
        traceback.print_exc()
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)

