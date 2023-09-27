import time
import math
import requests
url = 'https://jw.qlu.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'

#cookie请自行抓取
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': "JSESSIONID=**************; route=*********6"
}

#ID以及节次说明
#xqh_id    [1]长清（空默认）  [3]历城  [4]菏泽  [zc]彩石前端彩石代码设置为2
#[3]第一节，[12]第二节，[48]第三节，[192]第四节，[768]晚910节，[15]上午，[240]下午，[1792]整个晚上，[2047]全天

zcd_list = [2**(i-1) for i in range(5, 6)]
xgj_list = list(range(3, 5))
jcd_list = [3, 12, 48, 192, 768, 15, 240, 1792, 2047]
xqh_list = [1,3,4,'zc']
for xqh in xqh_list:
    for zcd in zcd_list:
        for xqj in xgj_list:
             for jcd in jcd_list:
                timestamp = int(time.time() * 1000)
                data = {
                        'fwzt': 'cx',
                        'xqh_id': xqh,
                        'xnm': '2023',
                        'xqm': '3',
                        'cdlb_id': '05',
                        'cdejlb_id': '',
                        'qszws': '',
                        'jszws': '',
                        'cdmc': '',
                        'lh': '',
                        'jyfs': '0',
                        'cdjylx': '',
                        'sfbhkc': '',
                        'zcd': zcd,
                        'xqj': xqj,
                        'jcd': jcd,
                        '_search': 'false',
                        'nd': timestamp,
                        'queryModel.showCount': '200',
                        'queryModel.currentPage': '1',
                        'queryModel.sortName': 'cdbh',
                        'queryModel.sortOrder': 'asc',
                        'time': '1'
                    }
                response = requests.post(url, data=data, headers=headers)
                response_json = response.json()
                cdmc_values = [item['cdmc'] for item in response_json['items']]
                row = [f'{xqh}_{int(math.log(zcd, 2)) + 1}_{xqj}_{jcd}', ','.join(cdmc_values)]
                data = {
                        'name': row[0],
                        'room': row[1]
                }
                
                print(data)
