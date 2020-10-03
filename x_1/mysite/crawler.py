from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


opt = Options()                   
opt.add_argument('--headless')   
chrome_driver_path = "/Users/weichenho/Desktop/chromedriver"      # chromedriver位置（請下載與瀏覽器對應版本）
driver = webdriver.Chrome(executable_path = chrome_driver_path ,chrome_options=opt )  #無視窗 / 開視窗與下方更換 '#'
# driver = webdriver.Chrome(chrome_driver_path)                             

key = ['折扣', '優惠', '下殺', '促銷', '特價']     #搜尋關鍵字，可自行新增

#---------首頁與輸入關鍵字----------------

target = []   #輸入的關鍵字
class_ = []   #商品種類
title = []    #商品名稱
price = []    #商品價格
discount = [] #折扣商品

for k in tqdm(key):

    driver.get(f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={k}&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType')
    time.sleep(3)

#-------輸入關鍵字後，取所有總類-----------

    html = driver.page_source           
    soup = bs(html,'lxml') 
    data = soup.select('#BodyBase > div.bt_2_layout.searchbox.searchListArea > div.attributesListArea > table.wrapTable > tbody > tr.cateTooth > td > div > ul')

    all_kind = []   #所有總類
    cate = []
    kind = data[0].find_all('li')

    for i in kind:
        x = i.find('a').get('title')
        if '(' in x:
            all_kind.append(x.split('(')[0])
        else:
            all_kind.append(x)
        cate.append(i.find('a').get('cate'))

#-------------個別種類---------------

    count = 0
    for i in cate:
        driver.get(f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={k}&searchType=1&cateLevel=0&cateCode={i}&curPage=1&_isFuzzy=0&showType=chessboardType')
        time.sleep(5)
        name = all_kind[count]
        count += 1

        html = driver.page_source           
        soup = bs(html,'lxml') 
        #取個別種類頁數
        page = soup.select('#BodyBase > div.bt_2_layout.searchbox.searchListArea.selectedtop > div.pageArea.topPage > dl > dt > span:nth-child(2)')
        pg = int(page[0].text[4:]) 

#---------個別總類爬取 / 處理----------
        for j in range(pg):
            try:            
                time.sleep(3)
                html = driver.page_source           
                soup = bs(html,'lxml') 
                t = soup.select('li > a > div > h3')
                p = soup.select('li > a > div.prdInfoWrap > p.money')
                for i in t:
                    title.append(i.text)
                for i in p:
                    x = i.text.replace('$','')
                    if '售完補貨中' in x:
                        x = x.replace('售完補貨中', '')
                    if '(' in x:
                        r = x.split('(')                         
                        discount.append(r[1].replace(')','')) 
                        if ',' in r[0]:
                            price.append(r[0].replace(',', ''))
                        else:
                            price.append(r[0])
                    else:
                        discount.append('')
                        if ',' in x:
                            price.append(x.replace(',', ''))
                        else:
                            price.append(x)
                    class_.append(name)
                    target.append(k)
                try:
                    driver.find_element_by_xpath('//div[@class="pageArea topPage"]/dl/dd[2]/a').click()  
                except:
                    driver.find_element_by_xpath('//div[@class="pageArea topPage"]/dl/dd/a').click()
            except:
                pass

#-------------DataFrame to CSV------------------
data ={
    'Target':target,
    'Class':class_,
    'Title':title,
    'Price':price,
    'Discount':discount
}

df = pd.DataFrame(data)
df.to_csv('momo.csv',index=True, index_label= 'id')

#----------------------------------------------------Bank----------------------------------------

driver.get('https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O0Y2mh4ttZH&n=1&mdiv=1099900000-bt_0_249_01-bt_0_249_01_e1&ctype=B')
time.sleep(3)
html = driver.page_source           
soup = bs(html,'lxml') 


data = soup.select('#Area_bankList > ul > li')

#銀行優惠總覽
bank = []
for i in data:
    dic = {}
    l = ''
    dic['Name'] = i.get('data-name')
    info = i.find_all('p')
    for y in info:
        l = l + ' ' + y.text
    dic['info'] = l
    bank.append(dic)

#行動支付優惠    
driver.find_element_by_xpath('//*[@id="Area_swiperpage_nav"]/ul/li[5]/a').click()
time.sleep(3)
html = driver.page_source           
soup = bs(html,'lxml') 

data1 = soup.select('#Area_swiperpage > div > div.box_page.swiper-wrapper > div.box_slidepage.swiper-slide.swiper-no-swiping.cate-show.swiper-slide-active > div > div > div > div > dl > dd > div > ul > li')

for i in data1:
    dic1 = {}
    l1  = []
    l1 = ''
    dic1['Name'] = i.get('data-name')
    info1 = i.find_all('p')
    for y in info1:
        l1 = l1 + ' ' + y.text
    dic1['info'] = l1
    bank.append(dic1)
    
df = pd.DataFrame(bank)
df.to_csv('momo_bank_dis.csv',index=True, index_label= 'id')


#-------------------------------------------今日最大牌--------------------------------------

driver.get('https://www.momoshop.com.tw/main/Main.jsp?cid=memb&oid=back2hp&mdiv=1099800000-bt_0_150_01-bt_0_150_01_e1&ctype=B')
time.sleep(3)
html = driver.page_source           
soup = bs(html,'lxml') 

f = soup.select('#bt_0_248_01_P1')
name = []
href = []
for i in f[0].find_all('li'):
    name.append(i.find('a').get('title'))
    href.append(i.find('a').get('href'))
data = {
    'Name':name,
    'Href':href
}
df = pd.DataFrame(data)
df.to_csv('special_product.csv',index=True, index_label= 'id')


#--------------------------------------限時搶購-------------------------------------------

driver.get('https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O1K5FBOqsvN&n=1#posTag1')
time.sleep(3)
html = driver.page_source           
soup = bs(html,'lxml') 

product = soup.select('#gdsBrand_1')
info = soup.select('#gdsName_1')
discount = soup.select('#discAmt_1')
price = soup.select('#nPrice_1')

data = zip(product, info, discount, price)

name1 = []
info1 = []
discount1 =[]
price1 = []

for pro, inf ,di , pr in data:
    name1.append(pro.text)
    info1.append(inf.text)
    discount1.append(di.text + '折')
    price1.append(pr.text + '元')
data = {
    'Name':name1,
    'Info':info1,
    'Discount':discount1,
    'Price':price1
}


df = pd.DataFrame(data)
df.to_csv('limited_time.csv',index=True, index_label= 'id')




            
driver.close()