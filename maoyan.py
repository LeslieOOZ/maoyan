import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
url = 'https://maoyan.com/board'
rsp = requests.get(url,headers=headers)
#print(rsp.text)

#电影名称
films = re.findall('<dd>.*?title="(.*?)".*?</dd>',rsp.text,re.S)
#主演
starrings = re.findall('<p class="star">.*?：(.*?)</p>',rsp.text,re.S)
#上映时间
times = re.findall('<p class="releasetime">.*?(\d+-\d+-\d+)</p>',rsp.text,re.S)


#遍历爬取到的信息并存储在data
for film,starring,time in zip(films,starrings,times):
    data = {
        '电影名称':film,
        '主演': starring.strip(),
        '上映时间':time,


    }
    print(data)

