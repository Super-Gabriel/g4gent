import os

def build_chatbot_mng_args(project_path:str):
    return (
        project_path,
        f"{project_path}/resources/initial_context_prompt.txt",
        f"{project_path}/drivers/msedgedriver.exe"
    )

if __name__ == "__main__":
    from src.Driver import Driver
    project_path = os.getcwd() + "/"
    dv = Driver(build_chatbot_mng_args(project_path))
    dv.test()