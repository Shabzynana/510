# import files
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

chatbot = ChatBot(
    'Chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.',
        'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri = ""
)


english_data = open('training_data/english.txt').read().splitlines()
yoruba_data = open('training_data/yoruba.txt').read().splitlines()


training_data = english_data + yoruba_data


trainer = ListTrainer(chatbot)
trainer.train(training_data)
trainer_corpus = ChatterBotCorpusTrainer(chatbot)


@app.route("/")
def index():
    return render_template("chatbot.html")


@app.route("/get_response")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run(debug=True,port=5006)
