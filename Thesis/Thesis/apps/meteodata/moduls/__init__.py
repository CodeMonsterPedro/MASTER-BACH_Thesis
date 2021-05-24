from .Deamon.ForecastDeamon import ForecastDeamon
from .MeteodataMiner import MeteodataMiner
from .DataReader import DataReader


class MainMenu:

    Deamon = ForecastDeamon()
    Miner = MeteodataMiner()
    Reader = DataReader()
    currentContext = 1

    def get_context():
        if MainMenu.currentContext == 1:
            context = {
                "meteodata_page": MainMenu.Reader._meteodata_page,
                "meteodata_search": MainMenu.Reader._meteodata_search,
                "meteodata_max_pages": MainMenu.get_max_pages(1),
                "meteodata_top_labels": MainMenu.get_top_labels(),
                "meteodata": MainMenu.Reader.get_data(1),
                "clear_meteodata_page": MainMenu.Reader._clear_meteodata_page,
                "clear_meteodata_search": MainMenu.Reader._clear_meteodata_search,
                "clear_meteodata_max_pages": MainMenu.get_max_pages(2),
                "clear_meteodata": MainMenu.Reader.get_data(2)
            }
        elif MainMenu.currentContext == 2:
            context = {
                "forecast": MainMenu.Reader.get_data(3),
                "forecast_page": MainMenu.Reader._forecast_page,
                "forecast_search": MainMenu.Reader._forecast_search,
                "forecast_max_pages": MainMenu.get_max_pages(3),
                "forecast_top_labels": MainMenu.get_top_labels(),
                "clear_forecast": MainMenu.Reader.get_data(4),
                "clear_forecast_page": MainMenu.Reader._clear_forecast_page,
                "clear_forecast_search": MainMenu.Reader._clear_forecast_search,
                "clear_forecast_max_pages": MainMenu.get_max_pages(4),
            }
        elif MainMenu.currentContext == 3:
            context = {
                "anomaly": MainMenu.Reader.get_data(5),
                "anomaly_page": MainMenu.Reader._anomaly_page,
                "anomaly_search": MainMenu.Reader._anomaly_search,
                "anomaly_max_pages": MainMenu.get_max_pages(5),
                "anomaly_top_labels": MainMenu.get_top_labels()
            }
        context.update(
            {
                "rows_count": MainMenu.Reader._rows_count,
                "menu_status": MainMenu.get_menu_status(),
                "submenu_status": MainMenu.get_submenu_status()
            }
        )
        return context

    def set_page(num, tableId):
        MainMenu.Reader.set_page(num, tableId)

    def search(tableId, search):
        MainMenu.Reader.search(tableId, search)

    def set_context(num):
        if num >= 1 and num <= 3:
            MainMenu.currentContext = num

    def data_update():
        print('data_update')
        #MainMenu.Miner.updateMeteodata()
        
    def forecast_update():
        print('forecast_update')
        #MainMenu.Deamon.update()

    def make_forecast_test():
        print('make_forecast_test')
        #MainMenu.Deamon._make_test()

    def anomaly_update():
        print('anomaly_update')
        #MainMenu.Deamon.scanForAnomalies()

    def get_menu_status():
        print('get_menu_status')
        if MainMenu.currentContext == 1:
            return ['button-active', 'button', 'button']
        elif MainMenu.currentContext == 2:
            return ['button', 'button-active', 'button']
        elif MainMenu.currentContext == 3:
            return ['button', 'button', 'button-active']

    def get_submenu_status():
        print('get_submenu_status')
        if MainMenu.currentContext == 1:
            if MainMenu.Miner.meteodataUpdateStatus():
                return 'hide'
            else:
                return 'active'
        elif MainMenu.currentContext == 2:
            if MainMenu.Deamon.forecastUpdateStatus():
                return 'hide'
            else:
                return 'active'
        elif MainMenu.currentContext == 3:
            if MainMenu.Deamon.anomaliesScanStatus():
                return 'hide'
            else:
                return 'active'

    def get_top_labels():
        print('get_top_labels')
        if MainMenu.currentContext == 1:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']
        elif MainMenu.currentContext == 2:
            return ['№', 'Дата и время', 'Код места', 'Название места', 'Температура', 'Направление ветра', 'Скорость ветра', 'Давление воздуха', 'Давление воды', 'Погодные явления']
        elif MainMenu.currentContext == 3:
            return ['№', '№ метеоданных', 'Имя поля', 'Значение', 'Описание аномалии']

    def get_max_pages(tableId):
        return MainMenu.Reader.get_max_pages(tableId)

    def sort(tableId, dataName):
        print('sort data', tableId, dataName)
        MainMenu.Reader.sort(tableId, dataName - 1)