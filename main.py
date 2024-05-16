from src.utils import get_employers


def main():
    companies = [78638] # список id компаний
    employers = get_employers(companies) # список словарей для заполнения базы данных
    print(employers)

if __name__ == '__main__':
    main()