import os
import dotenv

def build_chatbot_mng_args(project_path:str):
    email = os.getenv('DEEPSEEK_EMAIL')
    password = os.getenv('DEEPSEEK_PASSWORD')
    return (
        project_path,
        f"{project_path}/resources/initial_context_prompt.txt",
        f"{project_path}/src/managers/msedgedriver.exe",
        email,
        password
    )

if __name__ == "__main__":
    dotenv.load_dotenv()
    from src.Driver import Driver
    project_path = os.getcwd() + "/"
    dv = Driver(build_chatbot_mng_args(project_path))
    dv.main()