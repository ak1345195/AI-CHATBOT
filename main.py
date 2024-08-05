from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Create a new chatbot instance
bot = ChatBot(
    "chatbot",
    read_only=False,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Sorry, I don't have an answer for that.",
            "maximum_similarity_threshold": 0.9
        }
    ]
)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")


# Function to fetch web search results
def fetch_web_response(query):
    api_key = 'AIzaSyB_5COiIYw9pAAcDyD_ZrN3oipSOMZq-gM'
    cse_id = '872432c3c87ed4c62'
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
    response = requests.get(search_url).json()
    if 'items' in response:
        return response['items'][0]['snippet']
    else:
        return "I couldn't find an answer to your question."


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    bot_response = bot.get_response(userText)

    if float(bot_response.confidence) < 0.5:
        # If confidence is low, fetch response from the web
        web_response = fetch_web_response(userText)
        return str(web_response)
    else:
        return str(bot_response)


if __name__ == "__main__":
    app.run(debug=True)
