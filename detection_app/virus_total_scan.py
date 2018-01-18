import requests


# from os import path
# from pfe_plateforme_web.settings import MEDIA_DIR

VT_API_KEY = '7b018153a61799558dda765c03e8f990b7600ba447d203546de98fadfca0302b'
def virus_total_scan(file_name,file_path)->dict:
    #Request scan
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': VT_API_KEY }
    files = {'file': (file_name, open(file_path, 'rb'))}
    response = requests.post(url, files=files, params=params)
    virus_total_response= response.json()
    if virus_total_response['response_code'] == 1:
        #get report
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': VT_API_KEY , 'resource': virus_total_response['resource'] }
        anti_virus_scan = requests.get(url, params=params)
        virus_total_report = anti_virus_scan.json()
        return virus_total_report
    else:
        return {}


# print(virus_total_scan('app-release.apk',path.join(MEDIA_DIR,'app-release.apk')))
