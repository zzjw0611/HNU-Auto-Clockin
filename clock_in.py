from aip import AipOcr
import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, default=None)
parser.add_argument('--password', type=str, default=None)
parser.add_argument('--province', type=str, default=None)
parser.add_argument('--city', type=str, default=None)
parser.add_argument('--county', type=str, default=None)
parser.add_argument('--app_id', type=str, default=None)
parser.add_argument('--api_key', type=str, default=None)
parser.add_argument('--secret_key', type=str, default=None)
args = parser.parse_args()

OCRClient = AipOcr(args.app_id, args.api_key, args.secret_key)

def main():
    getimgvcode = json.loads(requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode').text)['data']['Token']
    captcha = OCRClient.basicGeneralUrl(f'https://fangkong.hnu.edu.cn/imagevcode?token={getimgvcode}')['words_result'][0]['words']
    login_info = {"Code":args.username,"Password":args.password,"VerCode":captcha,"Token":getimgvcode}

    login_url = 'https://fangkong.hnu.edu.cn/api/v1/account/login'
    set_cookie = requests.post(login_url, json=login_info)
    ASPXAUTH = set_cookie.headers['Set-Cookie'][702:-8]

    clockin_url = 'https://fangkong.hnu.edu.cn/api/v1/clockinlog/add'
    headers = {'Cookie': f'{ASPXAUTH}; TOKEN={getimgvcode}; Hm_lvt_d7e34467518a35dd690511f2596a570e=1612281837,1613093402,1613146382; pgv_pvi=4032871424'}
    clockin_data = {"Temperature":"null",
                    "RealProvince":args.province,
                    "RealCity":args.city,
                    "RealCounty":args.county,
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

    clockin = requests.post(clockin_url, headers=headers, json=clockin_data)
    if '成功' in clockin.text or '已提交' in clockin.text:
        isSucccess = 0
    else:
        isSucccess = 1

main()