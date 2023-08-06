from enum import Enum

class UpdateTypes(Enum):
    message = 'message'
    edited_message = 'edited_message'
    channel_post = 'channel_post'
    channel_edited_post = 'channel_edited_post'
    inline_query = 'inline_query'
    choosen_inline_query = 'choosen_inline_query'
    callback_query = 'callback_query'
    other = 'other'


class TelegramUpdate:
    def __init__(self, telegram_update):
        self.update = telegram_update

    def get_type(self):
        if 'message' in self.update:
            return UpdateTypes.message
        elif 'edited_message' in self.update:
            return UpdateTypes.edited_message
        elif 'channel_post' in self.update:
            return UpdateTypes.channel_post
        elif 'channel_edited_post' in self.update:
            return UpdateTypes.channel_edited_post
        elif 'inline_query' in self.update:
            return UpdateTypes.inline_query
        elif 'choosen_inline_query' in self.update:
            return UpdateTypes.choosen_inline_query
        elif 'callback_query' in self.update:
            return UpdateTypes.callback_query
        else:
            return UpdateTypes.other

    # This would return Message object for updates of message type and so on.
    def get_content(self):
        update_type = self.get_type()
        return self.update[update_type.value]

def null_responder(content):
    pass

class TelegramUpdateHandlerFactory:
    def __init__(self, all_responder=null_responder,
                 message_responder=null_responder,
                 edited_message_responder=null_responder,
                 channel_post_responder=null_responder,
                 channel_edited_post_responder=null_responder,
                 inline_query_responder=null_responder,
                 choosen_inline_query_responder=null_responder,
                 callback_query_responder=null_responder,
                 other_responder=null_responder):
        self.all_responder = all_responder
        self.message_responder = message_responder
        self.edited_message_responder = edited_message_responder
        self.channel_post_responder = channel_post_responder
        self.channel_edited_post_responder = channel_edited_post_responder
        self.inline_query_responder = inline_query_responder
        self.choosen_inline_query_responder = choosen_inline_query_responder
        self.callback_query_responder = callback_query_responder
        self.other_responder = other_responder

    def get_update_handler(self):
        def resulting_update_handler(telegram_update):
            update = TelegramUpdate(telegram_update)
            update_type = update.get_type()
            self.all_responder(update.get_content())
            if update_type == UpdateTypes.message:
                self.message_responder(update.get_content())
            if update_type == UpdateTypes.edited_message:
                self.edited_message_responder(update.get_content())
            if update_type == UpdateTypes.channel_post:
                self.channel_post_responder(update.get_content())
            if update_type == UpdateTypes.channel_edited_post:
                self.channel_edited_post_responder(update.get_content())
            if update_type == UpdateTypes.inline_query:
                self.inline_query_responder(update.get_content())
            if update_type == UpdateTypes.choosen_inline_query:
                self.choosen_inline_query_responder(update.get_content())
            if update_type == UpdateTypes.callback_query:
                self.callback_query_responder(update.get_content())
            if update_type == UpdateTypes.other:
                self.other_responder(update.get_content())

        return resulting_update_handler






def print_update_type_handler(telegram_update):
    update = TelegramUpdate(telegram_update)
    print(update.get_type().value)

