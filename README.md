# 爬取猫眼榜单

- 网址：https://maoyan.com/board
- 爬取的信息：电影名称、主演、上映时间

- 思路：
  - 一共十部电影，查询源代码发现爬取的信息都在\<dd>\</dd>标签中
  - 根据源代码构造正则表达式
- ![源码](https://github.com/LeslieOOZ/maoyan/blob/master/ph.png)
