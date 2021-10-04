from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hcode, hlink

from data import config
from data.items import items
from keyboards.inline.purchases_keyboard import buy_keyboard, paid_keyboard
from loader import dp
from states.test_states import Purchase
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.message_handler(Command('payment'))
async def show_items(message: types.Message, state: FSMContext):
    caption = """
Название продукта: {title}
<i>Описание:</i>
{description}

<u>Цена:</u> {price:.2f} <b>RUB</b>
"""

    for item in items:
        await message.answer_photo(
            photo=item.photo_link,
            caption=caption.format(
                title=item.title,
                description=item.description,
                price=item.price,
            ),
            reply_markup=buy_keyboard(item_id=item.id)
        )

    await Purchase.Payment.set()
