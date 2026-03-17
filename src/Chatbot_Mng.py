from .managers.Sel_Man import SelMan
from .managers import Utils
import random
import time
import os

class ChatbotMng:
    def __init__(self, args:tuple):
        (
            self.project_path,
            self.prompt_txt_path,
            self.driver_type,
            self.driver_path,
            self.email,
            self.password,
            self.xpath_names
        ) = args
        print(self.xpath_names)
        print(self.email)
        print(self.password)
        self.mng = SelMan(driver_path=self.driver_path, type=self.driver_type)
        self.prompt = Utils.read_prompt(self.prompt_txt_path)
        self.bot_initializer()

    def bot_initializer(self):
        self.mng.open_page("https://chat.deepseek.com/sign_in")
        self.mng.send_keys_to('xpath', self.xpath_names['email_input'], self.email, wait=random.randint(1,7))
        self.mng.send_keys_to('xpath', self.xpath_names['password_input'], self.password, wait=random.randint(1,7))
        self.mng.click_obj('xpath', self.xpath_names['login_button'], wait=random.randint(1,7))
        self.mng.click_obj('xpath', self.xpath_names['smart_search_button'], wait=random.randint(1,3))
        self.mng.click_obj('xpath', self.xpath_names['deep_thinking_button'], wait=random.randint(1,3))
        self.mng.send_keys_to('xpath', self.xpath_names['prompt_input'], self.prompt, wait=random.randint(1,7), enter=True)
        
        # para esperar a que el bot responda
        self.mng.get_text('xpath', self.xpath_names['bot_msg'])

    def bot_interaction(self, chat_msg: str) -> str:
        self.mng.send_keys_to('xpath', self.xpath_names['prompt_input'], chat_msg, wait=random.randint(1,3), enter=True)

        bot_msg = self.mng.get_text('xpath', self.xpath_names['bot_msg'])
        
        return bot_msg

    def close(self):
        self.mng.quit()