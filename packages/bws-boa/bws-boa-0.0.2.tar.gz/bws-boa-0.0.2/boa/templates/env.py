template = """
MYSQL_NAME=ms-name
MYSQL_USER=ms-user
MYSQL_PASSWORD=ms-pass
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306

JWT_SECRET_KEY=%(secret)s

REGISTER = http://ip_node:5555/ms/register
MS_HOST = https://ip_ms:5000

HOST = "localhost"
PORT = 5000
"""
