import psycopg2

from src.utils import get_employers, valid_salary
from config import config
from src.DBManager import DBManager


def main():

    database_name = 'cw5'
    params = config() # параметры для подключения

    # создаем базу данных
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cursor.execute(f'CREATE DATABASE {database_name}')
    conn.close()

    companies = [80, 78638, 1740, 577743, 23186, 3127, 2748, 4233, 39305, 15478]  # список id компаний
    employers = get_employers(companies)  # список словарей для заполнения базы данных

    # создаем таблицы базы данных

    conn = psycopg2.connect(database=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE companies(
                    company_id serial PRIMARY KEY,
                    company_name varchar(50) NOT NULL,
                    link varchar(200) NOT NULL,
                    url_vacancies varchar(200) NOT NULL)
                    """)

        cur.execute("""
                    CREATE TABLE vacancies(
                    vacancy_id serial PRIMARY KEY,
                    company_id int REFERENCES companies (company_id),
                    title_vacancy varchar(100),
                    salary int)
                    """)
    conn.commit()

    # заполняем базу данных

    with conn.cursor() as cur:
        for emp in employers:
            cur.execute("""INSERT INTO companies (company_name, link, url_vacancies)
                        VALUES (%s, %s, %s)
                        returning company_id""",
                        (emp["company"].get("name"),
                         emp["company"].get("alternate_url"),
                         emp["company"].get("vacancies_url")))

            company_id = cur.fetchone()[0]
            for vacancy in emp['vacancies']:
                salary = valid_salary(vacancy["salary"])
                cur.execute("""INSERT INTO vacancies
                            (company_id, title_vacancy, salary)
                            VALUES (%s, %s, %s)""",
                            (company_id, vacancy['name'], salary))

    conn.commit()
    conn.close()

    db = DBManager(database_name, params) #
    companies_list = db.get_companies_and_vacancies_count()
    all_vacancies = db.get_all_vacancies()
    highest_salary = db.get_vacancies_wth_highest_salary()
    avg_salary = db.get_avg_salary()
    keyword_vac = db.get_vacancies_with_keyword('python')
    print(companies_list,  all_vacancies, highest_salary, avg_salary, keyword_vac, sep="\n")


if __name__ == '__main__':
    main()
