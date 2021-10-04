from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode, hlink

from data import config
from data.items import items
from keyboards.inline.purchases_keyboard import paid_keyboard
from loader import dp
from states.test_states import Purchase
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text_contains='qiwi', state=Purchase.Payment)
async def create_invoice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(':')[-1]
    item_id = int(item_id) - 1
    item = items[item_id]

    amount = item.price
    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        '\n'.join([
            f'Оплатите не менее {amount:.2f} по номеру телефона или по адресу',
            '',
            hlink(config.WALLET_QIWI, url=payment.invoice),
            'И обязательно укажите ID платежа:',
            hcode(payment.id)
        ]),
        reply_markup=paid_keyboard)

    await Purchase.Payment_QIWI.set()
    await state.update_data(payment=payment)

    @dp.callback_query_handler(text='cancel', state=Purchase.Payment_QIWI)
    async def cancel_payment(call: types.CallbackQuery, state: FSMContext):
        await call.message.edit_text('Отменено')
        await state.finish()

    @dp.callback_query_handler(text='paid', state=Purchase.Payment_QIWI)
    async def approve_payment(call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        payment: Payment = data.get('payment')
        try:
            payment.check_payment()
        except NoPaymentFound:
            await call.message.answer('Транзакция не найдена.')
            return
        except NotEnoughMoney:
            await call.message.answer('Оплаченная сума меньше необходимой.')
            return

        else:
            await call.message.answer('Успешно оплачено')
        await call.message.edit_reply_markup()
        await state.finish()
