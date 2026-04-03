from .Chatbot_Mng import ChatbotMng
from .agent_tools.command_tool.command_tool import linux_tools
from .agent_tools.file_tool.file_tool import file_tool
from .managers import Utils 

class Driver:
    def __init__(self, chatbot_mng_args:tuple):
        self.chatbot_mng_args = chatbot_mng_args

    def main(self):
        print("\n\nIniciando agente...\n\n")
        chatbot_mng = ChatbotMng(self.chatbot_mng_args)

        while True:
            iteration = 1
            prompt = "usuario: "+ input("Prompt >> ")
            print("\n")
            ai_response = chatbot_mng.bot_interaction(prompt)
            action = self.process_ai_response(ai_response)
            while action:
                print(f"Ejecutando acciones, iteracion: {iteration} ...")
                iteration += 1
                ai_response = chatbot_mng.bot_interaction(action)
                action = self.process_ai_response(ai_response)

    def process_ai_response(self, ai_response:str):
        ai_response = Utils.str_to_dict(ai_response)
        if not isinstance(ai_response, dict):
            return f"sistema: error en la ultima respuesta, formato json salió incompleto o con errores, mensaje: {ai_response}"
        if ai_response['type'] == 0:
            print(f"\n\n{ai_response['response']}\n\n")
        elif ai_response['type'] == 1:
            print(f"\n{ai_response['description']}")
            agent_tool = ai_response['agent_tool']
            function = ai_response['function']
            parameters = ai_response['parameters']
            
            tool_response = "sin respuesta"
            if agent_tool == "command_tool":
                l_tools = linux_tools()
                if function == "execute_command":
                    tool_response = l_tools.execute_command(parameters['cmd_list'], parameters['timeout'])
            
            if agent_tool == "file_tool":
                f_tools = file_tool()
                if function == "create_file":
                    tool_response = f_tools.create_file(parameters['file_path'], parameters['content'], parameters['force'])
                elif function == "read_file":
                    tool_response = f_tools.read_file(parameters['file_path'])
                elif function == "edit_file":
                    tool_response = f_tools.edit_file(parameters['file_path'], parameters['old_string'], parameters['new_string'], parameters['create_backup'])
                elif function == "delete_file":
                    tool_response = f_tools.delete_file(parameters['file_path'], parameters['confirm'])
                elif function == "get_file_info":
                    tool_response = f_tools.get_file_info(parameters['file_path'])
                elif function == "list_files":
                    tool_response = f_tools.list_files(parameters['directory'], parameters['pattern'], parameters['recursive'])

            return f"{agent_tool}: {tool_response}"
        