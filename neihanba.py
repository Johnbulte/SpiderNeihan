# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 18:54:46 2018

@author: tarena
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:11:49 2018

@author: tarena
"""

import requests
from lxml import etree

class BaiduImageSpider:
    def __init__(self):
        self.baseurl = "https://www.neihan8.com"
        self.headers = {'User-Agent': 'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;'}
        self.proxies={"HTTP":"110.73.7.64:8123"}
        self.basepage = "http://tieba.baidu.com/index_"
    
    
    #获取每个帖子的url,html
    def getPageUrl(self,url):
        #得到贴吧第1页的html源码
        print(url)
        res = requests.get(url,headers=self.headers,proxies=self.proxies)
        res.encoding = "utf-8"
        html = res.text
        parseHtml = etree.HTML(html)
        t_list = parseHtml.xpath('//div[@class="pic-column-list mt10"]/div/h3/a/@href')
        for t in t_list:
            t_url = self.baseurl + t
            print(t_url)
            self.getImageUrl(t_url)
    
    #获取帖子中所有图片的URL
    def getImageUrl(self,t_url):
        #获取帖子的HTML源码，为了从中获取图片的url
        res = requests.get(t_url,headers=self.headers,proxies=self.proxies)
        res.encoding = "utf-8"
        html = res.text
        #得到图片的url
        parseHtml = etree.HTML(html)
        i_list = parseHtml.xpath('//div[@class="detail"]/p/a/img/@src')
        print(i_list)
        for i in i_list:
            print(i)
            self.writeImage(i)
        
    
    #保存到本地
    def writeImage(self,i):
        #获取图片的html源码  bytes
        res = requests.get(i,headers=self.headers,proxies=self.proxies)
        res.encoding = "utf-8"
        html = res.content
        #保存到本地
        filename = i[-10:]
        with open(filename,"wb") as f:
            print('%s正在下载'%filename)
            f.write(html)
            print('%s下载成功'%filename)
        
       
    #主函数
    def workOn(self):
        start = int(input('请输入起始页：'))
        end = int(input('请输入结尾页：'))      
        for page in range(start,end+1):
            print('正在下载第%d页' % page)
            if page == 1:
                self.getPageUrl(self.baseurl+"/gif")
            else:
                url = self.basepage +str(page) + ".html"
                self.getPageUrl(url)
            print("第%d页下载成功"%page)
    
    
if __name__ == "__main__":
    spider = BaiduImageSpider()
    spider.workOn()
    
    
    