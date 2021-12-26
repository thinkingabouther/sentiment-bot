import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sentiment_aggregator import SentimentAggregator

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
APP_URL = os.environ['APP_URL']
ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_API_KEY']
YOUTUBE_ENDPOINT = os.environ['YOUTUBE_ENDPOINT']
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']


class Bot:
    def __init__(self, port, token, app_url, endpoint, key, youtube_endpoint, youtube_key):
        self.sentiment_aggregator = SentimentAggregator(endpoint, key, youtube_endpoint, youtube_key)
        self.updater = Updater(TOKEN, use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('bop', self.bop))
        dp.add_handler(CommandHandler('never_gonna', self.never_gonna()))

        self.updater.start_webhook(listen="0.0.0.0",
                                   port=int(port),
                                   url_path=token)
        self.updater.bot.setWebhook(app_url + token)

    def idle(self):
        self.updater.idle()

    def bop(self, update: Update, context: CallbackContext):
        update.message.reply_text("bop умер, не пишите")

    def never_gonna(self, update):
        positive, neutral, negative = self.sentiment_aggregator.aggregate_sentiments("dQw4w9WgXcQ")
        reply_text = "Положительный = {}" \
                     "Нейтральный = {}" \
                     "Отрицательный = {}".format(positive, neutral, negative);
        update.message.reply_text(reply_text)


if __name__ == '__main__':
    bot = Bot(PORT, TOKEN, APP_URL, ENDPOINT, KEY, YOUTUBE_ENDPOINT, YOUTUBE_KEY)
    bot.idle()