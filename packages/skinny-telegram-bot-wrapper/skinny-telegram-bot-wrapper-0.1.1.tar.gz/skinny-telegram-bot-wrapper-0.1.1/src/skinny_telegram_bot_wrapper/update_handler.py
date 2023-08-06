from pprint import pprint
from flask import Flask, request as flask_request
from src.skinny_telegram_bot_wrapper.request_handler import RequestHandler
import requests


class UpdateAgent:
    def __init__(self, token: str, listening_endpoint: str,
                 telegram_update_handler):
        self.listening_endpoint = listening_endpoint
        self.telegram_update_handler = telegram_update_handler
        self.flask_app = Flask(__name__)

    # update_handler is a function that takes the full telegram response as an
    # dict, For more info refer to telegram_update_handlers module

    def setup(self):
        self._set_update_handler(self.listening_endpoint , self.telegram_update_handler)
        return self.flask_app

    def _update_handler_wrapper(self, update_handler):
        def result_func():
            update_handler(flask_request.json)
            return ''
        return result_func

    def _set_update_handler(self, listening_endpoint, update_handler):
        self.flask_app.add_url_rule(
            listening_endpoint,
            'update_handler',
            self._update_handler_wrapper(update_handler),
            methods=['GET', 'POST'])

    def get_app(self):
        return self.flask_app
