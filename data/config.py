from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста


# Параметры для работы с оплатой QIWI
QIWI_TOKEN = env.str('QIWI_TOKEN')
WALLET_QIWI = env.str('WALLET')
QIWI_PUBKEY = env.str('QIWI_P_PUB')
