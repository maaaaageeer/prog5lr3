from weather_mag import Weather_mag as wm 
import pytest

key = 'key'



def test_without_key():
    assert wm.getweatherdata(
        "moscow") is None, \
        " Для получения данных необходимо задать значение для api_key "


def test_in_riga():
    assert wm.getweatherdata("Riga",
                                           api_key=key) is not None, \
        " Type of response is not none while using the key "


def test_type_of_res():
    assert type(wm.getweatherdata("Riga",
                                                api_key=key)) is str, \
        " Type of response is not none while using the key "


def test_args_error():
    assert wm.getweatherdata(
        '') is None, \
        " There should be one positional argument: 'city' and one keyword argument 'key_arg'"


def test_pos_arg_error():
    assert wm.getweatherdata('',
                                           api_key=key) is None, \
        " There should be one positional argument: 'city' "


def test_coords_dim():
    import json

    assert len(
        json.loads(wm.getweatherdata('Riga', api_key=key)).get('coord')) == 2, \
        " Dimension is 2: lon and lat "


def test_temp_type():
    import json

    assert type(json.loads(wm.getweatherdata('Riga', api_key=key)).get(
        'main')['feels_like']) is float, \
        " Error with type of feels_like attribute "


inp_params_1 = "city, api_key, expected_country"
exp_params_countries = [("Chicago", key, 'US'),
                        ("Saint Petersburg", key, 'RU'), ("Dakka", key, 'BD'),
                        ("Minsk", key, 'BY'), ("Kioto", key, 'JP'),
                        ("Anchorage", key, 'US'), ("Havana", key, 'CU')]


@pytest.mark.parametrize(inp_params_1, exp_params_countries)
def test_countries(city, api_key, expected_country):
    import json

    assert json.loads(wm.getweatherdata(city, api_key=key)).get('sys',
                                                                              'NoValue')["country"] == expected_country, \
        " Error with country code "


#
# Проверить что такое DST и как оно может влиять на этот тест.
inp_params_2 = "city, api_key, expected_time"
exp_params_timezones = [("Chicago", key, 'UTC-5'),
                        ("Saint Petersburg", key, 'UTC+3'),
                        ("Dakka", key, 'UTC+6'), ("Minsk", key, 'UTC+3'),
                        ("Kioto", key, 'UTC+9'), ("Anchorage", key, 'UTC-8'),
                        ("Havana", key, 'UTC-4')]


@pytest.mark.parametrize(inp_params_2, exp_params_timezones)
def test_utc_time(city, api_key, expected_time):
    import json
    import datetime
    json_response = json.loads(wm.getweatherdata(city, api_key=key)).get('timezone',
                                                                                       'NoValue')
    
    utc_timezone = datetime.timezone(datetime.timedelta(seconds=json_response))
    utc_timezone_for_test = datetime_timezone_to_test_timezone(utc_timezone)
    assert utc_timezone_for_test == expected_time, \
       " Error with timezone "

import datetime
def datetime_timezone_to_test_timezone(datetime_timezone : datetime.timezone):
    formatted = str(datetime_timezone)[:6]
    if formatted[4] == '0':
        formatted = formatted[:4] + formatted[5:6]
    return formatted