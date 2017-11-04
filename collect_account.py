#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup
from simplemysql import SimpleMysql

def main():
    manCount = 0
    womenCount = 0
    db = SimpleMysql(host="127.0.0.1",db="ybdb",user="yoneda",passwd="qweewqq")
    while True:
        url = "https://blogs.yahoo.co.jp/FRONT/randomblog.html" # yahooブログをランダムに1個取得するURL
        r = requests.get(url)
        redirected_url = r.url
        account = re.sub(r"(https://blogs.yahoo.co.jp)/(\w+)/(\d+.html)",r"\2",redirected_url)
        text = r.text
        soup = BeautifulSoup(text,"html5lib") # html5libはブラウザと同じようにパースしてくれる優れたオプション
        genderTag = soup.find(class_="usercard__desc")
        genderText = genderTag.string
        if genderText.find(u"男性")!=-1 and manCount<100:
            manCount = manCount + 1
            db.insert("account",{"name":account,"gender":0})
            print("account="+account+",gender=0")
        elif genderText.find(u"女性")!=-1 and womenCount<100:
            womenCount = womenCount + 1
            db.insert("account",{"name":account,"gender":1})
            print("account="+account+",gender=1")
        if manCount>=100 and womenCount>=100:
            break
    db.commit()
    print("the end")


if __name__ == "__main__":
    main()
