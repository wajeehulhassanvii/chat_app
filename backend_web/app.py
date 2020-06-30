from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


app = Flask(__name__)
api = Api(app)

# initiate two different chatbots
app_trained_bot = ChatBot("App Trained Bilal Bot")
standard_bot = ChatBot("Standard Bilal Bot")

# app training of chat bot
trainer = ListTrainer(app_trained_bot)

conversation = [
    "Hi",
    "How can I help you?",
    "Are you a machine learning engineer?",
    "Not, me but Wajeeh who designed me, is.",
    "Thanks",
    "You're welcome!!!",
]

trainer.train(conversation)

# standard training of the bot
corpus_trainer = ChatterBotCorpusTrainer(standard_bot)
corpus_trainer.train("chatterbot.corpus.english")
corpus_trainer.train("chatterbot.corpus.english.greetings")
corpus_trainer.train("chatterbot.corpus.english.conversations")

# for the home '/'
class Home(Resource):
    def get(self):
        return jsonify({
            "status": 200,
            "msg": "you're home"
            })


class Chat(Resource):
    def post(self):
        posted_data = request.get_json()
        question = posted_data['question']
        app_trained_bot_answer = app_trained_bot.get_response(question)
        standard_bot_answer = standard_bot.get_response(question)
        # type(standard_bot_answer)
        return jsonify({
            "status": 200,
            "app trained bot replies": str(app_trained_bot_answer),
            "standard bot replies": str(standard_bot_answer)
        })


api.add_resource(Home, '/')
api.add_resource(Chat, '/chat')


if __name__=="__main__":
    app.run(host="0.0.0.0", port="5000")