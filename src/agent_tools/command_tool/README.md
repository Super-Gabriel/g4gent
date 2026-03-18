# command_tool

agent tool para interactuar con el sistema operativo

# uso

{
    "type": 1,
    "agent_tool": "command_tool",
    "function": (funcion a ejecutar),
    "parameters": (json con los parametros de la funcion)
}

# funciones

execute_command:
    ejecuta un comando en el sistema operativo
    parametros:
        cmd_list: list
        timeout: int
    retorna:
        str