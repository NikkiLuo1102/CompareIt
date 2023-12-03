'''
Author: shihan
Date: 2023-12-02 12:21:59
version: 1.0
description: 
'''
import requests
from openpyxl import Workbook

headers = {
    'Referer': 'https://category.vip.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank'
data = {
    'app_name': 'shop_pc',
    'app_version': '4.0',
    'warehouse': 'VIP_HZ',
    'fdc_area_id': '104103101',
    'client': 'pc',
    'mobile_platform': '1',
    'province_id': '104103',
    'api_key': '70f71280d5d547b2a7bb370a529aeea1',
    'user_id': '',
    'mars_cid': '1689245318776_e2b4a7b51f99b3dd6a4e6d356e364148',
    'wap_consumer': 'a',
    'standby_id': 'nature',
    'keyword': '耐克运动鞋',
    'lv3CatIds': '',
    'lv2CatIds': '',
    'lv1CatIds': '',
    'brandStoreSns': '',
    'props': '',
    'priceMin': '',
    'priceMax': '',
    'vipService': '',
    'sort': '0',
    'pageOffset': '0',
    'channelId': '1',
    'gPlatform': 'PC',
    'batchSize': '120',
    '_': '1689250387620',
}

response = requests.get(url=url, params=data, headers=headers)
products = [i['pid'] for i in response.json()['data']['products']]

# 打开文件并创建 CSV 写入器
# 创建一个工作簿和工作表
workbook = Workbook()
sheet = workbook.active

# 设置表头
header = [
    '标题', '品牌', '售价', '图片', '商品信息', '详情页'
]
sheet.append(header)

min_price_row=[]
for i in range(0, len(products), 50):
    product_id = ','.join(products[i:i+50])
    link = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'
    params = {
        # 'callback': 'getMerchandiseDroplets2',
        'app_name': 'shop_pc',
        'app_version': '4.0',
        'warehouse': 'VIP_HZ',
        'fdc_area_id': '104103101',
        'client': 'pc',
        'mobile_platform': '1',
        'province_id': '104103',
        'api_key': '70f71280d5d547b2a7bb370a529aeea1',
        'user_id': '',
        'mars_cid': '1689245318776_e2b4a7b51f99b3dd6a4e6d356e364148',
        'wap_consumer': 'a',
        'productIds': product_id,
        'scene': 'search',
        'standby_id': 'nature',
        'extParams': '{"stdSizeVids":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x","ic2label":1,"superHot":1,"bigBrand":"1"}',
        'context': '',
        '_': '1689250387628',
    }
    json_data = requests.get(url=link, params=params, headers=headers).json()

    for index in json_data['data']['products']:
        attr = ','.join([j['value'] for j in index['attrs']])
        row = [
            index['title'],
            index['brandShowName'],
            index['price']['salePrice'],
            index['squareImage'],
            attr,
            f'https://detail.vip.com/detail-{index["brandId"]}-{index["productId"]}.html',
        ]
        if len(min_price_row)==0 or float(row[2])<float(min_price_row[2]):
            min_price_row=row
        sheet.append(row)
        
# 保存数据到Excel文件
workbook.save('商品.xlsx')
print(min_price_row[0])

'''
                    <th>title</th>
                    <th>link</th>
                    <th>price</th>
                    <th>manufacturer</th>
                    <th>other</th>'''
'''
['COURT LEGACY 轻便休闲 小白鞋 男子板鞋',
 'Nike', 
 '198',
   'http://h2.appsimg.com/a.appsimg.com/upload/merchandise/pdcvis/611861/2023/0612/178/4b8049eb-ea43-4631-8e1d-e83f44c4b5f1.jpg', 
   '板鞋/小白鞋,平底,无,适中', 
   'https://detail.vip.com/detail-1710618487-6920028890971952983.html']'''