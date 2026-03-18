import os
import shutil
from pathlib import Path
import datetime
import stat

class file_tool:
    def __init__(self):
        self.allowed_extensions = [".txt", ".py", ".json", ".md", ".csv", ".log", ".conf", ".ini", ".yaml", ".yml", ".html", ".css", ".js", ".xml"]
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.forbidden_paths = ["/etc/shadow", "/etc/passwd", "/root/", "/boot/", "/dev/", "/proc/", "/sys/"]
        
    def _is_path_allowed(self, file_path: str) -> tuple:
        """Verifica si la ruta está permitida por seguridad"""
        path = Path(file_path).resolve()
        for forbidden in self.forbidden_paths:
            if str(path).startswith(forbidden):
                return (False, f"Acceso denegado: {forbidden} no está permitido")
        return (True, "")
    
    def _check_extension(self, file_path: str) -> tuple:
        """Verifica si la extensión del archivo está permitida"""
        ext = Path(file_path).suffix.lower()
        if ext and ext not in self.allowed_extensions:
            return (False, f"Extensión {ext} no permitida. Extensiones permitidas: {', '.join(self.allowed_extensions)}")
        return (True, "")
    
    def create_file(self, file_path: str, content: str = "", force: bool = False) -> str:
        """Crea un archivo con el contenido especificado"""
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            allowed, msg = self._check_extension(file_path)
            if not allowed:
                return f"Error: {msg}"
            
            path = Path(file_path)
            
            if len(content.encode('utf-8')) > self.max_file_size:
                return "Error: El contenido excede el tamaño máximo permitido (10MB)"
            
            if path.exists() and not force:
                return f"Error: El archivo {file_path} ya existe. Usa force=True para sobrescribir"
            
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Archivo creado exitosamente: {file_path}\nTamaño: {len(content)} bytes\nFecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
        except Exception as e:
            return f"Error creando archivo: {str(e)}"
    
    def read_file(self, file_path: str, max_lines: int = None) -> str:
        """Lee y retorna el contenido de un archivo"""
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(file_path)
            
            if not path.exists():
                return f"Error: El archivo {file_path} no existe"
            
            if not path.is_file():
                return f"Error: {file_path} no es un archivo"
            
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return "Error: El archivo excede el tamaño máximo permitido (10MB)"
            
            with open(path, 'r', encoding='utf-8') as f:
                if max_lines:
                    lines = []
                    for i, line in enumerate(f):
                        if i >= max_lines:
                            line_count = self._count_lines(file_path)
                            lines.append(f"\n... (archivo truncado, mostrando {max_lines} de {line_count} líneas)")
                            break
                        lines.append(line.rstrip())
                    content = "\n".join(lines)
                else:
                    content = f.read()
            
            stat_info = path.stat()
            mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            
            return f"Contenido de {file_path}:\n" + "="*50 + f"\n{content}\n" + "="*50 + f"\nTamaño: {file_size} bytes\nModificado: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
        except UnicodeDecodeError:
            return "Error: No se puede leer el archivo como texto (posiblemente binario)"
        except Exception as e:
            return f"Error leyendo archivo: {str(e)}"
    
    def edit_file(self, file_path: str, old_string: str, new_string: str, create_backup: bool = True) -> str:
        """Reemplaza texto en un archivo"""
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(file_path)
            
            if not path.exists():
                return f"Error: El archivo {file_path} no existe"
            
            if not path.is_file():
                return f"Error: {file_path} no es un archivo"
            
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return "Error: El archivo excede el tamaño máximo permitido (10MB)"
            
            if create_backup:
                backup_path = path.with_suffix(path.suffix + '.backup')
                shutil.copy2(path, backup_path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            occurrences = content.count(old_string)
            
            if occurrences == 0:
                return f"No se encontró '{old_string}' en el archivo"
            
            new_content = content.replace(old_string, new_string)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            result = f"Archivo editado exitosamente: {file_path}\nReemplazos realizados: {occurrences}"
            if create_backup:
                result += f"\nBackup creado: {backup_path}"
            
            return result
            
        except Exception as e:
            return f"Error editando archivo: {str(e)}"
    
    def append_to_file(self, file_path: str, content: str) -> str:
        """Añade contenido al final de un archivo existente"""
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(file_path)
            
            if not path.exists():
                return self.create_file(file_path, content)
            
            current_size = path.stat().st_size
            new_size = current_size + len(content.encode('utf-8'))
            if new_size > self.max_file_size:
                return "Error: El archivo excedería el tamaño máximo permitido después del append"
            
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            
            return f"Contenido añadido a {file_path} (nuevo tamaño: {new_size} bytes)"
            
        except Exception as e:
            return f"Error añadiendo contenido: {str(e)}"
    
    def _count_lines(self, file_path: str) -> int:
        """Cuenta el número de líneas en un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except:
            return 0
    
    def delete_file(self, file_path: str, confirm: bool = True) -> str:
        """Elimina un archivo (con confirmación explícita)"""
        if not confirm:
            return "Error: Se requiere confirmación explícita para eliminar archivos (confirm=True)"
        
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(file_path)
            
            if not path.exists():
                return f"Error: El archivo {file_path} no existe"
            
            if not path.is_file():
                return f"Error: {file_path} no es un archivo"
            
            backup_path = path.with_suffix(path.suffix + '.deleted.backup')
            shutil.copy2(path, backup_path)
            
            os.remove(path)
            
            return f"Archivo eliminado: {file_path}\nBackup guardado en: {backup_path}"
            
        except Exception as e:
            return f"Error eliminando archivo: {str(e)}"
    
    def get_file_info(self, file_path: str) -> str:
        """Retorna información detallada del archivo"""
        try:
            allowed, msg = self._is_path_allowed(file_path)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(file_path)
            
            if not path.exists():
                return f"Error: El archivo {file_path} no existe"
            
            stat_info = path.stat()
            
            info = f"Información de: {file_path}\n"
            info += "="*50 + "\n"
            info += f"Tamaño: {stat_info.st_size} bytes ({stat_info.st_size/1024:.2f} KB)\n"
            info += f"Creado: {datetime.datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            info += f"Modificado: {datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            info += f"Accedido: {datetime.datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            info += f"Permisos: {oct(stat_info.st_mode)[-3:]}\n"
            info += f"Propietario UID: {stat_info.st_uid}\n"
            info += f"Grupo GID: {stat_info.st_gid}\n"
            info += f"Enlaces duros: {stat_info.st_nlink}\n"
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                info += f"Líneas: {line_count}\n"
            except:
                info += "Líneas: No aplica (archivo binario)\n"
            
            return info
            
        except Exception as e:
            return f"Error obteniendo información: {str(e)}"
    
    def list_files(self, directory: str, pattern: str = "*", recursive: bool = False) -> str:
        """Lista archivos en un directorio"""
        try:
            allowed, msg = self._is_path_allowed(directory)
            if not allowed:
                return f"Error de seguridad: {msg}"
            
            path = Path(directory)
            
            if not path.exists():
                return f"Error: El directorio {directory} no existe"
            
            if not path.is_dir():
                return f"Error: {directory} no es un directorio"
            
            if recursive:
                files = list(path.rglob(pattern))
            else:
                files = list(path.glob(pattern))
            
            dirs = [f for f in files if f.is_dir()]
            files = [f for f in files if f.is_file()]
            
            result = f"Directorio: {directory}\n"
            result += "="*50 + "\n"
            
            if dirs:
                result += "\nDIRECTORIOS:\n"
                for d in sorted(dirs):
                    result += f"  {d.name}/\n"
            
            if files:
                result += "\nARCHIVOS:\n"
                for f in sorted(files):
                    size = f.stat().st_size
                    size_str = f"{size} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                    result += f"  {f.name} ({size_str})\n"
            
            result += f"\nTotal: {len(dirs)} directorios, {len(files)} archivos"
            
            return result
            
        except Exception as e:
            return f"Error listando archivos: {str(e)}"

if __name__ == "__main__":
    print("="*60)
    print("INICIANDO PRUEBAS UNITARIAS DE FILE_TOOL")
    print("="*60)
    
    ft = file_tool()
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    
    print(f"\nDirectorio de pruebas: {test_dir}")
    
    print("\n" + "-"*40)
    print("PRUEBA 1: Crear archivo")
    print("-"*40)
    test_file = test_dir / "test1.txt"
    result = ft.create_file(str(test_file), "Hola mundo\nEsta es una prueba\nLínea 3")
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 2: Leer archivo")
    print("-"*40)
    result = ft.read_file(str(test_file))
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 3: Editar archivo")
    print("-"*40)
    result = ft.edit_file(str(test_file), "Hola mundo", "Hola FILE_TOOL")
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 4: Añadir contenido")
    print("-"*40)
    result = ft.append_to_file(str(test_file), "\nLínea añadida al final")
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 5: Información del archivo")
    print("-"*40)
    result = ft.get_file_info(str(test_file))
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 6: Crear archivo Python")
    print("-"*40)
    py_file = test_dir / "test_script.py"
    py_content = "#!/usr/bin/env python3\nprint(\"Hola desde archivo de prueba\")\n\ndef main():\n    return \"Función main ejecutada\"\n\nif __name__ == \"__main__\":\n    print(main())"
    result = ft.create_file(str(py_file), py_content)
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 7: Listar archivos")
    print("-"*40)
    result = ft.list_files(str(test_dir))
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 8: Extensión no permitida")
    print("-"*40)
    bad_file = test_dir / "test.bad"
    result = ft.create_file(str(bad_file), "contenido")
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 9: Eliminar archivo")
    print("-"*40)
    result = ft.delete_file(str(test_file), confirm=True)
    print(result)
    
    print("\n" + "-"*40)
    print("PRUEBA 10: Listar archivos recursivamente")
    print("-"*40)
    subdir = test_dir / "subdir"
    subdir.mkdir(exist_ok=True)
    subfile = subdir / "subfile.txt"
    ft.create_file(str(subfile), "Archivo en subdirectorio")
    result = ft.list_files(str(test_dir), recursive=True)
    print(result)
    
    print("\n" + "="*60)
    print("PRUEBAS COMPLETADAS")
    print("="*60)
