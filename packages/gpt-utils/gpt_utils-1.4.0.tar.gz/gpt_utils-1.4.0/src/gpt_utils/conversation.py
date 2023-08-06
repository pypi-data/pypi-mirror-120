from .core import GPT
from .prompt import ChatPrompt


class Conversation:
    def __init__(self,
                 botname,                   # The name for the human as it shows up in GPT's prompt
                 username,                  # Similarly, the name for the human
                 *first_messages,           # A 2-tuple of messages to get things started, human first,
                                            # the second message is what the user will see when the bot
                                            # starts the chat
                 intro_text=None,           # Intro text which precedes the messages in the prompt
                 **gpt_kwargs               # kwargs for the GPT instance, note that stop will be overridden with '\n'
                 ):
        self.intro_text = intro_text
        self.username = username
        self.botname = botname
        self.messages = [first_messages]

        gpt_kwargs['stop'] = '\n'
        self.gpt = GPT(**gpt_kwargs)

    def reset(self):
        self.messages = [self.messages[0]]

    @property
    def counter(self):
        return len(self.messages) - 1

    @property
    def greeting(self):
        return self.messages[0][1]

    @property
    def prompt(self):
        return ChatPrompt(
            self.botname,
            self.username,
            *self.messages,
            intro_text=self.intro_text,
        )

    def preprocess(self, message):
        """Process message before obtaining response from GPT-3"""
        return message

    def postprocess(self, raw_response):
        """Process after before obtaining response from GPT-3"""
        return raw_response

    def response(self, message):
        message = self.preprocess(message)
        prompt = self.prompt.format(message)
        response = self.postprocess(
            self.gpt.response(prompt)
        )
        self.messages.append([message, response])
        return response

    def retry(self, temperature=None):
        if temperature:
            self.gpt.temperature = temperature
        last_human_message = self.messages[-1][0]
        self.messages.pop(-1)  # Pop last exchange
        return self.response(last_human_message)
