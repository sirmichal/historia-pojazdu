import pandas
import datetime
from selenium import webdriver


def nastepna_data(start, koniec=None):
    if koniec:
        start = datetime.datetime.strptime(start, '%d-%m-%Y')
        koniec = datetime.datetime.strptime(koniec, '%d-%m-%Y')
        zakres = pandas.date_range(start, koniec)
    else:
        zakres = pandas.date_range(f'{start}-01-01', f'{start}-12-31')
    for data in zakres:
        yield data.strftime("%d-%m-%Y")


def sprawdz_date(nr_rej: str, vin: str, start, koniec=None):
    assert len(vin) == 17
    firefox = webdriver.Firefox()
    firefox.get(r'https://historiapojazdu.gov.pl')
    for data in nastepna_data(start, koniec):
        nr_rej_form = firefox.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:rej')
        vin_form = firefox.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:vin')
        data_rej_form = firefox.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:data')
        sprawdz_btn = firefox.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:btnSprawdz')
        for elem in nr_rej_form, vin_form, data_rej_form:
            elem.clear()
        nr_rej_form.send_keys(nr_rej)
        vin_form.send_keys(vin)
        data_rej_form.send_keys(data)
        sprawdz_btn.click()
        if 'RAPORT O POJEŹDZIE' in firefox.page_source:
            print(f'nr rejestracyjny: {nr_rej}')
            print(f'VIN: {vin}')
            print(f'data pierwszej rejestracji: {data}')
            break
    else:
        firefox.close()


if __name__ == '__main__':
    nr_rej = ''
    vin = ''

    sprawdz_date(nr_rej, vin, '04-05-2010', '04-05-2010')
