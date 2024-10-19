owm_api_key = 'key'


class Weather_mag:
    @staticmethod
    def getweatherdata(place,api_key = None):
        import requests
        try:
            response = requests.get(
                f'https://ru.api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}') #! Вставляем Ru, поскольку основной не работает
        except (requests.ReadTimeout):
            return 'Read timeout Error'
        
        response.encoding = 'utf-8'
        res_object = response.text
        return res_object
    