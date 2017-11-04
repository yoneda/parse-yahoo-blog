#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup

def main():
    url = "https://blogs.yahoo.co.jp/FRONT/randomblog.html" # yahooブログをランダムに1個取得するURL
    r = requests.get(url) # requestsはhttpのためのライブラリ
    redirected_url = r.url
    print(redirected_url)

    account = re.sub(r"(https://blogs.yahoo.co.jp)/(\w+)/(\d+.html)",r"\2",redirected_url)
    print(account)

    text = r.text
    soup = BeautifulSoup(text,"html5lib") # html5libはブラウザと同じようにパースしてくれる優れたオプション
    genderTag = soup.find(class_="usercard__desc")
    genderText = genderTag.string
    gender = -1
    # findメソッドは、ターゲットの文字列が見つかればそのインデックス開始位置を返す。見つからなければ-1を返す。
    if genderText.find("男性")!=-1: gender = 0
    elif genderText.find("女性")!=-1: gender = 1
    print(gender)

if __name__ == "__main__":
    main()
