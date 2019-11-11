import requests
from bs4 import BeautifulSoup
# 引入jieba套件的analyse模組（用來分析中文關鍵字）
import jieba.analyse

url = 'https://www.books.com.tw/web/sys_bbotm/books/020903/?pd=3'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

resp = requests.get(url, headers=headers)
# 設定編碼為 utf-8 避免中文亂碼問題
resp.encoding = 'utf-8'

# 根據 HTTP header 的編碼解碼後的內容資料（ex. UTF-8），若該網站沒設定可能會有中文亂碼問題。所以通常會使用 resp.encoding 設定
raw_html = resp.text

# 將 HTML 轉成 BeautifulSoup 物件，這裡使用 html.parser 內建解析器
soup = BeautifulSoup(raw_html, "html.parser")

# 觀察書名皆為h4元素超連結a內的text
a_tags = soup.select('h4 a')

# 取出每項書名(text)，並一一放入a_tag_class類別
a_tags_class = []
for t in a_tags:
    print(t.text)
    a_tags_class += t

# 將a_tag_class類別轉換成字串a_tags_str(後面jieba.analyse.extract_tags無法分析類別，但可以分析字串)
a_tags_str = ''
for i in a_tags_class:
    a_tags_str += (i + '\n')

# 使用extract_tags函式分析並取出排名前7個的關鍵字
keywords = jieba.analyse.extract_tags(a_tags_str, 7)

# 印出關鍵字
print("關鍵字:", keywords)

# 將類別轉成字串(方便寫入txt檔)
keywords_str = ''
for i in keywords:
    keywords_str += (i + ', ')

# 使用檔案 with ... open 開啟寫入檔案模式將資料寫入
with open('keywords.txt', 'w') as output_file:
    output_file.write(a_tags_str + '\n')
    output_file.write('關鍵字: ' + keywords_str)

