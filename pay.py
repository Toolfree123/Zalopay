from selenium import webdriver
import time,json,re,requests,os
desired_cap = {
 "browserName": "chrome",
    "browserVersion": "latest",
    "os": "Windows",
    "os_version": "11",
    "name": "My Test"
}

driver = webdriver.Remote(
    command_executor='https://kthithanh_eobAV5:mGk6RPZkkui8xGFU5b2U@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
driver.get('https://social.zalopay.vn/spa/v2')
time.sleep(3)
driver.save_screenshot("screenshot.png")
pin=input('ENTER PIN:')
ckzlp=''
ckzlpjson=driver.get_cookies()
print(ckzlpjson)
for i2 in ckzlpjson:
    print(i2)
    name=i2['name']
    value=i2['value']
    ckzlp=ckzlp+str(name)+'='+str(value)+'; '
os.system('cl')
print(ckzlp)
headers={
    'host': 'sapi.zalopay.vn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': ckzlp,
    'referer': 'https://l.facebook.com/',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
listid=requests.get('https://sapi.zalopay.vn/v2/history/transactions?page_size=50',headers=headers).json()
for i in range(0,int(len(listid['data']['transactions']))):
    id=listid['data']['transactions'][i]['trans_id']
    mn=listid['data']['transactions'][i]['trans_amount']
    day=listid['data']['transactions'][i]['trans_time']
    listmess=requests.get(f'https://sapi.zalopay.vn/v2/history/transactions/{id}?type=1',headers=headers).json()
    mess=listmess['data']['transaction']['description']
    print(str(id)+'|'+str(day))
    file=open('allbill.txt','a')
    file.write(str(id)+'|'+str(day)+'\n')
    file.close()
# trả thưởng bằng selemium
def pay(mgd,mn,pin,driver):
    driver.get(f'https://social.zalopay.vn/spa/v2/transfer?app_trans_id={mgd}')
    time.sleep(5)
    driver.save_screenshot("pay.png")
    driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[2]/div[1]/input').send_keys(str(int(mn)*2))
    driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div[2]/button').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[9]/div/div[2]/div/div[2]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="@um/pin-pin-input"]').send_keys(pin)
#kiểm tra bill
while True:
    listid=requests.get('https://sapi.zalopay.vn/v2/history/transactions?page_size=10',headers=headers).json()
    for so in range(10):
      id=listid['data']['transactions'][so]['trans_id']
      mn=listid['data']['transactions'][so]['trans_amount']
      day=listid['data']['transactions'][so]['trans_time']
      listmess=requests.get(f'https://sapi.zalopay.vn/v2/history/transactions/{id}?type=1',headers=headers).json()
      mess=listmess['data']['transaction']['description']
      mgd=listmess['data']['transaction']['app_trans_id']
      mess2=f'[{mn}][{mess}][{day}--{id}]'
      file=open('allbill.txt','r')
      #kiểm tra thắng thua
      if id in file.read():
          pass
          file.close()
      elif int(mn)<3 or int(mn)>10:
          print(mess2,' SAI HẠN MỨC')
      elif mess in 'cClL':
          if (str(id)[-1]) == '0':
              print(mess2,'THUA')
          #chẳn
          elif mess == 'c' or mess == 'C':
              if int(str(id)[-1])%2==0:
                  print(mess2,'THẮNG')
                  pay(mgd,mn,pin,driver)
              else:
                  print(mess2,'THUA')
          #lẻ
          elif mess == 'l' or mess == 'L':
              if int(str(id)[-1])%2==1:
                  print(mess2,'THẮNG')
                  pay(mgd,mn,pin,driver)
              else:
                  print(mess2,'THUA')
      else:
          print(mess2,' SAI CÚ PHÁP')
      #thêm tất cả bill vào file allbill.txt
      file=open('allbill.txt','a')
      file.write(str(id)+'|'+str(day)+'\n')
      file.close()
input()
