import requests
import pathlib

class RequestHandler:
    def __init__(self, token):
        self.token = token
        self.requst_base_url = f"https://api.telegram.org/bot{self.token}"

    def get_request_base_url(self):
        return self.requst_base_url

    def get_request_url(self, request_method):
        return f"{self.requst_base_url}/{request_method}"

    def send_non_file_request(self, request_method, **request_params):
        request_url = self.get_request_url(request_method)
        res = requests.get(request_url, json=request_params)
        return res.json()

    def send_simple_message(self, chat_id, text):
        response = self.\
            send_non_file_request('sendMessage', text=text, chat_id=chat_id)
        return response

    def send_message_wih_inline_button(self, chat_id, text, btn_text,
                                       callback_data):
        keyboard_button = {'text' : btn_text, 'callback_data' : callback_data}
        inline_keyboard = {'inline_keyboard' : [[keyboard_button]]}
        response = self.\
            send_non_file_request('sendMessage', text=text, chat_id=chat_id,
                                  reply_markup=inline_keyboard)
        return response

    def answer_callback_query(self, callback_query_id, text, show_alert=False):
        response = self.\
            send_non_file_request('answerCallbackQuery',
                                  callback_query_id=callback_query_id,
                                  text=text,
                                  show_alert=show_alert)
        return response

    def send_document(self, name, content, chat_id, **request_params):
        request_url = self.get_request_url('sendDocument')
        params = {'chat_id': chat_id, **request_params}
        files = {'document': (name, content)}
        res = requests.post(request_url, files=files, params=params)
        return res.json()

    def send_document_by_file(self, path, chat_id, **request_params):
        file_name = pathlib.PurePath(path).name
        with open(path, 'rb') as f:
            content = f.read(-1)
            self.send_document(file_name, content, chat_id, **request_params)

