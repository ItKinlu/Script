#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 用来苹果证书配置自动化操作 '

__author__ = 'SP'

csrPath      = "/Users/sanpao/Desktop/CertificateSigningRequest.certSigningRequest"
downLoadPath = "/Users/sanpao/Downloads"
udidAllPath  = "/Users/sanpao/Desktop/udidAll.deviceids"

import time
import datetime
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select


# browser.close()
# print(browser.page_source)


# 查找TeamName和ID
def checkTeamNameID(browser):
    browser.find_element_by_link_text("Membership").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//section[@class='column large-9 small-12']")))
    section = browser.find_elements_by_xpath("//section[@class='column large-9 small-12']")
    teamNameS = section[1]
    teamNameP = teamNameS.find_element_by_xpath("p")
    print("TeamName:" + teamNameP.text)
    teamIDS = section[2]
    teamIDP = teamIDS.find_element_by_xpath("p")
    print("TeamID:" + teamIDP.text)
    return teamNameP.text,teamIDP.text

# 生成生产证书
def generateProductionCer(browser):
    browser.get("https://developer.apple.com/account/resources/certificates/add")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//ul[@class='form-radio-list']")))
    ul = browser.find_element_by_xpath("//ul[@class='form-radio-list']")
    li = ul.find_elements_by_xpath('li')[1]
    li.find_element_by_xpath("span/input").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='form-file-container']")))
    divFile = browser.find_element_by_xpath("//div[@class='form-file-container']")
    uploadFile = divFile.find_element_by_xpath("//input[@type = 'file']")
    uploadFile.send_keys(csrPath)
    save = browser.find_element_by_id("action-save").click()
    dows = browser.find_element_by_class_name("actions-container")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='tb-btn--primary']")))
    browser.find_element_by_link_text("Download").click()

# 创建BundleID
def generateBundleID(browser,bundleID = ""):
    # 1.建bundleid
    browser.get("https://developer.apple.com/account/resources/identifiers/add/bundleId")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    continueBtn = browser.find_element_by_xpath("//button[@id='action-continue']")
    continueBtn.click()
    if bundleID == "":
        bundleID = input("请输入Bundle ID:")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='description']")))
    descriptionInput = browser.find_element_by_xpath("//input[@id='description']")
    current = datetime.datetime.now()
    descriptionInput.send_keys(current.strftime('%Y%m%d'))
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='identifier']")))
    identifierInput = browser.find_element_by_xpath("//input[@id='identifier']")
    identifierInput.send_keys(bundleID)
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='PUSH_NOTIFICATIONS']")))
    pushBtn = browser.find_element_by_xpath("//input[@id='PUSH_NOTIFICATIONS']")
    pushBtn.click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@class='tb-btn--primary action-save']")))
    continueBtn2 = browser.find_element_by_xpath("//button[@class='tb-btn--primary action-save']")
    continueBtn2.click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@class='tb-btn--primary action-save']")))
    continueBtn3 = browser.find_element_by_xpath("//button[@class='tb-btn--primary action-save']")
    continueBtn3.click()
    # 2.建推送证书
    generatePushCer(browser)
# 创建推送证书
def generatePushCer(browser):
    browser.get("https://developer.apple.com/account/resources/certificates/add")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//ul[@class='form-radio-list']")))
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//ul[@class='form-radio-list']")))
    ul = browser.find_elements_by_xpath("//ul[@class='form-radio-list']")[1]
    li = ul.find_elements_by_xpath('li')[2]
    li.find_element_by_xpath("span/input").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//select[@id='certificate-identifier']")))
    s1 = Select(browser.find_element_by_xpath("//select[@id='certificate-identifier']"))
    s1.select_by_index(1)
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='form-file-container']")))
    divFile = browser.find_element_by_xpath("//div[@class='form-file-container']")
    uploadFile = divFile.find_element_by_xpath("//input[@type = 'file']")
    uploadFile.send_keys(csrPath)
    save = browser.find_element_by_id("action-save").click()
    dows = browser.find_element_by_class_name("actions-container")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='tb-btn--primary']")))
    browser.find_element_by_link_text("Download").click()

# 添加设备号
def addDeviceId(browser):
    browser.get("https://developer.apple.com/account/resources/devices/add")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='form-file-container']")))
    divFile = browser.find_element_by_xpath("//div[@class='form-file-container']")
    uploadFile = divFile.find_element_by_xpath("//input[@type = 'file']")
    uploadFile.send_keys(udidAllPath)
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-register']")))
    browser.find_element_by_xpath("//button[@id='action-register']").click()

# 创建描述文件
def generateProfile(browser):
    browser.get("https://developer.apple.com/account/resources/profiles/add")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='type-adhoc']")))
    browser.find_element_by_xpath("//input[@id='type-adhoc']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//select[@id='appIdId']")))
    s1 = Select(browser.find_element_by_xpath("//select[@id='appIdId']"))
    s1.select_by_index(1)
    # print("*" * 30 + "下列是bundleid选项" + "*" * 30)
    # for i in range(1,len(s1.options)):
    #     option = s1.options[i]
    #     print("%d . %s" % (i,option.text))
    # while True:
    #     selectOption = input("请输入选项==>")
    #     try:
    #         s1.select_by_index(int(selectOption))
    #         break
    #     except Exception as e:
    #         print("老哥别乱输入啊，看清楚了")
    # print("111")
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//ul[@class='select-table single']")))
    ul = browser.find_element_by_xpath("//ul[@class='select-table single']")
    li = ul.find_elements_by_xpath('li')[-1]
    li.find_element_by_xpath("span/input").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='selectAllDId']")))
    browser.find_element_by_xpath("//input[@id='selectAllDId']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@class='form-text text-input']")))
    browser.find_element_by_xpath( "//input[@class='form-text text-input']").send_keys(str(int(time.time())))
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@id='action-continue']")))
    browser.find_element_by_xpath("//button[@id='action-continue']").click()
    WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='tb-btn--primary']")))
    browser.find_element_by_link_text("Download").click()



def tools(browser):
    while True:
        waitCode = input("请选择 0.退出 1.Team Name & ID 2.创建生产证书 3.创建Bundle ID 4.添加设备 5.创建描述文件 (输入其他全自动，必须新账号)==>")
        if waitCode == "0":
            exit()
        elif waitCode == "1":
            print("Team Name & ID")
        elif waitCode == "2":
            print("创建生产证书")
            generateProductionCer(browser)
        elif waitCode == "3":
            print("创建Bundle ID")
            generateBundleID(browser)
        elif waitCode == "4":
            print("添加设备")
            addDeviceId(browser)
        elif waitCode == "5":
            print("创建描述文件")
            generateProfile(browser)
        else:
            bundleID = input("请输入Bundle ID:")
            teamName,teamID = checkTeamNameID(browser)
            print("创建生产证书")
            generateProductionCer(browser)
            print("创建Bundle ID")
            generateBundleID(browser,bundleID)
            print("添加设备")
            addDeviceId(browser)
            print("创建描述文件")
            generateProfile(browser)
        os.system("open " + downLoadPath)

while True:
    account = input("请输入账号==>")
    pwd = input("请输入密码==>")
    if account != "" and pwd != "":
        browser = webdriver.Chrome()
        browser.get("https://developer.apple.com")
        browser.find_element_by_link_text("Account").click()

        WebDriverWait(browser, 30).until(expected_conditions.frame_to_be_available_and_switch_to_it((By.ID, "aid-auth-widget-iFrame")))
        WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='account_name_text_field']")))

        account_input = browser.find_element_by_xpath("//input[@id='account_name_text_field']")
        account_input.send_keys(account)
        browser.find_element_by_id("sign-in").click()

        WebDriverWait(browser, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@id='password_text_field']")))
        pwd_input = browser.find_element_by_xpath("//input[@id='password_text_field']")
        pwd_input.send_keys(pwd)
        pwd_input.send_keys(Keys.ENTER)
        tools(browser)
print("结束")