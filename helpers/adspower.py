import requests
from time import sleep

API_URl = 'http://localhost:50325/'


def check_adspower():
    try:
        requests.get(API_URl + 'status').json()
        sleep(1)
    except requests.exceptions.ConnectionError:
        raise Exception('The API is unavailable. Check if AdsPower is running')
    else:
        return True


def get_group_id(group_name):
    args = {
        'group_name': group_name
    }

    try:
        r = requests.get(API_URl + 'api/v1/group/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Couldn\'t find out if the group exists: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            if r['data']['list']:
                return r['data']['list'][0]['group_id']
            else:
                return None


def create_group(name):
    try:
        r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': name}).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r["msg"])
        else:
            return r['data']['group_id']


def create_profile(proxy_string=None, group_id='0'):
    if proxy_string:
        proxy_host, proxy_port, proxy_login, proxy_password = proxy_string.split(':')

        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'other',
                'proxy_type': 'socks5',
                'proxy_host': proxy_host,
                'proxy_port': proxy_port,
                'proxy_user': proxy_login,
                'proxy_password': proxy_password
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
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            return r['data']['serial_number']


def run_profile(serial_number):
    args = {
        'serial_number': serial_number,
        'ip_tab': 0
    }
    try:
        r = requests.get(API_URl + 'api/v1/browser/start',  params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            ws = r["data"]["ws"]["selenium"]
            driver_path = r["data"]["webdriver"]
            return ws, driver_path


def close_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        requests.get(API_URl + 'api/v1/browser/stop', params=args)
        sleep(1)
    except Exception as e:
        raise Exception(f'Failed to close the profile: {str(e)}')


def delete_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        r = requests.get(API_URl + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'The profile\'s user_id could not be found: {str(e)}')

    if not r['data']['list']:
        raise Exception('The profile to delete was not found')

    user_id = r['data']['list'][0]['user_id']

    try:
        r = requests.post(API_URl + 'api/v1/user/delete', json={'user_ids': [user_id]}).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Error deleting the profile: {str(e)}')

    if r['code'] != 0:
        raise Exception(r['msg'])


def get_profile(serial_number):
    args = {'serial_number': serial_number}

    try:
        r = requests.get(API_URl + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')

    if r['code'] != 0:
        raise Exception(r['msg'])

    if not r['data']['list']:
        raise Exception(f'Profile {serial_number} not found')

    return r['data']['list'][0]


def get_profiles_by_group_id(group_id):
    args = {
        'group_id': group_id,
        'page_size': 100
    }

    try:
        r = requests.get(API_URl + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')

    if r['code'] != 0:
        raise Exception(r['msg'])

    return r['data']['list']