from .Chatbot_Mng import ChatbotMng

class Driver:
    def __init__(self, chatbot_mng_args:tuple):
        self.chatbot_mng_args = chatbot_mng_args

    def main(self):
        chatbot_mng = ChatbotMng(self.chatbot_mng_args)

        while True:
            prompt = input("Prompt >> ")
            if prompt == "exit":
                break
            ai_response = chatbot_mng.bot_interaction(prompt)
            print(ai_response)