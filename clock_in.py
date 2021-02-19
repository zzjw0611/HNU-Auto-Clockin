from aip import AipOcr
import requests
import json
import time

APP_ID = '23674789'
API_KEY = '8FGFY6cyLKGXunfB1HRmcb6U'
SECRET_KEY = 'oqkxn9w4fS0sIB1TlGja3wrHrdNSPoYS'
OCRClient = AipOcr(APP_ID, API_KEY, SECRET_KEY)

getimgvcode = json.loads(requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode').text)['data']['Token']
captcha = OCRClient.basicGeneralUrl(f'https://fangkong.hnu.edu.cn/imagevcode?token={getimgvcode}')['words_result'][0]['words']

login_info = {"Code":"201905010211","Password":"Abc2!0!linzepeng","VerCode":captcha,"Token":getimgvcode}

login_url = 'https://fangkong.hnu.edu.cn/api/v1/account/login'
set_cookie = requests.post(login_url, json=login_info)
ASPXAUTH = set_cookie.headers['Set-Cookie'][702:-8]
access_token = json.loads(set_cookie.text)['data']['AccessToken']

cookie = f'{ASPXAUTH}; TOKEN={getimgvcode}; Hm_lvt_d7e34467518a35dd690511f2596a570e=1612281837,1613093402,1613146382; pgv_pvi=4032871424'

clockin_url = 'https://fangkong.hnu.edu.cn/api/v1/clockinlog/add'
headers = {'Cookie': cookie}
clockin_data = {"Temperature":"null",
                "RealProvince":"福建省",
                "RealCity":"泉州市",
                "RealCounty":"泉港区",
                "RealAddress":"。",
                "IsUnusual":"0",
                "UnusualInfo":"",
                "IsTouch":"0",
                "IsInsulated":"0",
                "IsSuspected":"0",
                "IsDiagnosis":"0",
                "tripinfolist":[{"aTripDate":"","FromAdr":"","ToAdr":"","Number":"","trippersoninfolist":[]}],
                "toucherinfolist":[],
                "dailyinfo":{"IsVia":"0","DateTrip":""},
                "IsInCampus":"0",
                "IsViaHuBei":"0",
                "IsViaWuHan":"0",
                "InsulatedAddress":"",
                "TouchInfo":"",
                "IsNormalTemperature":"1",
                "Longitude":118.95317077636719,
                "Latitude":25.116409301757812}

clockin = requests.post(clockin_url, cookie=cookie, json=clockin_data)
print(clockin.text)