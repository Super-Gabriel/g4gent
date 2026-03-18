import json

def read_prompt(txt_path: str):
    prompt = read_txt(txt_path)
    prompt = delete_line_breaks(prompt)
    return prompt

# método que lee un archivo .txt
def read_txt(txt_path: str):
    content = None
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as txt:
            content = txt.read()
    except Exception as e:
        print(f'Error al leer el txt: {e}')

    return content

# método para borrar los saltos de línea de un texto
def delete_line_breaks(text: str):
    formatted_text = text.replace('\n', ' ').replace('\r', ' ')
    
    return formatted_text

# método que convierte un string en un diccionario
def str_to_dict(string: str):
    try:
        dict = json.loads(string)
        return dict
    except Exception as e:
        print(f"error en str_to_dict: {e}")
        return e