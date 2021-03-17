import logging
import sys
from telegram import  ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler

from lib import utils


class VatBot:

    def __init__(self):

        logging.basicConfig(filename='VAT_bot.log',
                            format='|%(asctime)s:%(msecs)d| [%(funcName)s] [%(levelname)s] - %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    def start(self, update, context):

        countries = [
            [
                InlineKeyboardButton("\U0001F1E6\U0001F1F9 Austria", callback_data='AT'),
                InlineKeyboardButton("\U0001F1E7\U0001F1EA Belgium", callback_data='BE'),
                InlineKeyboardButton("\U0001F1E7\U0001F1EC Bulgaria", callback_data='BG'),
                InlineKeyboardButton("\U0001F1E8\U0001F1FE Cyprus", callback_data='CY')
            ],
            [
                InlineKeyboardButton("\U0001F1E8\U0001F1FF Czech Republic", callback_data='CZ'),
                InlineKeyboardButton("\U0001F1E9\U0001F1EA Germany", callback_data='DE'),
                InlineKeyboardButton("\U0001F1E9\U0001F1F0 Denmark", callback_data='DK'),
                InlineKeyboardButton("\U0001F1EA\U0001F1EA Estonia", callback_data='EE')
            ],
            [
                InlineKeyboardButton("\U0001F1EC\U0001F1F7 Greece", callback_data='EL'),
                InlineKeyboardButton("\U0001F1EA\U0001F1F8 Spain", callback_data='ES'),
                InlineKeyboardButton("\U0001F1EB\U0001F1EE Finland", callback_data='FI'),
                InlineKeyboardButton("\U0001F1EB\U0001F1F7 France", callback_data='FR')
            ],
            [
                InlineKeyboardButton("\U0001F1EC\U0001F1E7 United Kingdom", callback_data='GB'),
                InlineKeyboardButton("\U0001F1ED\U0001F1F7 Croatia", callback_data='HR'),
                InlineKeyboardButton("\U0001F1ED\U0001F1FA Hungary", callback_data='HU'),
                InlineKeyboardButton("\U0001F1EE\U0001F1EA Ireland", callback_data='IE')
            ],
            [
                InlineKeyboardButton("\U0001F1EE\U0001F1F9 Italy", callback_data='IT'),
                InlineKeyboardButton("\U0001F1F1\U0001F1F9 Lithuania", callback_data='LT'),
                InlineKeyboardButton("\U0001F1F1\U0001F1FA Luxembourg", callback_data='LU'),
                InlineKeyboardButton("\U0001F1F1\U0001F1FB Latvia", callback_data='LV')
            ],
            [
                InlineKeyboardButton("\U0001F1F2\U0001F1F9 Malta", callback_data='MT'),
                InlineKeyboardButton("\U0001F1F3\U0001F1F1 Netherlands", callback_data='NL'),
                InlineKeyboardButton("\U0001F1F5\U0001F1F1 Poland", callback_data='PL'),
                InlineKeyboardButton("\U0001F1F5\U0001F1F9 Portugal", callback_data='PT')
            ],
            [
                InlineKeyboardButton("\U0001F1F7\U0001F1F4 Romania", callback_data='RO'),
                InlineKeyboardButton("\U0001F1F8\U0001F1EA Sweden", callback_data='SE'),
                InlineKeyboardButton("\U0001F1F8\U0001F1EE Slovenia", callback_data='SL'),
                InlineKeyboardButton("\U0001F1F8\U0001F1F0 Slovakia", callback_data='SK')
            ]

        ]

        r_m = InlineKeyboardMarkup(countries)

        update.message.reply_text('Please choose country:', reply_markup=r_m)

        return COUNTRY

    def button(self, update, context):

        query = update.callback_query
        query.answer()
        query.edit_message_text(text='Selected ' + query.data + ' as country,' + '\nnow please insert VAT number:')
        context.user_data["c_code"] = query.data

        return VAT

    def get_vat_info(self, update, context):

        user = update.message.from_user

        logging.info('VAT     inserted by ' + str(user) + ' >>>>> ' + str(update.message.text))
        logging.info('COUNTRY inserted by ' + str(user) + ' >>>>> ' + str(context.user_data["c_code"]))

        update.message.reply_text(utils.search_VAT_API(update.message.text, str(context.user_data["c_code"])))

        return ConversationHandler.END

    def exit(self, update, context):

        user = update.message.from_user
        logging.info('Exit user >>>>> ' + str(user.first_name))
        update.message.reply_text('Bye! Bye! ' + user.first_name + ' \U0001F917', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def credits(self, update, context):

        update.message.reply_text('buciski@vivaldi.net '
                                  '\n\nhttps://github.com/buciski/repo_bot '
                                  '\n\nVAT FAQ: https://bit.ly/2Om2H2j '
                                  '\n\nVAT info: https://bit.ly/2OPl8vZ')


if __name__ == '__main__':

    # TODO: if there is a log file take it and...take care of it :)

    bot = VatBot()
    updater = Updater(token=sys.argv[1], use_context=True)
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(CommandHandler('credits', bot.credits))

    VAT, COUNTRY = range(2)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start)],
        states={
            COUNTRY: [CallbackQueryHandler(bot.button)],
            VAT: [MessageHandler(filters=Filters.text, callback=bot.get_vat_info)]
        },
        fallbacks=[CommandHandler('exit', bot.exit)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
