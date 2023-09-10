import csv
import requests
url = 'https://jw.qlu.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
#cookie请自行抓取
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': 'JSESSIONID=**********; JSESSIONID=*******; route=*********'
}

#ID以及节次说明
#[3]第一节，[12]第二节，[48]第三节，[192]第四节，[768]晚910节，[15]上午，[240]下午，[1792]整个晚上，[2047]全天
zcd_list = list(range(2, 22))
xgj_list = list(range(1, 8))
jcd_list = [3, 12, 48, 192, 768, 15, 240, 1792, 2047]

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['zcd_xqj_jcd', 'cdmc'])
    for zcd in zcd_list:
        for xqj in xgj_list:
            for jcd in jcd_list:
                data = {
                    'fwzt': 'cx',
                    'xqh_id': '1',
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
                    'zcd': zcd,
                    'xqj': xqj,
                    'jcd': jcd,
                    '_search': 'false',
                    'nd': '1693479485693',
                    'queryModel.showCount': '200',
                    'queryModel.currentPage': '1',
                    'queryModel.sortName': 'cdbh',
                    'queryModel.sortOrder': 'asc',
                    'time': '2'
                }

                response = requests.post(url, data=data, headers=headers)
                response_json = response.json()
                cdmc_values = [item['cdmc'] for item in response_json['items']]
                row = [f'{zcd}_{xqj}_{jcd}', ','.join(cdmc_values)]
                writer.writerow(row)



#INSERT INTO empty_classroom(section ,course) VALUES
#('',''),('','')
# 打开CSV文件，将其转化为SQL语言保存的txt中
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    # 处理每一行数据
    for row in reader:

        # 将数据转换为元组形式
        data_tuple = tuple(row)

        # 保存到txt文件
        with open('output.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(str(data_tuple) + ',')