# file_tool

agent tool para interactuar con archivos

## uso

{
    "type": 1,
    "agent_tool": "file_tool",
    "function": "(nombre de la funcion)",
    "parameters": (json con los parametros de la funcion)
}

## funciones

create_file:
    crea un nuevo archivo con el contenido especificado.
    parametros:
        file_path: str
        content: str
        force: bool
    retorna: str

read_file:
    lee y retorna el contenido de un archivo
    parametros:
        file_path: str
        max_lines: int
    retorna: str

edit_file:
    edita un archivo reemplazando texto
    parametros:
        file_path: str
        old_string: str
        new_string: str
        create_backup: bool
    retorna: str

append_to_file:
    anade contenido al final de un archivo
    parametros:
        file_path: str
        content: str
    retorna: str

delete_file:
    elimina un archivo
    parametros:
        file_path: str
        confirm: bool
    retorna: str

get_file_info:
    obtiene informacion detallada del archivo
    parametros:
        file_path: str
    retorna: str

list_files:
    lista archivos en un directorio
    parametros:
        directory: str
        pattern: str
        recursive: bool
    retorna: str