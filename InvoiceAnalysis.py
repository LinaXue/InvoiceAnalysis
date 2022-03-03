# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 01:05:58 2022

@author: Lina
"""

import tkinter as tk

import numpy as np

from tkinter import ttk

from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

import requests, re, os, datetime

from concurrent.futures import ThreadPoolExecutor, as_completed

def transferDate(sYear, sMonth, eYear, eMonth):  

    date = []

    if (sYear == eYear) and (sMonth == eMonth):

        date = [[int(sYear), int(sMonth)]]

    elif sYear == eYear:

        for m in range(int(sMonth), int(eMonth) + 1, 2):

            date.append([sYear, m])

    else:  

        for y in range(int(sYear), int(eYear) + 1):

            if y == int(eYear):

                for m in range(1, int(eMonth) + 1, 2):

                    date.append([y, m])

            elif y == int(sYear):

                for m in range(int(sMonth), 12, 2):

                    date.append([y, m])

            else:

                for m in range(1, 12, 2):

                    date.append([y, m])                

    return date

def getInvoiceInfo(year, month):  

    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_' + str(year) + str(month).zfill(2) + '/'

    html = requests.get(url).content.decode('utf-8')

    sp = BeautifulSoup(html, 'html.parser')

    transInfo = []  #[商品1, 商品2, 商品3]

    addrInfo = []

    

    for trans in sp.find_all('td', headers=re.compile('tranItem(\d?)')):

        for tran in re.split('[\*,、，。等共計及和個項組份罐0-9元 ]', trans.text):

            if tran:

                transInfo.append(tran)

                

    for address in sp.find_all('td', headers=re.compile('companyAddress(\d?)')):

        addrInfo.append(address.text[0:2])

            

    return transInfo, addrInfo

def process(startYear, startMonth, endYear, endMonth):

    start = datetime.datetime.now()

    date = transferDate(startYear, startMonth[0], endYear, endMonth[0])

    with ThreadPoolExecutor() as executor:

        result = [executor.submit(getInvoiceInfo, d[0], d[1]) for d in date]

    

    countyInfo = {}

    itemsInfo = {('飲食', '食品', '飲品', '飲料', '餐飲', '麵包', '餐費', '餐飲費', '咖啡', '水果', '冰品', '礦泉水', '零食', '乳品', '餐點', '早餐', '茶葉蛋', '蛋糕', '便當', '泡麵', '蔬菜', '冰塊', '滷味', '飯糰', '鮮乳', '用餐', '飲品券', '晚餐', '咖啡豆', '口香糖', '水', '燴飯', '爆米花', '雞蛋', '熱湯', '豆漿', '湯圓', '火鍋', '鮮奶', '綠茶', '煎餃', '糖果', '玉米湯', '霜淇淋', '茶葉', '吐司', '餅乾', '優酪乳', '午餐', '烘焙材料', '布丁', '優格','水果食品', '薯條雞塊', '飲料零食', '食品飲料'): 0,

                 ('娛樂', '點數卡', '報紙', '門票', '遊戲點數', '遊戲軟體', '觀景臺門票', '遊戲幣', '禮盒', '兌換碼', '線上遊戲', '玩具', '基本台費', '遊戲卡點數', '會員卡費用'): 0,

                 ('交通', '油品', '汽油', '停車費', '柴油', '洗車費', '九五無鉛汽油', '洗車', '停車位租金'): 0,

                 ('菸酒', '酒品', '酒類', '啤酒', '米酒', '菸品'): 0,

                 ('教育', '文具', '文具用品', '影印', '童書', '學費', '測驗費用', '紙張用品', '圖書'): 0,

                 ('生活用品', '生活用品', '用品', '五金', '購物袋', '打火機', '家電', '民生用品', '洗衣精', '輕便雨衣', '衛生用品', '雨衣', '口罩', '開瓶器', '面紙', '電池', '廚具', '網路線', '用品一批', '日用品', '衛生紙', '保溫杯', '家居用品', '日用品百貨', '毛浴巾', '五金材料', '清潔用品', '清潔袋'): 0,

                 ('數位商品', '電腦週邊產品', '電腦週邊設備', '數位商品', '手機', '耳麥', '耳機', 'C週邊商品', 'C用品', '應用程式'): 0,

                 ('醫療用品', '藥品', '保健食品', '健康食品', '營養品', '生理食鹽水', '感冒糖漿', '醫療注射液', '口含錠'): 0,

                 ('運動用品', '運動用品', '運動配件'): 0,

                 ('寵物用品', '飼料', '貓糧'): 0,

                 ('農作用具', '農藥'): 0,

                 ('氣體燃料費', '液化石油氣', '天然氣費', '瓦斯', '瓦斯費', '桶裝瓦斯', '瓦斯桶'): 0,

                 ('衣物與美容', '服飾', '服飾配件', '毛毯', '棉褲', '童裝', '衣物', '女鞋', '美容', '化妝品', '化粧品'): 0,

                 ('電信費與收訊費', '電信', '電信費', '收視費', '電信服務費', '連線費', '訊號費', '電信服務', '市話', '寬頻', '市話寬頻', '市話寬頻業務'): 0,

                 ('其他', '手續費', '運費', '住宿費', '服務費', '電影網路訂票手續費', '佣金', '其他服務費', '交通票券手續費', '代收運費', '代收小額付費', '網際網路收入', '儲值卡', '一卡通', '月租費', '宅急便', '水費', '電費', '房租'): 0}

    

    for future in as_completed(result):

        for idx, info in enumerate(future.result()):

            if (idx % 2 == 0):

                for item in info:

                    for itemsKey in itemsInfo:

                        if item in itemsKey:

                            itemsInfo[itemsKey] += 1

            else:

                for county in info:

                    if county == '台北': county = '臺北'

                    countyInfo[county] = countyInfo.get(county, 0) + 1

    

    printInvoiceInfo(itemsInfo, countyInfo, start, startYear, startMonth, endYear, endMonth)

    

def printInvoiceInfo(itemsInfo, countyInfo, start, startYear, startMonth, endYear, endMonth):

    font = FontProperties(fname=os.environ['WINDIR']+'\\Fonts\\kaiu.ttf', size=16)

    itemName = np.array(['飲食', '娛樂', '交通', '菸酒', '教育', '生活用品', '數位商品', '醫療用品', '運動用品', '寵物用品', '農作用具', '氣體燃料費', '衣物與美容', '電信與收訊費', '其他'])

    itemCount = np.array([count for count in itemsInfo.values()])

    countyName = np.array(list(countyInfo.keys()))

    countyCount = np.array([count for count in countyInfo.values()])

    

    plt.figure(figsize = (10, 5))

    plt.bar(itemName, itemCount)

    plt.xticks(np.arange(len(itemName)), itemName, fontproperties = font, rotation = 50)

    plt.xlabel('商品分類', fontproperties = font)

    plt.ylabel('購買次數', fontproperties = font)

    plt.title(startYear+' 年 '+startMonth[0]+' 月至 '+endYear+' 年 '+endMonth[1]+' 月發票統計圖(依商品)', fontproperties = font)

    

    plt.figure(figsize = (10, 5))

    plt.bar(countyName, countyCount)

    plt.xticks(np.arange(len(countyName)), countyName, fontproperties = font, rotation = 60)

    plt.xlabel('縣市', fontproperties = font)

    plt.ylabel('次數統計', fontproperties = font) 

    plt.title(startYear+' 年 '+startMonth[0]+' 月至 '+endYear+' 年 '+endMonth[1]+' 月發票統計圖(依縣市)', fontproperties = font)

    #plt.savefig('發票統計長條圖.png', dpi = 600)

    plt.show()

    

    print('time: {}'.format(datetime.datetime.now() - start))

def windowtk():

    window = tk.Tk()

    window.title('分析發票')

    window.geometry('450x250') 

   

    start = tk.Label(window, text = '開始年月: ', justify = tk.RIGHT, width = 100)

    start.place(x=10, y=10, width=100, height=20)

    sY = tk.Label(window, text = '年(民國)', justify = tk.RIGHT, width = 50)

    sY.place(x=195, y=10, width=50, height=20)

    sM = tk.Label(window, text = '月', justify = tk.RIGHT, width = 20)

    sM.place(x=350, y=10, width=20, height=20)

    end = tk.Label(window, text = '結束年月: ', justify = tk.RIGHT, width = 100)

    end.place(x=10, y=40, width=100, height=20)

    eY = tk.Label(window, text = '年(民國)', justify = tk.RIGHT, width = 50)

    eY.place(x=195, y=40, width=50, height=20)

    eM = tk.Label(window, text = '月', justify = tk.RIGHT, width = 20)

    eM.place(x=350, y=40, width=20, height=20)

 

    year = ('102', '103', '104', '105', '106', '107', '108')

    month = ('1、2', '3、4', '5、6', '7、8', '9、10', '11、12')

    startYear = ttk.Combobox(window, width = 120, values = year)

    startYear.place(x=110, y=10, width=80, height=20)

    startMon = ttk.Combobox(width = 100, values = month)

    startMon.place(x=260, y=10, width=80, height=20)

    endYear = ttk.Combobox(window, width=80, values = year)

    endYear.place(x=110, y=40, width=80, height=20)

    endMon = ttk.Combobox(window, width = 100, values = month)

    endMon.place(x=260, y=40, width=80, height=20)

    

    startAna = tk.Button(window, text='開始分析', width=50, command = lambda: process(startYear.get(), startMon.get().split('、'), endYear.get(), endMon.get().split('、'))) #endYear.get(), endMon.get()

    startAna.place(x=160, y=130, width=100, height=20)

    endAna = tk.Button(window, text='結束', width=50, command = window.quit)

    endAna.place(x=160, y=160, width=100, height=20)    

    

    window.mainloop()

windowtk()