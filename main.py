import telebot
import threading
import time

import config
import functions
import keyboards


threading.Thread(daemon=True, target=functions.set_basic_exchange_rate).start()
threading.Thread(daemon=True, target=functions.set_specific_exchange_rate).start()

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    time.sleep(30)
    rates = functions.currency_rate_message()

    rates_message = bot.send_message(chat_id=config.CHANNEL_ID,
                                     text=rates,
                                     reply_markup=keyboards.main_keyboard(),
                                     parse_mode='Markdown',
                                     message_thread_id=2,
                                     )
    
    bot.pin_chat_message(chat_id=config.CHANNEL_ID,
                        message_id=rates_message.id,
                        disable_notification=True,
                        )
    
    while True:
        time.sleep(60)

        rates = functions.currency_rate_message()

        bot.edit_message_text(chat_id=config.CHANNEL_ID,
                              message_id=rates_message.id,
                              text=rates,
                              parse_mode='Markdown',
                              )
        bot.edit_message_reply_markup(chat_id=config.CHANNEL_ID,
                                      message_id=rates_message.id,
                                      reply_markup=keyboards.main_keyboard(),
                                      )


# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     print(message)


# @bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
# @bot.channel_post_handler()
# def channel_post(message):
#     print(message.text)

if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass
