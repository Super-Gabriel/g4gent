# g4gent

Implementación propia de un agente de IA con Python que interactúa con modelos de lenguaje (como DeepSeek) mediante Selenium y ejecuta herramientas del sistema.

## Descripción general

El agente utiliza Selenium para conectarse a DeepSeek, iniciar sesión, enviar prompts y recibir respuestas. Las respuestas del modelo se procesan en formato JSON, pudiendo ser mensajes para el usuario o solicitudes de ejecución de herramientas (como el explorador de archivos). Actualmente cuenta con un explorador de archivos Linux que permite ejecutar comandos en el sistema.

## Estructura del proyecto

- src/Chatbot_Mng.py: Gestiona la interacción con DeepSeek.
- src/Driver.py: Controlador principal que orquesta el bucle de conversación y ejecuta herramientas.
- src/agent_tools/: Contiene herramientas del agente (ej. file_explorer).
- src/managers/: Módulos auxiliares (Selenium, utilidades).
- resources/: Recursos adicionales.
- Archivos de configuración: config.txt, .env, etc.

## Estado de implementación

- [x] conexión al modelo de lenguaje mediante selenium
- [ ] creación de módulos tipo MCP
