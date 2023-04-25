from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
from sys import exit
import re
from time import sleep
from progress.bar import Bar
from threading import Thread
import random
from string import ascii_letters, digits
import os
from shutil import rmtree


def init_exit():
    input("\nНажмите Enter, чтобы выйти")
    exit()


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result


def worker(ws_index, metamask_index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[ws_index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="critical-error"]')))
    except:
        pass
    else:
        driver.refresh()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
    WebDriverWait(driver, 1)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'import-srp__srp-word-0')))

    seed = metamask[metamask_index].split()
    for j in range(12):
        driver.find_element(By.ID, f'import-srp__srp-word-{j}').send_keys(seed[j])

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    meta_password = ''.join(random.choice(ascii_letters + digits) for j in range(8))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(meta_password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(((By.XPATH, '//input[@data-testid="create-password-confirm"]')))).send_keys(meta_password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    driver.get('https://www.google.com/')


def bypass():
    try:
        open('C:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
    except FileNotFoundError:
        try:
            open(
                'D:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
        except FileNotFoundError:
            return False
        else:
            path = 'D:\.ADSPOWER_GLOBAL\\'
    else:
        path = 'C:\.ADSPOWER_GLOBAL\\'

    with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'r', encoding='utf-8') as file:
        text = file.read()
        file.close()

    text = text.replace(
        '} = {"scuttleGlobalThis":true,"scuttleGlobalThisExceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","location","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}',
        '} = {"scuttleGlobalThis":false,"scuttleGlobalThisExceptions":[]}')

    with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'w', encoding='utf-8') as file:
        file.write(text)
        file.close()

    for d in os.listdir(path + 'cache'):
        try:
            rmtree(path + f'cache\\{d}\\Default\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn')
            rmtree(path + f'cache\\{d}\\extensionCenter\\3f78540a9170bc1d87c525f061d1dd0f')
        except:
            continue

    return True


config = ConfigParser()
config.read('restore.ini')

API_URl = 'http://localhost:50325/'

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

    sleep(1)

    metamask = None
    try:
        metamask = open(config['settings']['metamask_file'])
        metamask = metamask.read().split('\n')
        if not metamask[-1]:
            metamask = metamask[:-1]
    except FileNotFoundError:
        print(f'Файл {config["settings"]["metamask_file"]} не найден')
        init_exit()

    print('Проверка завершена, поиск строк, связанных с профилями...\n')

    first_profile = int(config['settings']['first_profile'])
    profile_number = int(config['settings']['profile_number'])

    profiles = list(range(first_profile, profile_number + first_profile))
    lines = []
    for profile in profiles:
        try:
            r = requests.get(API_URl + 'api/v1/user/list', params={'serial_number': profile}).json()
        except Exception as e:
            print(f'Не удалось найти профиль с номером {profile}: {e}')
            init_exit()
        else:
            sleep(1)
            if r['code'] != 0:
                print(f'Не удалось найти профиль с номером {profile}: {r["msg"]}')
                init_exit()
            else:
                if not r['data']['list']:
                    print(f'Не удалось найти профиль с номером {profile}')
                    init_exit()

                group_id = r['data']['list'][0]['group_id']
                group_name = r['data']['list'][0]['group_name']

                offset = 0
                try:
                    offset = int(re.findall(r'Profiles(\d*)-\d*', group_name)[0]) - 1
                except Exception as e:
                    print('Не удалось определить номер первого профиля в группе (группа имеет не стандартное название)')
                    init_exit()

                try:
                    r = requests.get(API_URl + 'api/v1/user/list', params={'group_id': group_id, 'page_size': 100}).json()
                except Exception as e:
                    print(f'Не удалось найти профили в группе: {e}')
                    init_exit()
                else:
                    sleep(1)
                    if r['code'] != 0:
                        print(f'Не удалось найти профили в группе: {r["msg"]}')
                        init_exit()
                    else:
                        group = r['data']['list']
                        group.reverse()

                        flag = False
                        for i in range(len(group)):
                            if group[i]['serial_number'] == str(profile):
                                lines.append(offset + i)
                                flag = True
                                break
                        if not flag:
                            print(f'Не удалось найти номер строки для профиля {profile}')
                            init_exit()

    print('Строки успешно найдены. Запуск профилей...\n')
    bar = Bar('Запуск профилей', max=len(profiles))
    ws_list = []
    driver_path = ''

    for i in profiles:
        args = {
            'serial_number': i,
            'ip_tab': 0,
            'open_tabs': 1
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

    print('\nПрофили запущены. Восстановление профилей...\n')

    bar = Bar("Восстановление профилей", max=len(profiles))
    threads = chunks([Thread(target=worker, args=(i, lines[i])) for i in range(len(profiles))], 2)
    for group in threads:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()
    bar.finish()

    print('\nРабота программы успешно завершена.')
    init_exit()
