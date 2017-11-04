#coding:utf-8
import requests
from bs4 import BeautifulSoup

def main():
    # httpライブラリを使ってhtmlを取得
    url = "https://blogs.yahoo.co.jp/manodonna/15937996.html"
    r = requests.get(url)
    text = r.text
    print(text)

if __name__ == "__main__":
    main()
