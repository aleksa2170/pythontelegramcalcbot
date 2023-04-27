from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext


# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    # Создание клавиатуры с выбором операций
    keyboard = [
        [
            InlineKeyboardButton("Умножение", callback_data='multiply'),
            InlineKeyboardButton("Деление", callback_data='divide')
        ],
        [
            InlineKeyboardButton("Сложение", callback_data='add'),
            InlineKeyboardButton("Вычитание", callback_data='subtract')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправка сообщения с клавиатурой
    update.message.reply_text('Выберите операцию:', reply_markup=reply_markup)


# Обработчик кнопок
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    # Сохранение выбранной операции в контексте пользователя
    context.user_data['operation'] = query.data
    # Запрос ввода первого числа
    query.edit_message_text(text="Введите первое число (используйте запятую в качестве разделителя):")


# Обработчик ввода чисел
def number_input(update: Update, context: CallbackContext):
    # Проверка, было ли введено первое число
    if 'first_number' not in context.user_data:
        try:
            # Преобразование числа из текста и сохранение в контексте пользователя
            context.user_data['first_number'] = float(update.message.text.replace(',', '.'))
            # Запрос ввода второго числа
            update.message.reply_text("Введите второе число (используйте запятую в качестве разделителя):")
        except ValueError:
            # Обработка некорректного ввода
            update.message.reply_text("Пожалуйста, введите корректное число.")
    else:
        try:
            # Преобразование числа из текста и сохранение в контексте пользователя
            context.user_data['second_number'] = float(update.message.text.replace(',', '.'))
            # Выполнение выбранной операции и отправка результата
            if context.user_data['operation'] == 'multiply':
                result = context.user_data['first_number'] * context.user_data['second_number']
            elif context.user_data['operation'] == 'divide':
                result = context.user_data['first_number'] / context.user_data['second_number']
            elif context.user_data['operation'] == 'add':
                result = context.user_data['first_number'] + context.user_data['second_number']
            elif context.user_data['operation'] == 'subtract':
                result = context.user_data['first_number'] - context.user_data['second_number']

            # Отправка результата операции с округлением до двух знаков после запятой
            update.message.reply_text("Результат: {:.2f}".format(result))
            # Очистка данных пользователя
            context.user_data.clear()

        except ValueError:
            # Обработка некорректного ввода
            update.message.reply_text("Пожалуйста, введите корректное число.")


# Команда /help
def help_command(update: Update):
    update.message.reply_text('Введите /start чтобы начать использовать калькулятор.')


def main():
    # Добавляем токен нашего бота
    TOKEN = "6136074126:AAHz1_ap2hUegoPNqHbgDyiJmpK0-U_FL3k"
    updater = Updater(token=TOKEN, use_context=True)

    # Регистрация обработчиков команд и кнопок
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, number_input))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
