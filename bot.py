import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from sentiment_analyser import SentimentAnalyzer
from urllib.parse import urlparse

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
APP_URL = os.environ['APP_URL']
ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_API_KEY']

ENTERING_LINK, ENTERING_MAX_COMMENTS, GETTING_RESULT = range(3)

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Введите ссылку на YouTube видео"
    )
    return ENTERING_MAX_COMMENTS
    

def enter_max_comments(update: Update, context: CallbackContext) -> int:
    """Ask the user for a max comments count."""
    context.user_data['link'] = update.message.text
    update.message.reply_text('Введите максимальное количество анализируемых комментариев')

    return GETTING_RESULT

def done(update: Update, context: CallbackContext) -> int:
    """Display the result."""

    if not update.message.text[1:].isdigit():
        update.message.reply_text("Введите целое число")
        return GETTING_RESULT

    context.user_data["max_comments"] = update.message.text
    
    update.message.reply_text(
        context.user_data["max_comments"] + " " + context.user_data["link"]
    )
    context.user_data.clear()
    return ConversationHandler.END

class Bot:
    def __init__(self, port, token, app_url, endpoint, key):
        self.sentiment_analyser = SentimentAnalyzer(endpoint, key)
        self.updater = Updater(TOKEN, use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('bop', self.bop))
        dp.add_handler(CommandHandler('sentiment', self.sentiment))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                ENTERING_MAX_COMMENTS: [
                    MessageHandler(
                        Filters.text, enter_max_comments
                    )
                ],
                GETTING_RESULT: [
                    MessageHandler(
                        Filters.text, done,
                    )
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        )

        dp.add_handler(conv_handler)


        self.updater.start_webhook(listen="0.0.0.0",
                                   port=int(port),
                                   url_path=token)
        self.updater.bot.setWebhook(app_url + token)
        self.updater.start_polling()

    def idle(self):
        self.updater.idle()

    def bop(self, update: Update, context: CallbackContext):
        docs_list = ['Hello', 'You are fucking retarded!']
        results = self.sentiment_analyser.get_sentiment(docs_list)
        for result in results:
            update.message.reply_text(result.sentiment)

    def sentiment(self, update: Update, context: CallbackContext):
        raw_url = update.message.text
        url = urlparse(raw_url)
        update.message.reply_text(url.netloc + url.path)

if __name__ == '__main__':
    bot = Bot(PORT, TOKEN, APP_URL, ENDPOINT, KEY)
    bot.idle()
