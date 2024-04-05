from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import random
from string import digits, ascii_letters


def get_exts(driver: webdriver.Chrome):
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


def new_metamask(seed, ws, driver_path, password=None, metamask_id=None):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws)
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    if not metamask_id:
        sleep(5)

        current = driver.current_window_handle
        windows = driver.window_handles
        windows.remove(current)

        for window in windows:
            driver.switch_to.window(window)
            driver.close()

        driver.switch_to.window(current)

        try:
            driver.maximize_window()
        except:
            pass

        metamask_id = [i['id'] for i in get_exts(driver) if 'MetaMask' in i['name']][0]

        driver.get(f'chrome-extension://{metamask_id}/home.html#onboarding/welcome')
        driver.refresh()

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="import-srp__srp-word-0"]')))

    seed = seed.split(' ')
    for i in range(12):
        driver.find_element(By.XPATH, f'//input[@data-testid="import-srp__srp-word-{i}"]').send_keys(seed[i])

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    if not password:
        password = ''.join(random.choice(ascii_letters + digits) for _ in range(8))

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(password)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-confirm"]'))).send_keys(password)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

    WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    driver.get('about:blank')


def old_metamask(seed, ws, driver_path, password=None):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws)
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    sleep(5)

    current = driver.current_window_handle
    windows = driver.window_handles
    windows.remove(current)

    for window in windows:
        driver.switch_to.window(window)
        driver.close()

    driver.switch_to.window(current)

    try:
        driver.maximize_window()
    except:
        pass

    metamask_id = [i['id'] for i in get_exts(driver) if 'MetaMask' in i['name']][0]

    driver.get(f'chrome-extension://{metamask_id}/home.html')
    driver.refresh()

    try:
        WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//a[@class="button btn-link unlock-page__link"]'))).click()
    except:
        new_metamask(seed, ws, driver_path, password, metamask_id)
        return

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="import-srp__srp-word-0"]')))

    seed = seed.split(' ')
    for i in range(12):
        driver.find_element(By.XPATH, f'//input[@data-testid="import-srp__srp-word-{i}"]').send_keys(seed[i])

    if not password:
        password = ''.join(random.choice(ascii_letters + digits) for _ in range(8))

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-vault-password"]'))).send_keys(password)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-vault-confirm-password"]'))).send_keys(password)

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-new-vault-submit-button"]'))).click()

    WebDriverWait(driver, 30).until(ec.url_to_be(f'chrome-extension://{metamask_id}/home.html#'))

    driver.get('about:blank')
