# coding:utf-8
import re
import requests
from bs4 import BeautifulSoup

def random_account():
    """
    yahooブログのアカウントをランダムに1個取得する
    @return <str> account アカウント名
    """
    # yahooブログをランダムに1個取得するURL
    url = "https://blogs.yahoo.co.jp/FRONT/randomblog.html"
    r = requests.get(url)
    redirected_url = r.url
    # 正規表現でブログurlからアカウント名を抽出
    account = re.sub(r"(https://blogs.yahoo.co.jp)/(\w+)/(\d+.html)",r"\2",redirected_url)
    return account

def extract_gender(account):
    """
    Yahooブログのあるユーザの性別を取得する
    @param <str> account アカウント名
    @return <int> 0であれば男性、1であれば女性、-1であればnotfound
    """
    url = "https://blogs.yahoo.co.jp/{}".format(account)
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text,"html5lib")
    genderTag = soup.find(class_="usercard__desc")
    genderText = genderTag.string
    gender = -1
    if genderText.find(u"男性")!=-1:
        gender = 0
    elif genderText.find(u"女性")!=-1:
        gender = 1
    return gender

def main():
    for i in range(0,30):
        account = random_account()
        gender = extract_gender(account)
        print(gender)

if __name__ == "__main__":
    main()
