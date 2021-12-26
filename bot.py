import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sentiment_analyser import SentimentAnalyzer
from youtube_reader import YouTubeReader

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
APP_URL = os.environ['APP_URL']
ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_API_KEY']
YOUTUBE_ENDPOINT = os.environ['YOUTUBE_ENDPOINT']
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']


class Bot:
    def __init__(self, port, token, app_url, endpoint, key, youtube_endpoint, youtube_key):
        self.sentiment_analyser = SentimentAnalyzer(endpoint, key)
        self.youtube_reader = YouTubeReader(youtube_endpoint, youtube_key)
        self.updater = Updater(TOKEN, use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('bop', self.bop))

        self.updater.start_webhook(listen="0.0.0.0",
                                   port=int(port),
                                   url_path=token)
        self.updater.bot.setWebhook(app_url + token)

    def idle(self):
        self.updater.idle()

    def bop(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        update.message.reply_text(self.sentiment_analyser.get_sentiment('Hello').sentiment)

    def get_comments(self, video_id):
        self.youtube_reader.read_comments_by_id("dQw4w9WgXcQ")


if __name__ == '__main__':
    bot = Bot(PORT, TOKEN, APP_URL, ENDPOINT, KEY, YOUTUBE_ENDPOINT, YOUTUBE_KEY)
    bot.idle()