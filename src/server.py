from routes import register_routes

from typing import Callable
from flask import Flask
from flask_cors import CORS
from waitress import serve
from os import getenv as env
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))


class FlaskServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.host = env('SERVER_HOST', 'localhost')
        self.port = env('SERVER_PORT', '5000')
        CORS(self.app)

    def register_routes(self, endpoint: str, name: str, handler: Callable, methods: list = ['POST', 'GET']):
        self.app.add_url_rule(endpoint, name, handler, methods=methods)

    def start(self):
        serve(self.app, host=self.host, port=self.port, threads=1)


if __name__ == '__main__':
    server = FlaskServer()

    register_routes(server)

    server.start()
