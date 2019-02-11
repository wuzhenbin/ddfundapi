
from pyquery import PyQuery as pq
from utils import *
from multiprocessing import Pool
import time
import json


def get_history(params):
    code = params['code']
    page = params['page']

    t = time.time()
    nowTime = lambda:int(round(t * 1000))
    params = {
        'callback': 'jQuery183015901735224567126_1549080604934',
        'fundCode': code,
        'pageIndex': str(page),
        'pageSize': '20',
        '_': nowTime()
    }

    headers = {
        'Host': 'api.fund.eastmoney.com',
        'Referer': 'http://fundf10.eastmoney.com/jjjz_006131.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    text = get_response('http://api.fund.eastmoney.com/f10/lsjz',params=params,headers=headers)
    res = text.replace('jQuery183015901735224567126_1549080604934(','')
    tar_str = res[:-1]
    get_json = json.loads(tar_str)
    LSJZList = get_json['Data']['LSJZList']
    return LSJZList

def get_api(code,int_page):
    groups =  [{'page':x,'code':code} for x in range(1,int_page)]
    pool = Pool()
    res = pool.map(get_history,groups)
    time_series = [x for item in res for x in item]
    time_series_lis = sorted(time_series,key=lambda s: s['FSRQ'],reverse=True)

    get_info = read({'fcode':code})
    get_info['time_val_list'] = time_series
    update_to_mongo({'fcode': code},get_info)


def parse_detail(code,html):
    doc = pq(html)
    title = doc.find('title').text()

    desc = doc.find('.bs_gl label').text()
    name = re_func('(.*?)基金',title)[1].replace('('+code+')','')


    # 是否在数据库中
    if read({'fcode':code}):
        print('基本信息已存在数据库')

    else:
        save_to_mongo({'fcode': code, 'desc': desc, 'title': name },'fcode')

    # 总页数
    all_page = doc.find('.pagebtns label').eq(-2).text() 
    int_page = int(all_page) + 1
    get_api(code,int_page)


def main():
    code = '005114'
    res = read({'fcode': code})

    # 是否在数据库中
    if not res:
        splash_url = 'http://localhost:8050/render.html'
        tar_url = 'http://fundf10.eastmoney.com/jjjz_{}.html'.format(code)
        args = { 'url': tar_url, 'wait': '2' }
        html = get_response(splash_url,params=args)
        parse_detail(code,html)
        return
        
    

if __name__ == '__main__':
    main()