from .managers.Sel_Man import SelMan
from .managers.Utils import Utils
import random
import time
import os

class ChatbotMng:
    def __init__(self, args:tuple):
        (
            self.project_path,
            self.prompt_txt_path,
            self.edge_driver_path
        ) = args

        self.email = os.getenv('DEEPSEEK_EMAIL')
        self.password = os.getenv('DEEPSEEK_PASSWORD')

        self.mng = SelMan(self.edge_driver_path, type='edge')

        self.prompt = Utils.read_prompt(self.prompt_txt_path)

        self.bot_initializer()

    def bot_initializer(self):
        self.mng.open_page("https://chat.deepseek.com/sign_in")
        self.mng.send_keys_to('xpath', "//input[@placeholder='Número de teléfono / dirección de correo']", self.email, wait=random.randint(1,10))
        self.mng.send_keys_to('xpath', "//input[@placeholder='Contraseña']", self.password, wait=random.randint(1,10))
        self.mng.click_obj('xpath', "//span[text()='Iniciar sesión']", wait=random.randint(1,10))
        self.mng.send_keys_to('xpath', "//textarea[@class='_27c9245 ds-scroll-area ds-scroll-area--show-on-focus-within d96f2d2a']", self.prompt, wait=random.randint(1,10), enter=True)
        time.sleep(10)

    def bot_interaction(self, chat_msg: str) -> str:
        self.mng.send_keys_to('xpath', "//textarea[@class='_27c9245 ds-scroll-area ds-scroll-area--show-on-focus-within d96f2d2a']", chat_msg, wait=random.randint(1,10), enter=True)

        bot_msg = self.mng.get_text('css_selector', "._4f9bf79.d7dc56a8._43c05b5", wait=5)
        
        return bot_msg

    def close(self):
        self.mng.quit()