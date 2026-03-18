import os
import subprocess

class linux_tools:
    def __init__(self):
        self.forbidden_commands = ["rm", "rm -rf", "sudo"]
        pass
    
    def test(self):
        return "test"

    def execute_command(self, cmd_list:list, timeout=10):
        try:
            for cmd in self.forbidden_commands:
                if cmd in cmd_list:
                    return "Error: comando prohibido."
            
            proc = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
            output = proc.stdout + proc.stderr
            return f"Código de retorno: {proc.returncode}\n{output}"
        except subprocess.TimeoutExpired:
            return "Error: comando excedió el tiempo límite."
        except Exception as e:
            return f"Error al ejecutar comando: {e}"