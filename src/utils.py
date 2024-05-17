import requests

def get_employers(companies: list):
    """
    Функция возвращает список словарей {company:{}, vacancies: {}}
    """
    employers = []
    for company in companies:
        url = f'https://api.hh.ru/employers/{company}'
        company_response = requests.get(url).json()
        vacancy_response = requests.get(company_response['vacancies_url'],
                                        headers={'User-Agent': 'HH-User-Agent'},
                                        params={'page': 0, 'per_page': 100}).json()
        employers.append({
            'company': company_response,
            'vacancies': vacancy_response['items']
        })
    return employers


def valid_salary(salary):
    '''Функция получения int значения для внесения в таблицу'''
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return salary['to']
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None

