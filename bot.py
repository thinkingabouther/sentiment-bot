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
        dp.add_handler(CommandHandler('never_gonna', self.never_gonna))

        self.updater.start_webhook(listen="0.0.0.0",
                                   port=int(port),
                                   url_path=token)
        self.updater.bot.setWebhook(app_url + token)

    def idle(self):
        self.updater.idle()

    def bop(self, update: Update, context: CallbackContext):
        update.message.reply_text("bop умер, не пишите")

    def never_gonna(self, update, context):
        scores = self.sentiment_aggregator.aggregate_sentiments("dQw4w9WgXcQ")
        reply_text = "🤔 Что мы узнали:\n" \
                     "🤯 Проанализировано комментариев {}\n" \
                     "👍 Положительных комментариев {}\n" \
                     "👌 Нейтральных комментариев {}\n" \
                     "👎 Отрицательных комментариев {}\n" \
                     "‍👀 Степень уверенности в моих ответах\n" \
                     "⬆ Медианная уверенность в том, что комментарии положительные {}\n" \
                     "➡ Нейтральные {} \n" \
                     "⬇ Отрицательные {}\n" \
                     "ИТОГ!!! Видео: {}" \
            .format(scores.count, scores.count_positive, scores.count_neutral, scores.count_negative, scores.positive_pc, scores.neutral_pc, scores.negative_pc, scores.overall);
        update.message.reply_text(reply_text)


if __name__ == '__main__':
    bot = Bot(PORT, TOKEN, APP_URL, ENDPOINT, KEY, YOUTUBE_ENDPOINT, YOUTUBE_KEY)
    bot.idle()