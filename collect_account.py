#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup
from simplemysql import SimpleMysql

# yahooブログからランダムで記事を抽出し、[アカウント名,性別]のセットをMySQLに保存するコード
# 実行前に、[sudo mysql.server start]を実行してMySQLを起動しなければいけない
def main():
    manCount = 0
    womenCount = 0
    db = SimpleMysql(host="127.0.0.1",db="ybdb",user="yoneda",passwd="qweewqq")
    while True:
        url = "https://blogs.yahoo.co.jp/FRONT/randomblog.html" # yahooブログをランダムに1個取得するURL
        r = requests.get(url)
        redirected_url = r.url
        account = re.sub(r"(https://blogs.yahoo.co.jp)/(\w+)/(\d+.html)",r"\2",redirected_url) # 正規表現でブログurlからアカウント名を抽出
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
    db.commit() # ALERT: 最後に1回コミットではなく、whileループの中にいれたほうがよい？
    print("the end")


if __name__ == "__main__":
    main()
