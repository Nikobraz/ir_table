import os

USERNAME = os.getenv('IR_USER')
PASSWORD = os.getenv('IR_PASS')
DB_HOST = os.getenv('DB_HOST', default='127.0.0.1')
DB_PORT = os.getenv('DB_PORT', default='5432')
DB_USER = os.getenv('DB_USER', default='postgres')
DB_PASS= os.getenv('DB_PASS', default='123456')