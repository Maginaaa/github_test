#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : login.py
# @Author: Lyn
# @Date  : 2018/10/6
# @Desc  :
from selenium import webdriver
import scrapy
import requests

# 使用selenium完成登录
def login_get_cookies_selenium(url):
    driver = webdriver.Chrome(executable_path='../chromedriver')
    driver.get(url)
    driver.find_element_by_css_selector(
        'body > div.position-relative.js-header-wrapper > header > div > div.HeaderMenu.d-lg-flex.flex-justify-between.flex-auto > div > span > div > a:nth-child(1)').click()
    driver.implicitly_wait(5)
    driver.find_element_by_id('login_field').send_keys('your_email')
    driver.find_element_by_id('password').send_keys('your_password')
    driver.find_element_by_css_selector('#login > form > div.auth-form-body.mt-3 > input.btn.btn-primary.btn-block').click()

    return driver.get_cookies()

# 使用requests完成登录
def login_get_cookies_requests():
    response = scrapy.Request(url="https://github.com")
    authenticity_token = response.css('input::attr(value)').extract()[1]
    res1 = requests.get('https://github.com/login')
    res2 = requests.post(
        'https://github.com/session',
        data={
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': authenticity_token,
            'login': 'your_email',
            'password': 'your_password'
        },
        cookies=res1.cookies.get_dict(),
    )

    return res2.cookies.get_dict()
