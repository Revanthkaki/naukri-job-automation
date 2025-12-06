import requests
import time
from config import Config

def solve_captcha(site_key, page_url):
    if not Config.TWOCAPTCHA_API_KEY:
        return None
    try:
        submit_url = "http://2captcha.com/in.php"
        params = {
            'key': Config.TWOCAPTCHA_API_KEY,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        response = requests.post(submit_url, data=params)
        result = response.json()
        if result.get('status') != 1:
            return None
        captcha_id = result.get('request')
        time.sleep(20)
        for _ in range(12):
            check_url = f"http://2captcha.com/res.php?key={Config.TWOCAPTCHA_API_KEY}&action=get&id={captcha_id}&json=1"
            check_response = requests.get(check_url)
            check_result = check_response.json()
            if check_result.get('status') == 1:
                return check_result.get('request')
            time.sleep(5)
        return None
    except Exception as e:
        print(f"CAPTCHA failed: {e}")
        return None
