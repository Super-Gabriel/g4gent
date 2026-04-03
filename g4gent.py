import os

def read_properties(path: str, sep: str = '=', strip: bool = True) -> dict:
    config = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('#'):
                continue
            if sep in line:
                key, value = line.split(sep, 1)
                value = value.rstrip('\n')
                if strip:
                    key = key.strip()
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                config[key] = value
    return config

def build_chatbot_mng_args(project_path:str):
    # configuraciones
    config = read_properties(f"{project_path}/config.txt")
    lang = config['lang']
    xpath_names = read_properties(f"{project_path}/resources/xpath_names/deepseek_{lang}.txt")

    # para credenciales
    email = config['deepseek_email']
    password = config['deepseek_password']
    
    # para driver_type
    driver_type = config['driver']

    # para driver_path
    managers_path = f"{project_path}/src/managers/"
    driver_path = (
        f"{managers_path}msedgedriver.exe" if driver_type == 'edge' else
        f"{managers_path}chromedriver.exe" if driver_type == 'chrome' else
        f"" if driver_type == 'firefox' else
        ""
    )
    prompt_txt_path = f"{project_path}/resources/initial_prompt_2.txt"
    
    return (
        project_path,
        prompt_txt_path,
        driver_type,
        driver_path,
        email,
        password,
        xpath_names,
    )

if __name__ == "__main__":
    from src.Driver import Driver
    project_path = os.getcwd() + "/"
    dv = Driver(build_chatbot_mng_args(project_path))
    dv.main()