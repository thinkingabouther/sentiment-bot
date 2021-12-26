import os

from telegram import Update
from sentiment_aggregator import SentimentAggregator
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
APP_URL = os.environ['APP_URL']
ENDPOINT = os.environ['AZURE_ENDPOINT']
KEY = os.environ['AZURE_API_KEY']
YOUTUBE_ENDPOINT = os.environ['YOUTUBE_ENDPOINT']
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']

ENTERING_LINK, ENTERING_MAX_COMMENTS, GETTING_RESULT = range(3)


class Bot:
    def __init__(self, port, token, app_url, endpoint, key, youtube_endpoint, youtube_key):
        self.sentiment_aggregator = SentimentAggregator(endpoint, key, youtube_endpoint, youtube_key)
        self.updater = Updater(TOKEN, use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('bop', self.bop))
        dp.add_handler(CommandHandler('sentiment', self.sentiment))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                ENTERING_MAX_COMMENTS: [
                    MessageHandler(
                        Filters.text, self.enter_max_comments
                    )
                ],
                GETTING_RESULT: [
                    MessageHandler(
                        Filters.text, self.done,
                    )
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.done)],
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
        update.message.reply_text("bop умер, не пишите")

    def analyse(self):
        scores = self.sentiment_aggregator.aggregate_sentiments("dQw4w9WgXcQ")
        return "🤔 Что мы узнали:\n" \
               "🤯 Проанализировано комментариев {}\n" \
               "👍 Положительных комментариев {}\n" \
               "👌 Нейтральных комментариев {}\n" \
               "👎 Отрицательных комментариев {}\n" \
               "‍👀 Степень уверенности в моих ответах\n" \
               "⬆ Медианная уверенность в том, что комментарии положительные {}\n" \
               "➡ Нейтральные {} \n" \
               "⬇ Отрицательные {}" \
            .format(scores.count, scores.count_positive, scores.count_neutral, scores.count_negative,
                    scores.positive_pc, scores.neutral_pc, scores.negative_pc);

    def start(self, update: Update, context: CallbackContext) -> int:
        """Start the conversation and ask user for input."""
        update.message.reply_text(
            "Введите ссылку на YouTube видео"
        )
        return ENTERING_MAX_COMMENTS

    def enter_max_comments(self, update: Update, context: CallbackContext) -> int:
        """Ask the user for a max comments count."""
        context.user_data['link'] = update.message.text
        update.message.reply_text('Введите максимальное количество анализируемых комментариев')

        return GETTING_RESULT

    def done(self, update: Update, context: CallbackContext) -> int:
        """Display the result."""

        if not update.message.text[1:].isdigit():
            update.message.reply_text("Введите целое число")
            return GETTING_RESULT

        context.user_data["max_comments"] = update.message.text

        analysed_data = self.analyse()

        update.message.reply_text(
            analysed_data
        )
        context.user_data.clear()
        return ConversationHandler.END


if __name__ == '__main__':
    bot = Bot(PORT, TOKEN, APP_URL, ENDPOINT, KEY, YOUTUBE_ENDPOINT, YOUTUBE_KEY)
    bot.idle()
