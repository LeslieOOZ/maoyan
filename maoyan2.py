'''
爬取猫眼TOP100：https://maoyan.com/board/4

爬取100部电影信息，每页10部，有10页
爬取的数据：排名、封面图片、电影名、主演、上映时间、评分

第一页：https://maoyan.com/board/4?offset=0
第二页：https://maoyan.com/board/4?offset=10
第三页：https://maoyan.com/board/4?offset=20

思路：
使用正则来抓取
'''
from multiprocessing import Pool
import requests
import re
from requests.exceptions import RequestException
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

#获取源码(html)
def get_page(url):
    try:
        rsp = requests.get(url,headers=headers)
        if rsp.status_code == 200:
            return rsp.text
        return None

    except RequestException:
        return None

#提取信息，最后封装为迭代形式（items），里面是字典形式
def shuju(html):
    pattern = re.compile('<dd>.*?<i.*?board-index.*?>(\d+)</i>'
                         +'.*?data-src="(.*?)"'
                         +'.*?<a.*?title.*?>(.*?)</a>'
                         +'.*?<p.*?>(.*?)</p>'
                         +'.*?<p.*?>(.*?)</p>'
                         +'.*?<p.*?>.*?<i.*?>(.*?)</i>.*?<i.*?>(.*?)</i>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'img':item[1],
            'name':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4][5:],
            'score':item[5]+item[6],
        }

#保存为文件
def write_file(i):
    with open('maoyan.txt','a',encoding='utf-8') as f:
        #写入文件要转化为str类型，False是保证不乱码
        f.write(json.dumps(i,ensure_ascii=False)+'\n')
        f.close()

#主函数
def main(url):
    html = get_page(url)
    #shuju()函数最终的结果是可迭代的，里面是字典形式
    for i in shuju(html):
        print(i)
        #把拿到的字典数据保存为文件
        write_file(i)

if __name__ == '__main__':
    urls = ['https://maoyan.com/board/4?offset={}'.format(num) for num in range(0,100,10)]
    #使用进程池来爬取，速度更快
    pool = Pool()
    pool.map(main,[url for url in urls])
