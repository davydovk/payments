from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура для оплаты
def buy_keyboard(item_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    qiwi_btn = InlineKeyboardButton(text='Qiwi', callback_data=f'qiwi:{item_id}')
    youkassa_btn = InlineKeyboardButton(text='ЮKassa', callback_data=f'youkassa:{item_id}')

    keyboard.add(qiwi_btn, youkassa_btn)

    return keyboard


# Клавиатура для проверки оплаты через qiwi
paid_keyboard = InlineKeyboardMarkup(row_width=1)

paid_btn = InlineKeyboardButton(text='Оплатил', callback_data='paid')
cancel_btn = InlineKeyboardButton(text='Отмена', callback_data='cancel')

paid_keyboard.add(paid_btn, cancel_btn)
