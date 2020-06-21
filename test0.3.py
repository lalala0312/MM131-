"""
0.3版本   稳定版
当前版本可获取单模块多图集多页的照片（经测试可稳定获取1500张图集吧）
这个时期的url是模块的url
"""
import requests
import random
import time
import re
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
请求头
Referer：防盗链，不加上的话从外部跳转会转向一个错误的网址
后续功能 UA池，ip代理池，多进程爬取
"""

class MmSpider:
    def __init__(self):
        self.url = 'https://www.mm131.net/xinggan/'   # 模块的网址
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.61 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.mm131.net'}


    def get_html(self, url):    # html  由parse_page传递过来的信息
        """
        请求网址并返回html信息
        :return:  html
        """
        i = 0
        while i < 3:
            try:
                r = requests.get(url, headers=self.headers, timeout=(5, 10), verify=False)
                if (r.status_code == 200):
                    r.encoding = 'GBK'
                    html = r.text
                    return html
                else:
                    return None
            except requests.exceptions.RequestException:
                i += 1
        return None


    def parse_page(self, info):   # info 获得来自模块的名称，图集html
        """
        提取出照片的url
        提取出照片的标题
        提取出模块标题
        提取出图集的照片数量
        处理单页
        :return: 字典内包含所需的信息
        """
        pic_info = info  # 用字典的键值对去存储相应的数据
        html = self.get_html(url=info['atlas_url'])
        if html is not None:
            img_url = re.search('\)" src="(.*?)"', html)   # 提取出需要的图片url,re.search会返回一个Match
            pic_title = re.search('<h5>(.*?)</h5>', html)  # 提取出单页的照片标题
            atlas_amount = re.search('page-ch.*?([0-9]{1,2})', html)  #提取该页所属图集的照片数量
            try:
                pic_info['img_url'] = img_url.group(1)
                pic_info['pic_title'] = pic_title.group(1)
                pic_info['atlas_amount'] = atlas_amount.group(1)
                pic_info['modle_name'] = info['module_name']
            except AttributeError:
                print(html)
            return pic_info
        else:
            return None

    def get_one_module(self):
        """
        获取某模块的所有的图集网页和title
        :param url:
        :return:
        """
        html = self.get_html(self.url)

        module_info = {}  # 用字典保存该模块的相关信息
        module_amount = re.search('<dd.*?/(\d{4})', html)                           # 提取该模块的图集数量
        module_name = re.search('class="public-title.*?</a>.*?\'>(.*?)</a>', html)  # 提取该模块的名称
        module_info['module_amount'] = module_amount.group(1)
        module_info['module_name'] = module_name.group(1)

        for i in range(5513, int(module_info['module_amount'])+1):                     # 循环从1开始遍历到最大图集数
            module_info['atlas_url'] = self.url + str(i) + '.html'                  # 拼接出图集的html，上回中断到2926了
            self.get_one_atlas(info=module_info)
            time.sleep(random.random()*0.05)

    def get_one_atlas(self, info):
        """
        获取单图集的全部照片
        :return:
        """
        pic_info = self.parse_page(info=info)   # 传递模块名称，图集html给parse_page()
        if pic_info is not None:
            self.download_img(pic_info=pic_info)
        else:
            None


    def download_img(self, pic_info):
        """
        下载图片
        :param pic_info:
        :return:
        """
        for i in range(1, int(pic_info['atlas_amount'])+1):
            base_url = pic_info['img_url'][:-5] + str(i) + '.jpg'           # 照片地址
            resp = requests.get(base_url, headers=self.headers, verify=False)             # 请求照片获得的响应
            title = pic_info['module_name'] + '/' + pic_info['pic_title']   # 照片的标题
            title = title.replace(":", " ")
            file_path = 'D:/MM131/' + title + '/'                           # 存放图片的路径
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            try:
                with open(file_path + '/' + str(i) + '.jpg', 'wb')as jpg:
                    jpg.write(resp.content)
                    print("冲冲冲" + str(i))
            except BaseException:
                print("出错了，hxd！")



if __name__ == '__main__':
    spider = MmSpider()
    spider.get_one_module()


