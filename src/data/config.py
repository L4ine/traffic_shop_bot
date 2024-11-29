from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

DATABASE_HOST = getenv('POSTGRES_HOST')
DATABASE_NAME = getenv('POSTGRES_DB')
DATABASE_USER = getenv('POSTGRES_USER')
DATABASE_PASS = getenv('POSTGRES_PASSWORD')

DATABASE_URL = 'postgresql+asyncpg://{user}:{passw}@{host}/{name}'.format(
	user=DATABASE_USER,
	passw=DATABASE_PASS,
	host=DATABASE_HOST,
	name=DATABASE_NAME
)

BOT_TOKEN = getenv('BOT_TOKEN')

YOOKASSA_SHOP_ID = getenv('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = getenv('YOOKASSA_SECRET_KEY')

XRAY_URL = getenv('XRAY_URL')

COOKIE = getenv('COOKIE')

TARIFFS = {
	1: {'name': '1 месяц', 'amount': '200.00'},
	3: {'name': '3 месяца', 'amount': '550.00'},
	6: {'name': '6 месяцев', 'amount': '1100.00'},
	12: {'name': '12 месяцев', 'amount': '2000.00'},
}
