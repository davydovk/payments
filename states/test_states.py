from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    Payment = State()
    Send_Invoice = State()
    Payment_QIWI = State()
    Payment_YOUKASSA = State()
