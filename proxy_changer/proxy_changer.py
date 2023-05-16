from configparser import ConfigParser
import requests
from time import sleep
from progress.bar import Bar

config = ConfigParser()
config.read('config.ini')
profile_number = int(config['Settings']['profiles_number'])
first_profile = int(config['Settings']['first_profile'])

API_URl = 'http://localhost:50325/'


def init_exit():
    input("\nНажмите Enter, чтобы выйти")
    exit()


if __name__ == '__main__':
    print('Проверка перед запуском...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('API недоступен. Проверьте, запущен ли AdsPower.')
        init_exit()

    sleep(1)

    proxy = None
    try:
        proxy = open(config['Settings']['proxy_file'])
        proxy = proxy.read().split('\n')
        if not proxy[-1]:
            proxy = proxy[:-1]
    except FileNotFoundError:
        print(f'Файл {config["settings"]["metamask_file"]} не найден')
        init_exit()

    if len(proxy) < profile_number:
        print(f'Строк с прокси в файле меньше, чем количество профилей, установленное в настройках.')
        init_exit()

    print('Проверка завершена, поиск user_id...\n')

    profiles = list(range(first_profile, profile_number + first_profile))
    bar = Bar(max=len(profiles))

    for i in range(len(profiles)):
        try:
            r = requests.get(API_URl + 'api/v1/user/list', params={'serial_number': profiles[i]}).json()
        except Exception as e:
            print(f'Не удалось найти профиль с номером {profiles[i]}: {e}')
            bar.finish()
            init_exit()
        else:
            if r['code'] != 0:
                print(f'Не удалось найти профиль с номером {profiles[i]}: {r["msg"]}')
                bar.finish()
                init_exit()
            else:
                if not r['data']['list']:
                    print(f'Не удалось найти профиль с номером {profiles[i]}')
                    bar.finish()
                    init_exit()

                profiles[i] = r['data']['list'][0]['user_id']
                bar.next()
                sleep(1)

    bar.finish()

    print('\nuser_id найдены. Изменение прокси...\n')

    bar = Bar(max=len(profiles))

    for i in range(len(profiles)):
        host, port, user, password = proxy[i].split(':')
        data = {
            'user_id': str(profiles[i]),
            'user_proxy_config': {
                'proxy_soft': 'other',
                'proxy_type': config['Settings']['proxy_type'],
                'proxy_host': host,
                'proxy_port': port,
                'proxy_user': user,
                'proxy_password': password
            }
        }
        try:
            r = requests.post(API_URl + 'api/v1/user/update', json=data).json()
        except Exception as e:
            bar.finish()
            print(f'\nНе удалось изменить прокси в {profiles[i]} профиле: {str(e)}')
            init_exit()
        else:
            if r['code'] != 0:
                print(f'\nНе удалось изменить прокси в {profiles[i]} профиле: {r["msg"]}')
                init_exit()
            else:
                bar.next()

        sleep(1)

    bar.finish()

    print('\nПрокси успешно изменены!')
    init_exit()