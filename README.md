# MM131-test
2020年6月份的爬虫基础练习
test0.3 能实现单模块的全图集爬取-待解决的问题（爬取到一定数量的图集时，会报错AttributeError: 'NoneType' object has no attribute 'group'）
初步怀疑：是页面的格式有所改变，导致正则表达式无法正确提取信息
方案：1.发现异常后抛出页面的html代码，然后分析具体原因
     2. 改用BeautifulSoup来解析页面，而不是用正则表达式
     
