from UI import AppUI
from PyQt5 import QtWidgets
import requests
import iso3166
import datetime
import rsrc


class WeatherApp:
    def __init__(self):

        self.main_window = QtWidgets.QMainWindow()
        self.weather_widget = QtWidgets.QWidget(self.main_window)

        self.weather_widget_ui = AppUI.Ui_Form()
        self.weather_widget_ui.setupUi(self.main_window)
        self.weather_widget_ui.SearchButton.clicked.connect(self.process_ui)

        self.main_window.show()

        self.__appid = 'df3bdc3de53e4551be3e6d949fc80e02'
        self.coord = None
        self.units = 'metric'

    def process_ui(self):

        self.clear()

        city = self.weather_widget_ui.city.toPlainText()
        if not city:
            self.weather_widget_ui.weather.print('Enter the name of the city')

        country = self.weather_widget_ui.country.toPlainText()
        if not country:
            self.weather_widget_ui.weather.print('Enter the name of the country')
        elif country.upper() in ['USA', 'UNITED STATES', 'US']:
            country = 'United States of America'
        elif country.upper() in ['GB', 'GREAT BRITAIN', 'ENGLAND', 'IRELAND']:
            country = 'United Kingdom of Great Britain and Northern Ireland'

        if self.get_city_coord(city, country):
            data = self.get_weather_data(self.coord)

            current_weather = data['current']['weather'][0]['main']
            current_temp = data['current']['temp']
            humidity = data['current']['humidity']
            max_temp = data['daily'][0]['temp']['max']
            min_temp = data['daily'][0]['temp']['min']
            current_presure = data['current']['pressure']
            current_wind_speed = data['current']['wind_speed']

            sunrise_date = datetime.datetime.fromtimestamp(data['daily'][0]['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
            sunrise_time = sunrise_date.split()[1]
            sunset_date = datetime.datetime.fromtimestamp(data['daily'][0]['sunset']).strftime('%Y-%m-%d %H:%M:%S')
            sunset_time = sunset_date.split()[1]

            self.weather_widget_ui.weather.setText(current_weather)
            self.weather_widget_ui.temp.setText(str(current_temp))
            self.weather_widget_ui.maxtemp.setText(f'Daily max temp: {max_temp}')
            self.weather_widget_ui.mintemp.setText(f'Daily min temp: {min_temp}')
            self.weather_widget_ui.pressure.setText(f'Pressure: {current_presure}')
            self.weather_widget_ui.humidity.setText(f'Humidity: {humidity}')
            self.weather_widget_ui.windspeed.setText(f'Wind speed: {current_wind_speed}')

            self.weather_widget_ui.sunrise.setText(f'Sunrise: {sunrise_time}')
            self.weather_widget_ui.sunset.setText(f'Sunset: {sunset_time}')

            if data['current']['weather'][0]['id'] == 800:
                self.weather_widget_ui.sun.setVisible(True)
            else:
                weather_id = data['current']['weather'][0]['id'] // 100
                if weather_id == 2:
                    self.weather_widget_ui.thunderstorm.setVisible(True)
                elif weather_id == 3 or weather_id == 5:
                    self.weather_widget_ui.rain.setVisible(True)
                elif weather_id == 6:
                    self.weather_widget_ui.snow.setVisible(True)
                elif weather_id == 7:
                    self.weather_widget_ui.fog.setVisible(True)
                else:
                    self.weather_widget_ui.cloud.setVisible(True)
        else:
            self.weather_widget_ui.temp.setText(f'There is no such city {city}')


    def get_city_coord(self, city, country):
        try:
            city = city.capitalize()
            country_code = iso3166.countries_by_name[country.upper()].alpha3

            url_locate_api = f'http://api.openweathermap.org/geo/1.0/direct'
            parametrs = {'q': f'{city},{country_code}', 'appid': {self.__appid}}

            resp = requests.get(url_locate_api, params=parametrs)
            data = resp.json()

            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            self.coord = (lat, lon)
        finally:
            return self.coord

    def get_weather_data(self, coord):
        url_weather_api = 'https://api.openweathermap.org/data/2.5/onecall'
        parametrs = {'lat': {coord[0]}, 'lon': {coord[1]}, 'appid': {self.__appid}, 'units': {self.units}}

        resp = requests.get(url_weather_api, params=parametrs)
        data = resp.json()
        return data

    def clear(self):
        self.weather_widget_ui.sun.setHidden(True)
        self.weather_widget_ui.thunderstorm.setHidden(True)
        self.weather_widget_ui.rain.setHidden(True)
        self.weather_widget_ui.snow.setHidden(True)
        self.weather_widget_ui.fog.setHidden(True)
        self.weather_widget_ui.cloud.setHidden(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    new_request = WeatherApp()
    sys.exit(app.exec_())
