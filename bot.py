import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sentiment_analyser import SentimentAnalyzer

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
APP_URL = os.environ['APP_URL']
endpoint = os.environ['AZURE_ENDPOINT']
key = os.environ['AZURE_API_KEY']
sentiment_analyser = SentimentAnalyzer(endpoint, key)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop', bop))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(APP_URL + TOKEN)
    updater.idle()


def bop(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    update.message.reply_text(sentiment_analyser.get_sentiment('Hello').sentiment)


if __name__ == '__main__':
    main()
