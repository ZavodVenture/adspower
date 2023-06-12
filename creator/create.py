import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from sys import exit
from configparser import ConfigParser
from progress.bar import Bar
from time import sleep
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import digits, ascii_letters
from datetime import datetime

config = ConfigParser()
config.read('config.ini')
profile_numbers = int(config['Settings']['profiles_number'])

API_URl = 'http://localhost:50325/'


def init_exit():
    input("\nНажмите Enter, чтобы выйти")
    exit()


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result


def worker(index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="critical-error"]')))
    except:
        pass
    else:
        driver.refresh()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
    WebDriverWait(driver, 1)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'import-srp__srp-word-0')))

    seed = metamask[index].split()
    for j in range(12):
        driver.find_element(By.ID, f'import-srp__srp-word-{j}').send_keys(seed[j])

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    meta_password = ''.join(random.choice(ascii_letters + digits) for j in range(8))

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(
        meta_password)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(((By.XPATH, '//input[@data-testid="create-password-confirm"]')))).send_keys(
        meta_password)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

    driver.implicitly_wait(5)

    while 1:
        try:
            sleep(5)
            driver.find_element(By.XPATH, '//div[@class="loading-overlay"]')
        except:
            break
        else:
            driver.refresh()
            continue

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    if discord:
        driver.get('https://discord.com/login/')

        script = """function login(token) {
        setInterval(() => {
        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
        }, 50);
        setTimeout(() => {
        location.reload();
        }, 2500);
        }
    
        login('%s')""" % discord[index]

        attempts = 0
        while attempts != 3:
            driver.execute_script(script)
            try:
                WebDriverWait(driver, 7).until(EC.url_to_be("https://discord.com/channels/@me"))
            except Exception:
                attempts += 1
                continue
            else:
                break

        if attempts == 3:
            with open('errors.txt', 'a', encoding='utf-8') as file:
                file.write(f'{datetime.now()} - Не удалось войти в дискорд ({offset + index + 1} строка в файле)\n')
                file.close()
        else:
            driver.get("https://www.google.com/")
    else:
        driver.get("https://www.google.com/")

    bar.next()


def bypass():
    try:
        open('C:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
    except:
        try:
            open('D:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
        except:
            return False
        else:
            path = 'D:\.ADSPOWER_GLOBAL\\'
    else:
        path = 'C:\.ADSPOWER_GLOBAL\\'

    with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'r',
              encoding='utf-8') as file:
        text = file.read()
        file.close()

    text = text.replace(
        '} = {"scuttleGlobalThis":true,"scuttleGlobalThisExceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","location","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}',
        '} = {"scuttleGlobalThis":false,"scuttleGlobalThisExceptions":[]}')

    try:
        with open(path + 'ext\\19657\\runtime-lavamoat.js', 'w', encoding='utf-8') as file:
            file.write(text)
            file.close()
        with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'w',
                  encoding='utf-8') as file:
            file.write(text)
            file.close()
    except FileNotFoundError:
        try:
            with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'w',
                      encoding='utf-8') as file:
                file.write(text)
                file.close()
        except FileNotFoundError:
            return False

    return True


if __name__ == '__main__':
    print('Проверка перед запуском...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('API недоступен. Проверьте, запущен ли AdsPower.')
        init_exit()

    if not bypass():
        print('Ошибка MetaMask. Проверьте, установлено ли расширение в AdsPower.')
        init_exit()

    metamask = None
    proxy = None
    discord = None
    try:
        metamask = open(config['Settings']['metamask_file'])
        metamask = metamask.read().split('\n')
        if not metamask[-1]:
            metamask = metamask[:-1]
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["metamask_file"]} не найден.')
        init_exit()

    try:
        proxy = open(config['Settings']['proxy_file'])
        proxy = proxy.read().split('\n')
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["proxy_file"]} не найден. Прокси не будут использованы.\n')

    try:
        discord = open(config['Settings']['discord_file'])
        discord = discord.read().split('\n')
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["discord_file"]} не найден. Дискорды не будут использованы.\n')

    offset = int(config['Settings']['offset'])

    metamask = metamask[offset:]
    metamask_len = len(metamask)
    if proxy:
        proxy = proxy[offset:]
        proxy_len = len(proxy)
    else:
        proxy_len = metamask_len

    if discord:
        discord = discord[offset:]
        discord_len = len(discord)
    else:
        discord_len = metamask_len

    if profile_numbers > proxy_len or\
       profile_numbers > discord_len or\
       profile_numbers > metamask_len:
        print('Количество строк в файлах с учётом смещения меньше, чем количество профилей, указанное в настройках.\n'
              f'Будет создано {min(proxy_len, discord_len, metamask_len)} профилей вместо {profile_numbers}\n')
        profile_numbers = min(proxy_len, discord_len, metamask_len)

    print('Проверка завершена. Создание профилей AdsPower...\n')

    group_name = f'Profiles{offset+1}-{offset+profile_numbers}_{config["Settings"]["group_name"]}'
    group_id = 0

    try:
        r = requests.get(API_URl + 'api/v1/group/list').json()
    except Exception as e:
        pass
    else:
        if r['code'] == 0:
            for i in r['data']['list']:
                if i['group_name'] == group_name:
                    group_id = i['group_id']
                    break

    if not group_id:
        try:
            r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': group_name}).json()
        except Exception as e:
            print('Не удалось создать группу профилей AdsPower: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                print('Не удалось создать группу профилей AdsPower: ' + r['msg'])
                init_exit()
            else:
                group_id = r['data']['group_id']

    profile_ids = []
    bar = Bar('Создание профилей', max=profile_numbers)
    for i in range(profile_numbers):
        if proxy:
            host, port, user, password = proxy[i].split(':')
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'other',
                    'proxy_type': config['Settings']['proxy_type'],
                    'proxy_host': host,
                    'proxy_port': port,
                    'proxy_user': user,
                    'proxy_password': password
                }
            }
        else:
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'no_proxy'
                }
            }

        try:
            r = requests.post(API_URl + 'api/v1/user/create', json=account_data).json()
        except Exception as e:
            bar.finish()
            print('\nНе удалось создать профиль: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                bar.finish()
                print('\nНе удалось создать профиль: ' + r['msg'])
                init_exit()
            else:
                profile_ids.append(r['data']['id'])
                bar.next()

        sleep(1)

    bar.finish()

    print('\nПрофили успешно созданы. Запуск профилей...\n')

    bar = Bar("Запуск профилей", max=profile_numbers)
    ws_list = []
    driver_path = ''
    for i in profile_ids:
        args = {
            'user_id': i,
            'ip_tab': 0
        }
        try:
            r = requests.get(API_URl + 'api/v1/browser/start', params=args).json()
        except Exception as e:
            bar.finish()
            print('\nНе удалось запустить профиль: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                bar.finish()
                print('\nНе удалось запустить профиль: ' + r['msg'])
                init_exit()
            else:
                ws_list.append(r["data"]["ws"]["selenium"])
                if not driver_path:
                    driver_path = r["data"]["webdriver"]
                bar.next()
        sleep(1)

    bar.finish()

    print('\nПрофили запущены. Настройка профилей...\n')

    bar = Bar("Настройка профилей", max=profile_numbers)

    threads = chunks([Thread(target=worker, args=(i,)) for i in range(profile_numbers)], int(config['Settings']['profile_setup_numbers']))
    for group in threads:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()

    bar.finish()

    print('\nРабота программы успешно завершена.')
    init_exit()
