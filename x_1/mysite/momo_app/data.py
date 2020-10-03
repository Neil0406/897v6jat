import pandas as pd

def momo():
    # 各分類商品數量總數 / 關鍵字搜尋數量
    momo = pd.read_csv('momo.csv').to_dict('recode')
    class_ = []
    target = []
    count = 0
    for i in momo:
        count += 1
        if i['Class'] not in class_:
            class_.append(i['Class'])
        if i['Target'] not in target:
            target.append(i['Target'])
            
    all_val = count  # 總數
            
    val = []          #target 數量
    for i in class_:
        count = 0
        dic = {}
        for j in momo:
            if j['Class'] == i:
                count += 1
        dic['class'] = i 
        dic['product_num'] = count
        val.append(dic)

            
    val2 = []        #class 數量   
    for i in target:
        count = 0
        dic1 = {}
        for j in momo:
            if j['Target'] == i:
                count += 1
        dic1['target'] = i
        dic1['target_num'] = count
        val2.append(dic1)
    return all_val, val, val2
    
#銀行處理
def bank():
    bank = pd.read_csv('momo_bank_dis.csv').to_dict('recode')
    bank_val = []
    for i in bank:
        dic = {}
        b = []
        b2 = []
        x = i['info'].split('  ')
        for j in x:
            if j != '':
                b.append(j)
        for k in b:
            b2.append(k.replace(' ',''))
        dic['name'] = i['Name']
        dic['info'] = b2
        bank_val.append(dic)
    return bank_val

#今日最大牌
def special():
    special_val = pd.read_csv('special_product.csv').to_dict('recode')
    return special_val

#限時搶購
def limited():
    limited_val = pd.read_csv('limited_time.csv').to_dict('recode')
    return limited_val[:12]       #只取前12筆

    