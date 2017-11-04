#coding:utf-8
import requests
from bs4 import BeautifulSoup

def main():
    # httpライブラリを使ってhtmlを取得
    url = "https://blogs.yahoo.co.jp/manodonna/15937996.html"
    r = requests.get(url)
    text = r.text
    # html5libでは、ウェブブラウザがしているのと同じようにパースしてくれる。
    # 他にもhtml.parserやlxmlなどのオプションがある
    soup = BeautifulSoup(text,"html5lib")
    genderTag = soup.find(class_="usercard__desc")
    genderText = genderTag.string
    # tag = "<div>aaa</div>"
    # tag.string
    # =>aaaa
    print(genderText)

if __name__ == "__main__":
    main()
