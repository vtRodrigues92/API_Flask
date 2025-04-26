from flask import Flask, make_response, jsonify
import requests, json
from waitress import serve
from datetime import datetime
from flask import request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.options import Options
#from webdriver_manager.core.os_manager import ChromeType
#from fake_useragent import UserAgent
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#import threading
#from selenium.webdriver.chrome.service import Service

app = Flask(__name__)


### Decorator que retorna a URL do Game
@app.route('/URL/<s7oryo9stv>,<game_id>,<vendor_id>,<vendor_limit_id>' , methods=['GET'])
def pegar_url_game(s7oryo9stv, game_id, vendor_id, vendor_limit_id):

    try:

        urlEvo = "https://odin.sportingtech.com/api/user/casinoapi/openGame"

        payloadEvo = {"requestBody":{"gameId":f'{game_id}',\
                        "channel":"web",\
                        "vendorLimitId":f'{vendor_limit_id}',\
                        "vendorId":f'{vendor_id}',\
                        "redirectUrl":f"https://vembetar.com/ptb/games/livecasino/detail/normal/{game_id}/{vendor_limit_id}"},\
                        "identity":"null",\
                        "device":"d",\
                        "languageId":23
                        }

        headersEvo = {"Content-Type": "application/json",
                    "Origin":"https://vembetar.com",
                    "Referer":"https://vembetar.com/",
                    "s7oryO9STV":s7oryo9stv,
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "X-PGDevice":"m"}

        dadosEvo = requests.post(urlEvo, json=payloadEvo, headers=headersEvo)

        gameUrl = json.loads(dadosEvo.text)['data']['gameUrl']

        data = {'status':'true','game_url':gameUrl}

        print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data)

        return data

    except Exception as e:

        print(e)

        data = {'status':'false','game_url':dadosEvo.content}


### Decorator que faz login na greenbet
@app.route('/login-greenbet/' , methods=['POST'])
def logar_greenbet():

    try:

        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        except:pass

        usuario = json.loads(request.data)['user']
        senha =   json.loads(request.data)['pass']

        # Definindo opções para o browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('disable-extensions')
        chrome_options.add_argument('disable-popup-blocking')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        #print(user_agent)
        
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("general.useragent.override", user_agent)
        #options = Options()
        #options.headless = True
        
        #driver = webdriver.Firefox(firefox_profile=profile, executable_path="C:\\Utility\\BrowserDrivers\\geckodriver.exe") 
        #driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=GeckoDriverManager().install())
        #driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)


        # Navigate to url
        driver.get("https://greenbets.io/api/client/clients:login-with-form")

        # Get all available cookies
        cookies = driver.get_cookies()

        cf_bm = cookies[0]['value']

        driver.close()
        
        user = usuario
        password = senha

        headers = {
                    "Device":"desktop",
                    "Content-Type": "application/json",
                    "Cookie":f'__cf_bm={cf_bm}',
                    "Origin":"https://greenbets.io",
                    "Referer":"https://greenbets.io/casino?cmd=signin&path=loginMultichannel",
                    "X-Project-Id":"103",
                    "User-Agent":user_agent,
                    "Version":"3.17.12"    
                }

        payload = {
                    "id":3498,
                    "values":{
                                "CAPTCHA_INPUT":"",
                                "MULTICHANNEL":user,
                                "PASSWORD":password
                            },
                    "fingerprint": 'W3sia2V5IjoidXNlckFnZW50IiwidmFsdWUiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE1LjAuMC4wIFNhZmFyaS81MzcuMzYifSx7ImtleSI6IndlYmRyaXZlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJsYW5ndWFnZSIsInZhbHVlIjoicHQtQlIifSx7ImtleSI6ImNvbG9yRGVwdGgiLCJ2YWx1ZSI6MjR9LHsia2V5IjoiZGV2aWNlTWVtb3J5IiwidmFsdWUiOjh9LHsia2V5IjoiaGFyZHdhcmVDb25jdXJyZW5jeSIsInZhbHVlIjo4fSx7ImtleSI6InNjcmVlblJlc29sdXRpb24iLCJ2YWx1ZSI6Wzc2OCwxMzY2XX0seyJrZXkiOiJhdmFpbGFibGVTY3JlZW5SZXNvbHV0aW9uIiwidmFsdWUiOls3MjAsMTM2Nl19LHsia2V5IjoidGltZXpvbmVPZmZzZXQiLCJ2YWx1ZSI6MTgwfSx7ImtleSI6InRpbWV6b25lIiwidmFsdWUiOiJBbWVyaWNhL1Nhb19QYXVsbyJ9LHsia2V5Ijoic2Vzc2lvblN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJsb2NhbFN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJpbmRleGVkRGIiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJhZGRCZWhhdmlvciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJvcGVuRGF0YWJhc2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJjcHVDbGFzcyIsInZhbHVlIjoibm90IGF2YWlsYWJsZSJ9LHsia2V5IjoicGxhdGZvcm0iLCJ2YWx1ZSI6IldpbjMyIn0seyJrZXkiOiJwbHVnaW5zIiwidmFsdWUiOltbIlBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiQ2hyb21lIFBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiQ2hyb21pdW0gUERGIFZpZXdlciIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV0sWyJNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXSxbIldlYktpdCBidWlsdC1pbiBQREYiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dXX0seyJrZXkiOiJ3ZWJnbFZlbmRvckFuZFJlbmRlcmVyIiwidmFsdWUiOiJHb29nbGUgSW5jLiAoSW50ZWwpfkFOR0xFIChJbnRlbCwgSW50ZWwoUikgVUhEIEdyYXBoaWNzIDYyMCBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKSJ9LHsia2V5IjoiYWRCbG9jayIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJoYXNMaWVkTGFuZ3VhZ2VzIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRSZXNvbHV0aW9uIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRPcyIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJoYXNMaWVkQnJvd3NlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJ0b3VjaFN1cHBvcnQiLCJ2YWx1ZSI6WzAsZmFsc2UsZmFsc2VdfSx7ImtleSI6ImZvbnRzIiwidmFsdWUiOlsiQXJpYWwiLCJBcmlhbCBCbGFjayIsIkFyaWFsIE5hcnJvdyIsIkNhbGlicmkiLCJDYW1icmlhIiwiQ2FtYnJpYSBNYXRoIiwiQ29taWMgU2FucyBNUyIsIkNvbnNvbGFzIiwiQ291cmllciIsIkNvdXJpZXIgTmV3IiwiR2VvcmdpYSIsIkhlbHZldGljYSIsIkltcGFjdCIsIkx1Y2lkYSBDb25zb2xlIiwiTHVjaWRhIFNhbnMgVW5pY29kZSIsIk1pY3Jvc29mdCBTYW5zIFNlcmlmIiwiTVMgR290aGljIiwiTVMgUEdvdGhpYyIsIk1TIFNhbnMgU2VyaWYiLCJNUyBTZXJpZiIsIlBhbGF0aW5vIExpbm90eXBlIiwiU2Vnb2UgUHJpbnQiLCJTZWdvZSBTY3JpcHQiLCJTZWdvZSBVSSIsIlNlZ29lIFVJIExpZ2h0IiwiU2Vnb2UgVUkgU2VtaWJvbGQiLCJTZWdvZSBVSSBTeW1ib2wiLCJUYWhvbWEiLCJUaW1lcyIsIlRpbWVzIE5ldyBSb21hbiIsIlRyZWJ1Y2hldCBNUyIsIlZlcmRhbmEiLCJXaW5nZGluZ3MiXX0seyJrZXkiOiJhdWRpbyIsInZhbHVlIjoiMTI0LjA0MzQ3NTI3NTE2MDc0In1d'
                }

        URL = 'https://greenbets.io/api/client/clients:login-with-form'
        

        response = requests.post(URL, json=payload, headers=headers)

        if response.status_code == 200:
            
            session_token = json.loads(response.content)['sessionToken']

            data_success = {'status':'true','s7oryo9stv':session_token, 'cookie':cf_bm, 'user-agent':user_agent}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success
            

        else:
            
            data_failure = {'status':'false','s7oryo9stv':response.text}
            
            return data_failure



    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','s7oryo9stv':e}  
        return data_failure



### Decorator que faz login na greenbet
@app.route('/login-inbrazza/' , methods=['POST'])
def logar_inbrazza():

    try:

        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        except:pass

        usuario = json.loads(request.data)['user']
        senha =   json.loads(request.data)['pass']

        # Definindo opções para o browser
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('disable-extensions')
        chrome_options.add_argument('disable-popup-blocking')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        #print(user_agent)
        
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("general.useragent.override", user_agent)
        #options = Options()
        #options.headless = True
        
        #driver = webdriver.Firefox(firefox_profile=profile, executable_path="C:\\Utility\\BrowserDrivers\\geckodriver.exe") 
        #driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=GeckoDriverManager().install())
        #driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)


        # Navigate to url
        driver.get("https://inbrazza.bet/api/client/clients:login-with-form")

        # Get all available cookies
        cookies = driver.get_cookies()

        cf_bm = cookies[0]['value']
        
        driver.close()

        user = usuario
        password = senha

        headers = {
                    "Device":"desktop",
                    "Content-Type": "application/json",
                    "Cookie":f'__cf_bm={cf_bm}',
                    "Origin":"https://inbrazza.bet",
                    "Referer":"https://inbrazza.bet/casino?cmd=signin&path=loginMultichannel",
                    "X-Project-Id":"94",
                    "User-Agent":user_agent,
                    "Version":"3.17.12"    
                }

        payload = {
                    "id":3426,
                    "values":{
                                "CAPTCHA_INPUT":"",
                                "MULTICHANNEL":user,
                                "PASSWORD":password
                            },
                    "fingerprint":"W3sia2V5IjoidXNlckFnZW50IiwidmFsdWUiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE0LjAuMC4wIFNhZmFyaS81MzcuMzYifSx7ImtleSI6IndlYmRyaXZlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJsYW5ndWFnZSIsInZhbHVlIjoicHQtQlIifSx7ImtleSI6ImNvbG9yRGVwdGgiLCJ2YWx1ZSI6MjR9LHsia2V5IjoiZGV2aWNlTWVtb3J5IiwidmFsdWUiOjh9LHsia2V5IjoiaGFyZHdhcmVDb25jdXJyZW5jeSIsInZhbHVlIjo4fSx7ImtleSI6InNjcmVlblJlc29sdXRpb24iLCJ2YWx1ZSI6Wzc2OCwxMzY2XX0seyJrZXkiOiJhdmFpbGFibGVTY3JlZW5SZXNvbHV0aW9uIiwidmFsdWUiOls3MjAsMTM2Nl19LHsia2V5IjoidGltZXpvbmVPZmZzZXQiLCJ2YWx1ZSI6MTgwfSx7ImtleSI6InRpbWV6b25lIiwidmFsdWUiOiJBbWVyaWNhL1Nhb19QYXVsbyJ9LHsia2V5Ijoic2Vzc2lvblN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJsb2NhbFN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJpbmRleGVkRGIiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJhZGRCZWhhdmlvciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJvcGVuRGF0YWJhc2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJjcHVDbGFzcyIsInZhbHVlIjoibm90IGF2YWlsYWJsZSJ9LHsia2V5IjoicGxhdGZvcm0iLCJ2YWx1ZSI6IldpbjMyIn0seyJrZXkiOiJwbHVnaW5zIiwidmFsdWUiOltbIlBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiQ2hyb21lIFBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiQ2hyb21pdW0gUERGIFZpZXdlciIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV0sWyJNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXSxbIldlYktpdCBidWlsdC1pbiBQREYiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dXX0seyJrZXkiOiJ3ZWJnbFZlbmRvckFuZFJlbmRlcmVyIiwidmFsdWUiOiJHb29nbGUgSW5jLiAoSW50ZWwpfkFOR0xFIChJbnRlbCwgSW50ZWwoUikgVUhEIEdyYXBoaWNzIDYyMCBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKSJ9LHsia2V5IjoiYWRCbG9jayIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJoYXNMaWVkTGFuZ3VhZ2VzIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRSZXNvbHV0aW9uIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRPcyIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJoYXNMaWVkQnJvd3NlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJ0b3VjaFN1cHBvcnQiLCJ2YWx1ZSI6WzAsZmFsc2UsZmFsc2VdfSx7ImtleSI6ImZvbnRzIiwidmFsdWUiOlsiQXJpYWwiLCJBcmlhbCBCbGFjayIsIkFyaWFsIE5hcnJvdyIsIkNhbGlicmkiLCJDYW1icmlhIiwiQ2FtYnJpYSBNYXRoIiwiQ29taWMgU2FucyBNUyIsIkNvbnNvbGFzIiwiQ291cmllciIsIkNvdXJpZXIgTmV3IiwiR2VvcmdpYSIsIkhlbHZldGljYSIsIkltcGFjdCIsIkx1Y2lkYSBDb25zb2xlIiwiTHVjaWRhIFNhbnMgVW5pY29kZSIsIk1pY3Jvc29mdCBTYW5zIFNlcmlmIiwiTVMgR290aGljIiwiTVMgUEdvdGhpYyIsIk1TIFNhbnMgU2VyaWYiLCJNUyBTZXJpZiIsIlBhbGF0aW5vIExpbm90eXBlIiwiU2Vnb2UgUHJpbnQiLCJTZWdvZSBTY3JpcHQiLCJTZWdvZSBVSSIsIlNlZ29lIFVJIExpZ2h0IiwiU2Vnb2UgVUkgU2VtaWJvbGQiLCJTZWdvZSBVSSBTeW1ib2wiLCJUYWhvbWEiLCJUaW1lcyIsIlRpbWVzIE5ldyBSb21hbiIsIlRyZWJ1Y2hldCBNUyIsIlZlcmRhbmEiLCJXaW5nZGluZ3MiXX0seyJrZXkiOiJhdWRpbyIsInZhbHVlIjoiMTI0LjA0MzQ3NTI3NTE2MDc0In1d"}


        URL = 'https://inbrazza.bet/api/client/clients:login-with-form'
        

        response = requests.post(URL, json=payload, headers=headers)

        if response.status_code == 200:
            
            session_token = json.loads(response.content)['sessionToken']

            data_success = {'status':'true','s7oryo9stv':session_token, 'cookie':cf_bm, 'user-agent':user_agent}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success
            

        else:
            
            data_failure = {'status':'false','s7oryo9stv':response.text}
            
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','s7oryo9stv':e}

        return data_failure



### Decorator que faz login na decolabet
@app.route('/login-decolabet/' , methods=['POST'])
def logar_decolabet():

    try:

        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        except:pass

        usuario = json.loads(request.data)['user']
        senha =   json.loads(request.data)['pass']

        # Definindo opções para o browser
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('disable-extensions')
        chrome_options.add_argument('disable-popup-blocking')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')

        driver = webdriver.Chrome(options=chrome_options)


        # Navigate to url
        driver.get("https://decolabet.com/api/client/clients:login-with-form")

        # Get all available cookies
        cookies = driver.get_cookies()

        cf_bm = cookies[0]['value']

        driver.close()
        
        user = usuario
        password = senha

        headers = {
                "Device":"desktop",
                "Content-Type": "application/json",
                "Cookie":f'__cf_bm={cf_bm}',
                "Origin":"https://decolabet.com",
                "Referer":"https://decolabet.com/casino?cmd=signin&path=loginMultichannel",
                "X-Project-Id":"88",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                "X-Locale":"BR_PT",
                "Version":"3.17.12"    
        }

        payload = {
                    "id":3498,
                    "values":{
                                "CAPTCHA_INPUT":"",
                                "MULTICHANNEL":user,
                                "PASSWORD":password
                            },
                    "fingerprint": "W3sia2V5IjoidXNlckFnZW50IiwidmFsdWUiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE1LjAuMC4wIFNhZmFyaS81MzcuMzYifSx7ImtleSI6IndlYmRyaXZlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJsYW5ndWFnZSIsInZhbHVlIjoicHQtQlIifSx7ImtleSI6ImNvbG9yRGVwdGgiLCJ2YWx1ZSI6MjR9LHsia2V5IjoiZGV2aWNlTWVtb3J5IiwidmFsdWUiOjh9LHsia2V5IjoiaGFyZHdhcmVDb25jdXJyZW5jeSIsInZhbHVlIjo4fSx7ImtleSI6InNjcmVlblJlc29sdXRpb24iLCJ2YWx1ZSI6WzE5MjAsMTA4MF19LHsia2V5IjoiYXZhaWxhYmxlU2NyZWVuUmVzb2x1dGlvbiIsInZhbHVlIjpbMTkyMCwxMDMyXX0seyJrZXkiOiJ0aW1lem9uZU9mZnNldCIsInZhbHVlIjoxODB9LHsia2V5IjoidGltZXpvbmUiLCJ2YWx1ZSI6IkFtZXJpY2EvU2FvX1BhdWxvIn0seyJrZXkiOiJzZXNzaW9uU3RvcmFnZSIsInZhbHVlIjp0cnVlfSx7ImtleSI6ImxvY2FsU3RvcmFnZSIsInZhbHVlIjp0cnVlfSx7ImtleSI6ImluZGV4ZWREYiIsInZhbHVlIjp0cnVlfSx7ImtleSI6ImFkZEJlaGF2aW9yIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Im9wZW5EYXRhYmFzZSIsInZhbHVlIjp0cnVlfSx7ImtleSI6ImNwdUNsYXNzIiwidmFsdWUiOiJub3QgYXZhaWxhYmxlIn0seyJrZXkiOiJwbGF0Zm9ybSIsInZhbHVlIjoiV2luMzIifSx7ImtleSI6InBsdWdpbnMiLCJ2YWx1ZSI6W1siUERGIFZpZXdlciIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV0sWyJDaHJvbWUgUERGIFZpZXdlciIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV0sWyJDaHJvbWl1bSBQREYgVmlld2VyIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXSxbIk1pY3Jvc29mdCBFZGdlIFBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiV2ViS2l0IGJ1aWx0LWluIFBERiIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV1dfSx7ImtleSI6IndlYmdsVmVuZG9yQW5kUmVuZGVyZXIiLCJ2YWx1ZSI6Ikdvb2dsZSBJbmMuIChJbnRlbCl+QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjIwIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpIn0seyJrZXkiOiJhZEJsb2NrIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRMYW5ndWFnZXMiLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFzTGllZFJlc29sdXRpb24iLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFzTGllZE9zIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRCcm93c2VyIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6InRvdWNoU3VwcG9ydCIsInZhbHVlIjpbMCxmYWxzZSxmYWxzZV19LHsia2V5IjoiZm9udHMiLCJ2YWx1ZSI6WyJBcmlhbCIsIkFyaWFsIEJsYWNrIiwiQXJpYWwgTmFycm93IiwiQ2FsaWJyaSIsIkNhbWJyaWEiLCJDYW1icmlhIE1hdGgiLCJDb21pYyBTYW5zIE1TIiwiQ29uc29sYXMiLCJDb3VyaWVyIiwiQ291cmllciBOZXciLCJHZW9yZ2lhIiwiSGVsdmV0aWNhIiwiSW1wYWN0IiwiTHVjaWRhIENvbnNvbGUiLCJMdWNpZGEgU2FucyBVbmljb2RlIiwiTWljcm9zb2Z0IFNhbnMgU2VyaWYiLCJNUyBHb3RoaWMiLCJNUyBQR290aGljIiwiTVMgU2FucyBTZXJpZiIsIk1TIFNlcmlmIiwiUGFsYXRpbm8gTGlub3R5cGUiLCJTZWdvZSBQcmludCIsIlNlZ29lIFNjcmlwdCIsIlNlZ29lIFVJIiwiU2Vnb2UgVUkgTGlnaHQiLCJTZWdvZSBVSSBTZW1pYm9sZCIsIlNlZ29lIFVJIFN5bWJvbCIsIlRhaG9tYSIsIlRpbWVzIiwiVGltZXMgTmV3IFJvbWFuIiwiVHJlYnVjaGV0IE1TIiwiVmVyZGFuYSIsIldpbmdkaW5ncyJdfSx7ImtleSI6ImF1ZGlvIiwidmFsdWUiOiIxMjQuMDQzNDc1Mjc1MTYwNzQifV0="
                    }

        URL = 'https://decolabet.com/api/client/clients:login-with-form'
        

        response = requests.post(URL, json=payload, headers=headers)

        if response.status_code == 200:
            
            session_token = json.loads(response.content)['sessionToken']

            data_success = {'status':'true','s7oryo9stv':session_token, 'cookie':cf_bm, 'user-agent':user_agent}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success
            

        else:
            
            data_failure = {'status':'false','s7oryo9stv':response.text}
            
            return data_failure



    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','s7oryo9stv':e}  
        return data_failure



### Decorator que faz login na decolabet
@app.route('/login-vembetar/' , methods=['POST'])
def logar_vembetar():
    try:

        #try:
        #    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        #except:pass

        usuario = json.loads(request.data)['user']
        senha =   json.loads(request.data)['pass']

        # define your proxies in dictionary  
        proxies = {'http': 'http://brd-customer-hl_aed823d1-zone-proxy_2023_daniel-country-br:f3d9e8chmago@brd.superproxy.io:22225',
                    'https': 'http://brd-customer-hl_aed823d1-zone-proxy_2023_daniel-country-br:f3d9e8chmago@brd.superproxy.io:22225'}
        
        # Definindo opções para o browser
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless=new")
        #chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('disable-extensions')
        chrome_options.add_argument('disable-popup-blocking')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        #print(user_agent)
        
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("general.useragent.override", user_agent)
        #options = Options()
        #options.headless = True
        
        #driver = webdriver.Firefox(firefox_profile=profile, executable_path="C:\\Utility\\BrowserDrivers\\geckodriver.exe") 
        #driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=GeckoDriverManager().install())
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        #driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, version='116.0.5845.97').install(),chrome_options=chrome_options)    
        #driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, version='114.0.5735.90').install(),chrome_options=chrome_options)
            
        # Navigate to url
        driver.get("https://vembetar.com/prejogo/")

        # Get all available cookies
        cookies = driver.get_cookies()

        PHPSESSID = cookies[1]['value']
        CF_BM = cookies[0]['value']
        FW_CRM = 'c82ee95f-2820-42e2-acf9-c7f4e9d40a95'
        
        url = 'https://vembetar.com/prejogo/'
        
        #usuario = 'jackvieira'
        #senha = 'Rod20271179#'

        data = {
            'login': '1',
            'username': usuario,
            'password': senha
        }

        headers = {
                "authority":"https://vembetar.com",
                "method":"POST",
                "path":"/prejogo/",
                "scheme":"https",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                "Cache-Control":"max-age=0",
                "Content-Length":"51",
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":f'PHPSESSID={PHPSESSID}; __cf_bm={CF_BM}; _fw_crm_v={FW_CRM}',
                "Origin":"https://vembetar.com",
                "Referer":"https://vembetar.com/prejogo/",
                "Sec-Ch-Ua":'Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                "Sec-Ch-Ua-Mobile":"?0",
                "Sec-Ch-Ua-Platform":"Windows",
                "Sec-Fetch-Dest":"document",
                "Sec-Fetch-Mode":"navigate",
                "Sec-Fetch-Site":"same-origin",
                "Sec-Fetch-User":"?1",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }

        #REQUISIÇÃO SEM PROXY
        #response = requests.post(url, data=data, headers=headers)

        #REQUISIÇÃO COM PROXY
        response = requests.post(url, data=data, headers=headers, proxies=proxies)

        if response.status_code == 200 and 'Último' in response.text:
                
            PHPSESSID = response.headers.get('Set-Cookie').split('PHPSESSID=')[1].split('; path=')[0]
            CF_BM = response.headers.get('Set-Cookie').split('__cf_bm=')[1].split('; path=/; ')[0]

            data_success = {'status':'true','phpsessid':PHPSESSID, 'cf_bm':CF_BM}
            
            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)
            print('\n\n')

            return data_success
            

        else:
            
            data_failure = {'status':'false','PHPSESSID':response.text}
            
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','PHPSESSID':e}

        return data_failure



### Decorator que retorna a URL do game
@app.route('/open-game-greenbet/' , methods=['POST'])
def open_game_greenbet():

    try:
        
        s7oryo9stv = json.loads(request.data)['s7oryo9stv']
        game_id =  json.loads(request.data)['game_id']
        cookie =   json.loads(request.data)['cookie']
        user_agent = json.loads(request.data)['user-agent']

        #### OPEN GAME
       
        headers = {
                    "Authorization":s7oryo9stv,
                    "Content-Type": "application/json",
                    "Cookie":f'__cf_bm={cookie}', # COOKIE É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                    "Device":"mobile",
                    "Referer":f"https://greenbets.io/casino/game/{game_id}",
                    "User-Agent":user_agent, # USER AGENT É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                    "Version":"3.17.12",    
                    "X-Project-Id":"103"
                }

        url_open_game = f'https://greenbets.io/api/gs/getUrl?game={game_id}&locale=BR_PT'
        
        response = requests.get(url_open_game, headers=headers)

        if response.status_code == 200:

            url_game = json.loads(response.content)['data']['link']

            data_success = {'status':'true','url_game':url_game}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success

        else:

            data_failure = {'status':'false','url_game':response.text}
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','url_game':e}

        return data_failure
        
        #### CONTINUA CASO O GAME FOR CASSINO AO VIVO (CONECTANDO NA ATLAS EVO)
        #response = requests.get(url_game, allow_redirects=False)

        #if response.status_code == 302:
            
        #    iframe_location = 'https://atlas.evo-games.com'+response.headers.get('Location')
        #    jsession_id = response.headers.get('Location').split('JSESSIONID=')[1].split('&params=')[0]

        #    print('Success -- ', iframe_location)

        #else:
        #    print('Failure')



    except:pass



### Decorator que retorna a URL do game
@app.route('/open-game-inbrazza/' , methods=['POST'])
def open_game_inbrazza():

    try:
        
        s7oryo9stv = json.loads(request.data)['s7oryo9stv']
        game_id =  json.loads(request.data)['game_id']
        cookie =   json.loads(request.data)['cookie']
        user_agent = json.loads(request.data)['user-agent']

        #### OPEN GAME
       
        headers = {
                "Authorization":s7oryo9stv,
                "Content-Type": "application/json",
                "Cookie":f'__cf_bm={cookie}', # COOKIE É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                "Device":"desktop",
                "Referer":f"https://inbrazza.bet/live-casino/game/{game_id}",
                "User-Agent":user_agent, # USER AGENT É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                "Version":"3.17.12",    
                "X-Project-Id":"94"
              }

        url_open_game = f'https://inbrazza.bet/api/gs/getUrl?game={game_id}&locale=BR_PT'
    
        response = requests.get(url_open_game, headers=headers)

        if response.status_code == 200:

            url_game = json.loads(response.content)['data']['link']

            data_success = {'status':'true','url_game':url_game}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success

        else:

            data_failure = {'status':'false','url_game':response.text}
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','url_game':e}

        return data_failure
        
        #### CONTINUA CASO O GAME FOR CASSINO AO VIVO (CONECTANDO NA ATLAS EVO)
        #response = requests.get(url_game, allow_redirects=False)

        #if response.status_code == 302:
            
        #    iframe_location = 'https://atlas.evo-games.com'+response.headers.get('Location')
        #    jsession_id = response.headers.get('Location').split('JSESSIONID=')[1].split('&params=')[0]

        #    print('Success -- ', iframe_location)

        #else:
        #    print('Failure')



    except:pass



### Decorator que retorna a URL do game
@app.route('/open-game-decolabet/' , methods=['POST'])
def open_game_decolabet():

    try:
        
        s7oryo9stv = json.loads(request.data)['s7oryo9stv']
        game_id =  '1950574'#json.loads(request.data)['game_id']
        cookie =   json.loads(request.data)['cookie']
        user_agent = json.loads(request.data)['user-agent']

        #### OPEN GAME
       
        headers = {
                    "Authorization":s7oryo9stv,
                    "Content-Type": "application/json",
                    "Cookie":f'__cf_bm={cookie}', # COOKIE É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                    "Device":"mobile",
                    "Referer":f"https://decolabet.com/casino/game/{game_id}",
                    "User-Agent":user_agent, # USER AGENT É UMA VARIAVEL QUE VEM DO ARQUIVO LOGIN-INBRAZZA
                    "Version":"3.17.12",    
                    "X-Project-Id":"88",
                    "X-Locale":"BR_PT",
                }

        url_open_game = f'https://decolabet.com/api/gs/getUrl?game={game_id}&locale=BR_PT'
        
        response = requests.get(url_open_game, headers=headers)

        if response.status_code == 200:

            url_game = json.loads(response.content)['data']['link']

            data_success = {'status':'true','url_game':url_game}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success

        else:

            data_failure = {'status':'false','url_game':response.text}
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','url_game':e}

        return data_failure
        
        #### CONTINUA CASO O GAME FOR CASSINO AO VIVO (CONECTANDO NA ATLAS EVO)
        #response = requests.get(url_game, allow_redirects=False)

        #if response.status_code == 302:
            
        #    iframe_location = 'https://atlas.evo-games.com'+response.headers.get('Location')
        #    jsession_id = response.headers.get('Location').split('JSESSIONID=')[1].split('&params=')[0]

        #    print('Success -- ', iframe_location)

        #else:
        #    print('Failure')



    except:pass



### Decorator que retorna a URL do game
@app.route('/open-game-vembetar/' , methods=['POST'])
def open_game_vembetar():

    try:
        # define your proxies in dictionary  
        proxies = {'http': 'http://brd-customer-hl_aed823d1-zone-proxy_2023_daniel-country-br:f3d9e8chmago@brd.superproxy.io:22225',
                    'https': 'http://brd-customer-hl_aed823d1-zone-proxy_2023_daniel-country-br:f3d9e8chmago@brd.superproxy.io:22225'}
        
        ## VARIAVEIS ##
        game_id = json.loads(request.data)['game_id']
        #game_url = json.loads(request.data)['game_url']
        m = json.loads(request.data)['m']
        PHPSESSID = json.loads(request.data)['phpsessid']
        CF_BM = json.loads(request.data)['cf_bm']
        FW_CRM = '13f4dfe3-5381-4ae2-9c45-792eeafc6572'

        #game_id = '41846'
        #game_url = 'fortune-rabbit'
        #m = '242'

        #### GET URL GAME
        URL = f'https://vnsetup-vembetar.belloatech.dev/modules/casino_framework/load_game.php\
?game_eid=i17FfZPBWYTld/2hNnp+gw=\
&game_id={game_id}\
&width=1045.3333333333333\
&height=588\
&m={m}\
&casino_v2=1\
&mode=real'


        header_1 = {
                "Accept-Language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie":f'_fw_crm_v={FW_CRM}; __cf_bm={CF_BM}; PHPSESSID={PHPSESSID}',
                "Referer":f'https://vnsetup-vembetar.belloatech.dev/casino/game/{game_id}',
                "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                }
        
        #REQUISIÇÃO SEM PROXY
        #response = requests.get(URL, headers=header_1, allow_redirects=False)

        #REQUISIÇÃO COM PROXY
        response = requests.get(URL, headers=header_1, proxyes=proxies, allow_redirects=False)


        if response.status_code == 302:
            location_1 = response.headers.get('Location')

        else:
            data_failure = {'status':'false','url_game':response.text}
            return data_failure

        #### SEGUNDA REQUISIÇÃO
        URL = f'https://vnsetup-vembetar.belloatech.dev{location_1}'


        header_2 = {

                "authority":"https://vnsetup-vembetar.belloatech.dev",
                "method":"GET",
                "path":f'{location_1}',
                "scheme":"https",
                "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie":f'_fw_crm_v={FW_CRM}; __cf_bm={CF_BM}; PHPSESSID={PHPSESSID} ',
                "Referer":f'https://vnsetup-vembetar.belloatech.dev/casino/game/{game_id}',
                "Sec-Ch-Ua":'Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115',
                "Sec-Ch-Ua-Mobile":"?0",
                "Sec-Ch-Ua-Platform":"Windows",
                "Sec-Fetch-Dest":"iframe",
                "Sec-Fetch-Mode":"navigate",
                "Sec-Fetch-Site":"same-origin",
                "Sec-Fetch-User":"?1",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        #REQUISIÇÃO SEM PROXY
        #response=requests.get(URL, headers=header_2)

        #REQUISIÇÃO COM PROXY
        response=requests.get(URL, headers=header_2, proxies=proxies)


        if response.status_code == 200:

            url_game = response.text.split(' src="')[1].split('"></iframe>')[0]

            data_success = {'status':'true','url_game':"https:"+url_game}

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), ' - ', data_success)

            return data_success

        
        else:
            data_failure = {'status':'false','url_game':response.text}
            return data_failure


    except Exception as e:
        
        print(e)

        data_failure = {'status':'false','url_game':e}

        return data_failure
   



if __name__ == "__main__":
    print('API Online...')
    #serve(app, port=8000)
    app.run(host='localhost', debug=True)  ### MODO HOMOLOGAÇÃO





#https://bf31-45-178-180-223.ngrok-free.app/URL/s7oryo9stv,game_id,vendor_id,vendor_limit_id

#/login-greenbet
#/login-inbrazza
#/login-vembetar



