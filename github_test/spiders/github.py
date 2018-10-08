# -*- coding: utf-8 -*-
import scrapy
import re
from github_test.utils.login import login_get_cookies_selenium,login_get_cookies_requests
import math
from scrapy.loader import ItemLoader
from github_test.items import EmailItem



class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    # start_urls = []
    start_urls = ['https://github.com/trending?since=daily']

    cookies = {}

    def parse(self, response):

        # 使用requests完成登录
        # self.cookies = login_get_cookies_requests()

        # 使用selenuim完成登录
        self.cookies = login_get_cookies_selenium(response.url)

        # 获取项目列表
        repo_list = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/ol').extract()[0]

        # 获取每个项目收藏者列表的url
        mem_list_url = re.findall('\/.{1,20}\/.{1,20}\/stargazers', repo_list)

        for path in mem_list_url:
            yield scrapy.Request(url="https://github.com" + path, callback=self.member_list, cookies=self.cookies)

    # 获取每个项目的收藏人列表
    def member_list(self, response):

        # 获取收藏用户数
        count = response.xpath('//*[@id="repos"]/div[1]/nav/a[1]/span/text()').extract()[0]

        # 计算收藏用户页数
        page_size = 51
        pages = min(math.ceil(int(count.replace(',', '')) / page_size), 100)
        for page_number in range(1, pages):
            yield scrapy.Request(url=response.url + '?page=' + str(page_number), callback=self.user_detail, cookies=self.cookies)

    # 获取用户详情
    def user_detail(self, response):
        user_list_css = response.xpath('//*[@id="repos"]/ol').extract()[0]
        user_list = re.findall('<a href="(.{0,20})">', user_list_css)
        for user in user_list:
            yield scrapy.Request(url='https://github.com' + user, callback=self.get_email, cookies=self.cookies)

    # 获取用户邮箱
    def get_email(self, response):
        loader = ItemLoader(item=EmailItem(), response=response)
        # 获取用户邮箱
        if len(response.css('.vcard-details li')) == 4:
            email = response.xpath('//*[@id="js-pjax-container"]/div/div[1]/ul/li[3]/a/text()').extract()[0]
            loader.add_value('email', email)
            yield loader.load_item()
        elif len(response.css('.vcard-details li')) == 3:
            email = response.xpath('//*[@id="js-pjax-container"]/div/div[1]/ul/li[2]/a/text()').extract()[0]
            loader.add_value('email', email)
            yield loader.load_item()
        else:
            print("用户未公开邮箱")
