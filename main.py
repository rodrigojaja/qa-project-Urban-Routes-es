import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import json
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    boton_pedir_taxi = (By.CSS_SELECTOR, "button.button.round")
    boton_tarifa_comfort = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    campo_numero_telefono = (By.CLASS_NAME, "np-button")
    agregar_numero_de_telefono = (By.ID, 'phone')
    boton_siguiente_numero_de_telefono = (By.CSS_SELECTOR, ".button.full")
    campo_ingresar_codigo = (By.ID, "code")
    boton_confirmar_codigo = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    click_metodo_de_pago = (By.CSS_SELECTOR, '.pp-button.filled')
    click_agregar_tarjeta = (By.CSS_SELECTOR, '.pp-row.disabled')
    campo_tarjeta_rellenar = (By.ID, 'number')
    campo_nip_rellenar = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    click_para_perder_foco = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[2]')
    boton_agregar_tarjeta = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    boton_cerrar_ventana_emergente = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal > div.section.active > button')
    obtener_metodo_de_pago = (By.CLASS_NAME, "pp-value-text")
    campo_comentario = (By.ID, "comment")
    slider_manta_y_pañuelos = (By.CSS_SELECTOR, ".slider.round")
    boton_agregar_helado = (By.CLASS_NAME, 'counter-plus')
    obtener_cantidad_de_helados = (By.CLASS_NAME, 'counter-value')
    pedir_taxi = (By.CLASS_NAME, 'smart-button')
    titulo_ventana_emerente = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
#ingresa desde
    def set_from(self, from_address):
        from_field_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        from_field_element.send_keys(from_address)

    #ingresa hasta
    def set_to(self, to_address):
        to_field_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field))
        to_field_element.send_keys(to_address)
#ingresa desde y hasta
    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
#obtener valor desde
    def get_from(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.from_field)
        ).get_property('value')
#obtener valor hasta
    def get_to(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.to_field)
        ).get_property('value')

#click en el boton pedir un taxi
    def set_click_boton_pedir_un_taxi(self):
        pedir = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_pedir_taxi)))
        pedir.click()
#click en tarifa comfort
    def set_click_boton_comfort(self):
        clickComfort = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_tarifa_comfort)))
        clickComfort.click()
#obtener valor de boton de tarifa comfort
    def get_boton_comfort(self):
        textoTarifaComfort = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_tarifa_comfort))).text
        return textoTarifaComfort
#click en el boton numero de telefono
    def set_boton_numero_telefono(self):
        clickNumeroDeTelefono = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_numero_telefono)))
        clickNumeroDeTelefono.click()
#ingresar numero de telefono
    def set_ingresar_numero_de_telefono(self, numero):
        agregarNumero = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.agregar_numero_de_telefono)))
        agregarNumero.send_keys(numero)
#Click en el boton siguiente para despeus obtener el codigo
    def set_click_boton_siguiente_numero_telefono(self):
        siguiente = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_siguiente_numero_de_telefono)))
        siguiente.click()
#obtener codigo
#ingresa el codigo en el campo
    def set_ingresar_codigo(self, codigo):
        ingresarCodigo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_ingresar_codigo)))
        ingresarCodigo.send_keys(codigo)
#confirmar codigo
    def set_confirmar_codigo(self):
        confirmar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_confirmar_codigo)))
        confirmar.click()
#obtener numero de telefono
    def get_numero_telefono(self):
        numero = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_numero_telefono)))
        return numero.text
    def set_proceso_numero_de_telefono_ingresar(self, numero):
        self.set_boton_numero_telefono()
        self.set_ingresar_numero_de_telefono(numero)
        self.set_click_boton_siguiente_numero_telefono()
    def set_codigo_numero_telefono(self, codigo):
        self.set_ingresar_codigo(codigo)
        self.set_confirmar_codigo()
#click en metodo de pago
    def set_click_metodo_pago(self):
        tarjetaCredito = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.click_metodo_de_pago)))
        tarjetaCredito.click()
#click en agregar tarjeta
    def set_click_agregar_tarjeta_por_favor(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.pp-row.disabled'))).click()

    #click metodo de pago y campo agregar tarjeta
    def set_clicks_metodo_pago_agregar_tarjeta(self):
        self.set_click_metodo_pago()
        self.set_click_agregar_tarjeta_por_favor()
#ingresar numero de tarjeta en campo numero de tarjeta
    def set_rellenar_campo_tarjeta(self, numeroDeTarjeta):
        ingresarTarjeta = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_tarjeta_rellenar)))
        ingresarTarjeta.send_keys(numeroDeTarjeta)
#ingresar codigo en el campo codigo
    def set_rellenar_campo_codigo(self, numeroCode):
        ingresarCodigo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_nip_rellenar)))
        ingresarCodigo.send_keys(numeroCode)
#ingresar campo tarjeta y campo codigo
    def set_rellenar_campos_tarjeta_y_codigo(self, numeroDeTarjeta, numeroCode):
        self.set_rellenar_campo_tarjeta(numeroDeTarjeta)
        self.set_rellenar_campo_codigo(numeroCode)
#obtener valor campo tarjeta
    def get_obtener_campo_tarjeta(self):
        ingresarTarjeta = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_tarjeta_rellenar)))
        return ingresarTarjeta.get_property('value')
#obtener valor campo codigo
    def get_obtener_campo_codigo(self):
        ingresarCodigo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_nip_rellenar)))
        return ingresarCodigo.get_property('value')
#Dar click para perder el enfoque
    def set_click_para_derder_el_enfoque(self):
        ckickOtroLado = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.click_para_perder_foco)))
        ckickOtroLado.click()
#click en agregar tarjeta
    def set_click__boton_agregar_tarjeta(self):
        clickAgregar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_agregar_tarjeta)))
        clickAgregar.click()
#cerrar ventana <button class="close-button section-close"></button>
    def set_click_cerrar_ventana_emergente(self):
        cerrarVentana = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_cerrar_ventana_emergente)))
        cerrarVentana.click()
#perder enfoque, agregar tarjeta, cerrar ventana emergente
    def set_clicks_perder_enfoque_agregar_tarjeta_cerrar_ventana(self):
        self.set_click_para_derder_el_enfoque()
        self.set_click__boton_agregar_tarjeta()
        self.set_click_cerrar_ventana_emergente()
#obtener valor de metodo de pago
    def get_obtener_metodo_de_pago(self):
        comprobarTexto = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.obtener_metodo_de_pago)))
        return comprobarTexto.text
#agregar comentario al conductor
    def set_agregar_comentario(self, message_for_driver):
        agregarComentario = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_comentario)))
        agregarComentario.send_keys(message_for_driver)
#comprobarComentario
    def get_comprobar_comentario(self):
        comprobarComentario = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.campo_comentario)))
        return comprobarComentario.get_attribute('value')
#hacer click en manta y pañuelos
    def set_click_manta_y_pañuelos(self):
        clickSlider = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.slider_manta_y_pañuelos)))
        clickSlider.click()
#saber si esta seleccionado el slider
    def get_saber_si_slider_esta_seleccionado(self):
        apretar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='r-sw-container']/*[contains(text(),'Manta')]/..//div[@class='switch']//input[@class='switch-input']")))
        return apretar.is_selected()
#agregar helado
    def set_agregar_helado(self):
        mashelado = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.boton_agregar_helado)))
        mashelado.click()
        mashelado.click()
#obtener cantidad de helados
    def get_cantidad_de_helados(self):
        helado = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.obtener_cantidad_de_helados)))
        return helado.text
#hacer click pedir taxo
    def set_click_pedir_taxi(self):
        pedir = self.driver.find_element(*self.pedir_taxi)
        pedir.click()
#comprobar valor ventana emergente
    def get_comprobar_ventana_emergente_si(self):
        emergente = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((self.titulo_ventana_emerente)))
        return emergente.text
#darle tiempo
    def set_tiempo(self):
        time.sleep(40)
#el coductor llegara en...
    def get_comprobar_informacion_de_conductor(self):
        otro = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((self.titulo_ventana_emerente)))
        return otro.text


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        chrome_options = ChromeOptions()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()
        cls.driver.delete_all_cookies()


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
    def test_texto_tarifa_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_click_boton_pedir_un_taxi()
        routes_page.set_click_boton_comfort()
        assert 'Comfort\n$10' == routes_page.get_boton_comfort()
    def test_agregar_numero_de_telefono(self):
        routes_page = UrbanRoutesPage(self.driver)
        numero = data.phone_number
        routes_page.set_proceso_numero_de_telefono_ingresar(numero)
        codigo = retrieve_phone_code(self.driver)
        routes_page.set_codigo_numero_telefono(codigo)
        assert routes_page.get_numero_telefono() == numero

    def test_agregar_una_tarjeta_de_credito(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_clicks_metodo_pago_agregar_tarjeta()
        numeroDeTarjeta = data.card_number
        numeroCode = data.card_code
        routes_page.set_rellenar_campos_tarjeta_y_codigo(numeroDeTarjeta, numeroCode)
        assert routes_page.get_obtener_campo_tarjeta() == numeroDeTarjeta
        assert routes_page.get_obtener_campo_codigo() == numeroCode
        routes_page.set_clicks_perder_enfoque_agregar_tarjeta_cerrar_ventana()
        assert routes_page.get_obtener_metodo_de_pago() == 'Tarjeta'

    def test_agregar_comentario_al_conductor(self):
        routes_page = UrbanRoutesPage(self.driver)
        comentario = data.message_for_driver
        routes_page.set_agregar_comentario(comentario)
        assert routes_page.get_comprobar_comentario() == comentario
        time.sleep(5)
    def test_seleccionar_manta_y_pañuelos(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_click_manta_y_pañuelos()
        assert routes_page.get_saber_si_slider_esta_seleccionado() == True
    def test_agregar_2_helados(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_agregar_helado()
        assert routes_page.get_cantidad_de_helados() == '2'
    def test_ventana_emergente(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_click_pedir_taxi()
        assert routes_page.get_comprobar_ventana_emergente_si() == 'Buscar automóvil'
    def test_ventana_opcional(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_tiempo()
        assert 'El conductor llegará en' in routes_page.get_comprobar_informacion_de_conductor()



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
