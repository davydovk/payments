from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, ContentType

from data.config import YOUKASSA_TOKEN
from data.items import items
from loader import dp, bot
from states.test_states import Purchase


@dp.callback_query_handler(text_contains='youkassa', state=Purchase.Payment)
async def payment(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(':')[-1]
    item_id = int(item_id) - 1
    item = items[item_id]

    currency = 'RUB'
    need_name = True
    need_phone_number = False
    need_email = True
    need_shipping_address = False

    await bot.send_invoice(chat_id=call.from_user.id,
                           title=item.title,
                           description=item.title,
                           payload=str(item.id),
                           start_parameter=str(item.id),
                           currency=currency,
                           prices=[
                               LabeledPrice(label=item.title, amount=item.price * 100)
                           ],
                           provider_token=YOUKASSA_TOKEN,
                           need_name=need_name,
                           need_phone_number=need_phone_number,
                           need_email=need_email,
                           need_shipping_address=need_shipping_address)

    await Purchase.Payment_YOUKASSA.set()


@dp.pre_checkout_query_handler(state=Purchase.Payment_YOUKASSA)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id, text="Спасибо за покупку! Ожидайте отправку")


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=Purchase.Payment_YOUKASSA)
async def process_successful_payment(message: Message, state: FSMContext):
    total_amount = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    await bot.send_message(message.chat.id, f'Оплата прошла успешно.\nСпасибо за покупку'
                                            f'\nСтоимость покупки = {total_amount} {currency}')

    await state.reset_state()
