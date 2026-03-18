# File Tool - Herramienta de Gestion de Archivos para el Agente

## Descripcion General

`file_tool` es una herramienta especializada para el agente que permite realizar operaciones seguras y controladas con archivos en el sistema. Proporciona una interfaz robusta para crear, leer, editar y gestionar archivos, evitando los problemas de escapado y seguridad que pueden ocurrir al usar `command_tool` para estas tareas.

## Funciones Disponibles

### 1. create_file
Crea un nuevo archivo con el contenido especificado.

**Parametros:**
- `file_path` (str): Ruta completa donde crear el archivo
- `content` (str): Contenido a escribir (por defecto "")
- `force` (bool): Sobrescribir si existe (por defecto False)

**Ejemplo de uso:**
```json
{
    "type": 1,
    "agent_tool": "file_tool",
    "function": "create_file",
    "parameters": {
        "file_path": "/home/usuario/proyecto/main.py",
        "content": "print(\"Hola mundo\")
",
        "force": false
    }
}
```

### 2. read_file
Lee y retorna el contenido de un archivo.

**Parametros:**
- `file_path` (str): Ruta del archivo a leer
- `max_lines` (int, opcional): Numero maximo de lineas a mostrar

**Ejemplo:**
```json
{
    "type": 1,
    "agent_tool": "file_tool",
    "function": "read_file",
    "parameters": {
        "file_path": "/home/usuario/proyecto/main.py",
        "max_lines": 50
    }
}
```

### 3. edit_file
Reemplaza texto en un archivo existente.

**Parametros:**
- `file_path` (str): Ruta del archivo a editar
- `old_string` (str): Texto a reemplazar
- `new_string` (str): Texto nuevo
- `create_backup` (bool): Crear backup antes de editar (True por defecto)

**Ejemplo:**
```json
{
    "type": 1,
    "agent_tool": "file_tool",
    "function": "edit_file",
    "parameters": {
        "file_path": "/home/usuario/proyecto/main.py",
        "old_string": "Hola",
        "new_string": "Adios",
        "create_backup": true
    }
}
```

### 4. append_to_file
Anade contenido al final de un archivo.

**Parametros:**
- `file_path` (str): Ruta del archivo
- `content` (str): Contenido a anadir

### 5. delete_file
Elimina un archivo (requiere confirmacion explicita).

**Parametros:**
- `file_path` (str): Ruta del archivo a eliminar
- `confirm` (bool): Confirmacion obligatoria (True)

### 6. get_file_info
Obtiene informacion detallada del archivo.

**Parametros:**
- `file_path` (str): Ruta del archivo

### 7. list_files
Lista archivos en un directorio.

**Parametros:**
- `directory` (str): Directorio a listar
- `pattern` (str): Patron de busqueda ("*" por defecto)
- `recursive` (bool): Buscar recursivamente (False por defecto)

## Caracteristicas de Seguridad

### Extensiones Permitidas
```
.txt, .py, .json, .md, .csv, .log, .conf, .ini, .yaml, .yml, .html, .css, .js, .xml
```

### Rutas Prohibidas
- /etc/shadow, /etc/passwd
- /root/, /boot/, /dev/
- /proc/, /sys/

### Limites
- Tamano maximo: 10MB por archivo
- Backups automaticos en operaciones destructivas
- Validacion de permisos y existencia

## Codigos de Retorno

La herramienta siempre retorna strings descriptivos que incluyen:
- Operaciones exitosas con detalles
- Errores claramente explicados
- Estadisticas (tamano, lineas, etc.)
- Confirmacion de backups

## Ventajas sobre command_tool

| Aspecto | command_tool | file_tool |
|---------|--------------|-----------|
| Escapado de caracteres | Propenso a errores | Automatico |
| Validacion de rutas | Manual | Automatica |
| Backups | No | Si |
| Control de tamano | No | Si |
| Extensiones permitidas | No | Si |
| Info detallada | Limitada | Completa |

## Notas Importantes

- Siempre usar `force=False` a menos que se este seguro de sobrescribir
- Las operaciones de edicion crean backups automaticos por seguridad
- Verificar las extensiones permitidas antes de crear archivos
- Las rutas se validan contra la lista de rutas prohibidas
- El tamano maximo de archivo es configurable en el constructor