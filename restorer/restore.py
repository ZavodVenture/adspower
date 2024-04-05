from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
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
from selenium.webdriver.common.keys import Keys


def init_exit():
    input("\nPress Enter to close program...")
    exit()


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result


def get_exts(driver):
    driver.get('chrome://extensions/')

    sleep(5)

    script = '''ext_manager = document.getElementsByTagName('extensions-manager')[0].shadowRoot;
    item_list = ext_manager.getElementById('items-list').shadowRoot;
    container = item_list.getElementById('container');
    extension_list = container.getElementsByClassName('items-container')[1].getElementsByTagName('extensions-item');

    var extensions = [];

    for (i = 0; i < extension_list.length; i++) {
        console.log(extension_list[i]);
        name = extension_list[i].shadowRoot.getElementById('name').textContent;
        id = extension_list[i].id;
        extensions.push({'id': id, 'name': name});
    }

    return extensions;'''

    return driver.execute_script(script)


def new_backpack(driver, metamask_index, martin_id):
    driver.get(f'chrome-extension://{martin_id}/options.html?onboarding=true')

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div/div[3]/button[2]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[2]/button[1]'))).click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//input')))

    seed = metamask[metamask_index].split()

    inputs = driver.find_elements(By.XPATH, '//input')

    for j in range(12):
        inputs[j].send_keys(seed[j])

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[3]/button'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[2]/button[2]'))).click()

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[2]/li/button')))
    sleep(10)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[2]/li/button'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=":r2a:"]/div/div[2]'))).click()
    sleep(1)

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[3]/div/div[1]/div/div[1]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[4]/button'))).click()

    meta_password = ''.join(random.choice(ascii_letters + digits) for _ in range(8)) if not config['settings'][
        'password'] else config['settings']['password']

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/form/div[2]/div[1]/span/input'))).send_keys(meta_password)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/form/div[2]/div[2]/span/input'))).send_keys(meta_password)

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/form/div[3]/button[1]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/form/div[3]/button[2]'))).click()

    sleep(2)

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[1]/div[4]/button[2]'))).click()

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="options"]/span/span/div/div/div/div/div[2]/button')))

    driver.get(f'chrome-extension://{martin_id}/popup.html')

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/div/div[3]/button'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/ul[2]/div[2]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/ul[1]/div[1]'))).click()


    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/form/div[1]/div/div/div/input'))).send_keys(Keys.CONTROL + 'a')
    sleep(0.1)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/form/div[1]/div/div/div/input'))).send_keys('999')

    el = driver.find_element(By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[1]/form/div[2]/button[2]')

    driver.execute_script('arguments[0].click()', el)
    sleep(1)

    driver.get('about:blank')


def old_backpack(driver: webdriver.Chrome, metamask_index, martin_id):
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div[1]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/span[1]/span/div/div/div[2]/div[5]/div[1]/div/div[1]/div/div/div[1]'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/span/span/div[2]/div[1]/div/div/div[2]/div[2]'))).click()
    sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    new_backpack(driver, metamask_index, martin_id)


def import_backpack(driver: webdriver.Chrome, metamask_index):
    extensions = get_exts(driver)

    try:
        backpack_id = [ex['id'] for ex in extensions if 'Backpack' in ex['name']][0]
    except IndexError:
        raise Exception('Martian extension not found')

    driver.get(f'chrome-extension://{backpack_id}/popup.html')
    sleep(3)
    driver.switch_to.window(driver.window_handles[0])

    if driver.current_url == f'chrome-extension://{backpack_id}/options.html?onboarding=true':
        new_backpack(driver, metamask_index, backpack_id)
    else:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
        except TimeoutException:
            return
        else:
            old_backpack(driver, metamask_index, backpack_id)


def worker(ws_index, metamask_index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[ws_index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    sleep(3)

    try:
        driver.maximize_window()
    except:
        pass

    tabs = driver.window_handles
    curr = driver.current_window_handle
    for tab in tabs:
        if tab == curr:
            continue
        driver.switch_to.window(tab)
        driver.close()
    driver.switch_to.window(curr)
    driver.get('about:blank')

    import_backpack(driver, metamask_index)

    driver.get('about:blank')
    bar.next()


config = ConfigParser()
config.read('restore.ini')

API_URl = 'http://localhost:50325/'

if __name__ == '__main__':
    print('Pre-launch verification...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('The API is unavailable. Check if AdsPower is running.')
        init_exit()

    sleep(1)

    metamask = None
    try:
        metamask = open(config['settings']['metamask_file'])
        metamask = metamask.read().split('\n')
        if not metamask[-1]:
            metamask = metamask[:-1]
    except FileNotFoundError:
        print(f'File {config["settings"]["metamask_file"]} not found')
        init_exit()

    print('Verification is complete, search for rows associated with profiles...\n')

    first_profile = int(config['settings']['first_profile'])
    profile_number = int(config['settings']['profile_number'])

    profiles = list(range(first_profile, profile_number + first_profile))
    lines = []

    bar = Bar('Searching rows', max=len(profiles))

    for profile in profiles:
        try:
            r = requests.get(API_URl + 'api/v1/user/list', params={'serial_number': profile}).json()
        except Exception as e:
            bar.finish()
            print(f'Couldn\'t find a profile with a number {profile}: {e}')
            init_exit()
        else:
            sleep(1)
            if r['code'] != 0:
                bar.finish()
                print(f'Couldn\'t find a profile with a number {profile}: {r["msg"]}')
                init_exit()
            else:
                if not r['data']['list']:
                    bar.finish()
                    print(f'Couldn\'t find a profile with a number {profile}')
                    init_exit()

                group_id = r['data']['list'][0]['group_id']
                group_name = r['data']['list'][0]['group_name']

                offset = 0
                try:
                    offset = int(re.findall(r'Profiles(\d*)-\d*_.*', group_name)[0]) - 1
                except Exception as e:
                    bar.finish()
                    print('Could not determine the number of the first profile in the group (the group has a non-standard name)')
                    init_exit()

                try:
                    r = requests.get(API_URl + 'api/v1/user/list', params={'group_id': group_id, 'page_size': 100}).json()
                except Exception as e:
                    bar.finish()
                    print(f'Could not find profiles in the group: {e}')
                    init_exit()
                else:
                    sleep(1)
                    if r['code'] != 0:
                        bar.finish()
                        print(f'Could not find profiles in the group: {r["msg"]}')
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
                            bar.finish()
                            print(f'Could not find the line number for the profile {profile}')
                            init_exit()
                        bar.next()

    bar.finish()

    print('\nThe rows were found successfully. Launching profiles...\n')

    bar = Bar('Launching profiles...', max=len(profiles))
    ws_list = []
    driver_path = ''

    for i in profiles:
        args = {
            'serial_number': i,
            'ip_tab': 0,
            'open_tabs': 0
        }

        try:
            r = requests.get(API_URl + 'api/v1/browser/start', params=args).json()
        except Exception as e:
            bar.finish()
            print('\nFailed to launch profile: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                bar.finish()
                print('\nFailed to launch profile: ' + r['msg'])
                init_exit()
            else:
                ws_list.append(r["data"]["ws"]["selenium"])
                if not driver_path:
                    driver_path = r["data"]["webdriver"]
                bar.next()
        sleep(1)

    bar.finish()

    print('\nProfiles are running. Restoring profiles...\n')

    bar = Bar("Restoring profiles...", max=len(profiles))
    threads = chunks([Thread(target=worker, args=(i, lines[i])) for i in range(len(profiles))], 2)
    for group in threads:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()
    bar.finish()

    print('\nThe program has been successfully completed.')
    init_exit()
