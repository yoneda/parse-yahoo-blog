#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup
from simplemysql import SimpleMysql

def main():
    url = "https://blogs.yahoo.co.jp/kirara21_0618/MYBLOG/yblog.html?m=lc&p=1"
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text,"html5lib")
    contentTag = soup.find(class_ = "entryTd userDefText")
    contentText = contentTag.text
    contentText = re.sub(r"[(\n+)( +)]",r"",contentText)
    print(contentText.replace(u"　",""))

if __name__ == "__main__":
    main()
