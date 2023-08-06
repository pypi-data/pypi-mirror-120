from .utilities import get_listening_url
from .request_handler import RequestHandler
from .update_handler import UpdateAgent

class Bot:
    def __init__(self, token:str):
        self.token = token
        self.request_handler = RequestHandler(token)

    def setup_listening(self, listening_endpoint: str,
                        base_url: str,
                        telegram_update_handler,
                        also_set_webhook=True):
        self.listening_url = get_listening_url(base_url, listening_endpoint)
        self.update_handler = UpdateAgent(self.token,
                                          listening_endpoint,
                                          telegram_update_handler)
        if also_set_webhook:
            self.reset_webhook()
        self.flask_app = self.update_handler.setup()

    def reset_webhook(self):
        self.remove_set_webhook()
        self.set_webhook()

    def set_webhook(self):
        # Refactor
        #TODO: Check res
        res = self.request_handler.\
            send_non_file_request('setWebhook', url=self.listening_url)
        print(res)

    def remove_set_webhook(self):
        #TODO: Check res
        res = self.request_handler.\
            send_non_file_request('setWebhook', url='')

    def get_app(self):
        return self.flask_app

    # Use this only for development/testing purposes
    def listen(self, host, port, cert_path, key_path):
        self.flask_app.run(host, port, ssl_context=(cert_path, key_path))

class PrintUpdateBot:
    def __init__(self, token, listening_endpoint, base_url):
        self.bot = Bot(token)
        def update_handler(telegram_update):
            print(telegram_update)
        self.bot.setup_listening(listening_endpoint, base_url, update_handler)

    def listen(self, host, port, cert_path, key_path):
        self.bot.listen(host, port, cert_path, key_path)
    
