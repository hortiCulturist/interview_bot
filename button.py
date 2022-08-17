from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def interview():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Почати опитування'))
    return m


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('ОТМЕНА'))
    return m


def yes_no():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('✅ Так', callback_data='yes_yes'))
    m.insert(InlineKeyboardButton('❌ Нi', callback_data='nope'))
    return m


def next():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('Розвінчати міф', callback_data='nxt'))
    return m


def end():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('Закінчити опитування', callback_data='endd'))
    return m


def axxe(count, message):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.add(InlineKeyboardButton('Надіслати другу', switch_inline_query=f'- бот у якому я пройшла опитування.\n'
                                                                      f'Mій результат - {count} балів(-и)!!\n\n{message}\n\n'))
    m.add(InlineKeyboardButton('Дізнатися більше', url='https://compendium.com.ua/dec/545877/'))
    m.add(InlineKeyboardButton('Пройти опитування знову', callback_data='start_again'))
    return m