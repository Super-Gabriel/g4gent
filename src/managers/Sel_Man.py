from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
import time
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.options import Options as eOptions
from selenium.webdriver.chrome.options import Options as cOptions


class SelMan:
    def __init__(self, driver_path: str, type='edge', usr_data_dir="", profile_dir=""):
        """
        Selenium's manager constructor. Initializes the driver
        =======
        Params
        driver_path: str
            path where the driver is located
        type: str
            type of driver to initialize, 'edge' or 'chrome'
        usr_data_dir: str
            For 'edge': path to the user data directory for edge driver (optional)
            For 'chrome': path where the downloads will be stored.
        profile_dir: str
            Only used for 'edge'
        """ 
        edge_options = eOptions()
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")

        self.dv = None
        try:
            if type == 'edge':
                service = EdgeService(executable_path=driver_path)
                if usr_data_dir != "" and profile_dir != "":
                    options = eOptions()
                    options.add_argument(f'user-data-dir={usr_data_dir}')
                    options.add_argument(f'profile-directory={profile_dir}')
                    self.dv = webdriver.Edge(service=service, options=options) 
                    return  
                else:
                    self.dv = webdriver.Edge(service=service, options=edge_options)
                    self.dv.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            elif type == 'chrome':
                service = ChromeService(executable_path=driver_path)
                if usr_data_dir != "":
                    options = cOptions()
                    options.add_argument("--lang=en")
                    #options.add_argument("--headless=new") THis would be to run without opening window, but doesn't seem to work fine 
                    #options.add_argument("--window-size=1920,1080")
                    ## add experimental options for file downloads
                    options.add_experimental_option("prefs", {
                        "download.default_directory": usr_data_dir,
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "safebrowsing.enabled": True
                    })
                    self.dv = webdriver.Chrome(service=service, options=options)
                    return
                else:
                    self.dv = webdriver.Chrome(service=service)
        except Exception as e:
            print(f'error en __init__: {e}')

    # metodo para asignarle un texto a un elemento
    def asign_value_to_by_js(self, type: str, value: str, text: str, seconds=60, wait=1, enter=False):
        try:
            text_input = self.get_obj_by(type, value, seconds, wait)
            self.dv.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """, text_input, text)
            if enter:
                text_input.send_keys(Keys.ENTER)
            else:
                text_input.send_keys()
        except Exception as e:
            print(f'error en asign_value_to_by_js: {e}')

    # metodo para obtener texto de un elemento
    def get_text(self, type: str, value: str, seconds=60, wait=1):
        element = self.get_obj_by(type, value, seconds, wait)
        texto = element.get_attribute("textContent")
        return texto
    
    # metodo para escribir en un area de texto
    def send_keys_to(self, type: str, value: str, string: str, seconds=60, wait=1, enter=False):
        result = False
        try:
            text_input = self.get_obj_by(type, value, seconds, wait)
            text_input.clear()
            if enter:
                text_input.send_keys(string, Keys.ENTER)
            else:
                text_input.send_keys(string)        
            return True
        except Exception as e:
            print(f'error en click_obj: {e}')
        return result
    
    # metodo para clickear un objeto
    def click_obj(self, type: str, value: str, seconds=60, wait=1, attemps=2):
        result = False
        attemp = 1
        while attemp <= attemps:
            try:
                self.get_obj_by(type, value, seconds, wait).click()
                result = True
                break
            except Exception as e:
                attemp += 1
                print(f'error en click_obj {value}')
        return result 

    # metodo para selecionar elementos en un select de html (dropdwon)
    def select_element(self, select_type: str, select: str, value_to_select: str, value_type='value', wait=2, siv=True):
        try:
            select_element = self.get_obj_by(select_type, select) # obteniendo el select

            if siv: # scroll into view = True por defecto (dirigires hacia el elemento)
                self.dv.execute_script("arguments[0].scrollIntoView(true);", select_element) # dirigirse hacie el select

            select_type_obj = Select(select_element) # el objeto tipo select
            select_element.click() # clickeando el elemento select
            
            time.sleep(wait) # esperando a que se abra el select
            if value_type == 'value':
                select_type_obj.select_by_value(value_to_select)
            elif value_type == 'id':
                select_type_obj.select_by_index(value_to_select)
            elif value_type == 'text':
                select_type_obj.select_by_visible_text(value_to_select) 
            time.sleep(wait)
        except Exception as e:
            print(f'error en select_element: {e}')

    # metodo para abrir una pagina dado un url 
    def open_page(self, url: str, wait=0):
        try:
            self.dv.get(url)
            if wait>0:
                time.sleep(wait)
        except Exception as e:
            print(f'error en open page: {e}')

    # metodo para obtener el elemento que ocurra primero de dos v1 o v2 ambos xpaths
    def get_any_of(self, v1_xpath: str, v2_xpath: str, wait=1, seconds=60):
        id = 0
        try:
            element = WebDriverWait(self.dv, seconds).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.XPATH, v1_xpath)),
                    EC.element_to_be_clickable((By.XPATH, v2_xpath))
                )
            )
            time.sleep(wait)
            if self.get_obj_by('xpath', v1_xpath, seconds=0, wait=0) == element:
                id = 1
            elif self.get_obj_by('xpath', v2_xpath, seconds=0, wait=0) == element:
                id = 2
        except Exception as e:
            print(f'error en get_any_of: {e} (SelMan.py)')
            element = None
            pass
        return element, id
    
    # metodo para hacer click en el elemento que aparezca primero entre dos elementos xpath
    def click_any_of(self, v1_xpath:str, v2_xpath:str, wait=1, seconds=60):
        try:
            result = False
            elem, id_clicked = self.get_any_of(v1_xpath=v1_xpath, v2_xpath=v2_xpath, wait=wait, seconds=seconds)
            elem.click()
            result = True
        except Exception as e:
            print(f'error en click_any_of: {e} (SelMan.py)')
        return result, id_clicked

    # metodo para obtener elementos (find.elements) util para obtener divs dentro de divs por ejemplo
    def get_objs_by(self, type:str, value:str, seconds=60, wait=1):
        try:
            elems = WebDriverWait(self.dv, seconds).until(
                EC.presence_of_all_elements_located((By.XPATH, value)) if type == 'xpath' else
                None # todo: agregar por id, y name (si en el futuro es necesario) 
            )
        except Exception as e:
            print(f'error en get_objs_by: {e} (SelMan.py)')
        return elems

    # metodo para obtener un elemento por tipo id, xpath o name, dado su valor
    def get_obj_by(self, type: str, value: str, seconds=60, wait=1):
        obj = None
        try:
            #print(f'intentanto obtener {value}\n')
            obj = WebDriverWait(self.dv, seconds).until(
                EC.element_to_be_clickable((By.ID, value)) if type == 'id' else
                EC.element_to_be_clickable((By.XPATH, value)) if type == 'xpath' else
                EC.element_to_be_clickable((By.NAME, value)) if type == 'name' else
                EC.element_to_be_clickable((By.CLASS_NAME, value)) if type == 'class' else
                EC.element_to_be_clickable((By.CSS_SELECTOR, value)) if type == 'css_selector' else
                None
            )
            time.sleep(wait)
        except Exception as e:
            #print(f'ocurrió un error get_obj_by_id: {id} : {e}')
            pass
        return obj
    
    # metodo para esperar una alerta y aceptarla
    def acept_alert(self, text='esperando alerta'):
        print(text)
        try:
            WebDriverWait(self.dv, 10).until(EC.alert_is_present())
            alert = self.dv.switch_to.alert
            print("alerta encontrada")
            alert.accept()
            return True
        except Exception:
            print(f'no hubo alerta')
            return False 

    # metodo para cambiar a un frame por el id
    def switch_to_frame(self, frame_name: str, seconds=2):
        try:
            self.dv.switch_to.frame(self.get_obj_by('id', frame_name, seconds))
            return True
        except Exception as e:
            print(f'error en switch_to_frame: {e}')
            return False
    
    # metodo para regresar al contenido original
    def switch_to_default_content(self):
        try:
            self.dv.switch_to.default_content()
        except Exception as e:
            print(f'error en switch_to_default_content: {e}')

    # metodo para hacer unzoom a la ventana del driver
    def unzoom(self, percentage=50):
        try:
            self.dv.execute_script(f"document.body.style.zoom='{percentage}%'")
        except Exception as e:
            print(f'error en unzoom: {e}')

    # metodo para hacer scroll
    def scroll(self, scroll_value: int):
        try:
            self.dv.execute_script(f"window.scrollTo(document.body.scrollWidth, {scroll_value});")
        except Exception as e:
            print(f'error en scroll: {e}')

    # metodo para cerrar el driver de selenium
    def quit(self):
        try:
            self.dv.quit()
        except Exception as e:
            print(f'error en quit: {e}')

    