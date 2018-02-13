# coding:utf-8
import re
import sys
import requests
from bs4 import BeautifulSoup

def goodcut_text(text,num):
    """
    テキストをきりの良い句読点で区切る関数
    @param text テキスト
    @param num きりのいい数字、この数字を超えた直後の最小のインデックスで切られる
    @return text カットされたテキスト
    """
    # 正規表現で「。」を探す
    pattern = r"。"
    iterator = re.finditer(pattern,text)
    starts = []
    for match in iterator:
        starts.append(match.start())

    specificIndex = -1
    for start in starts:
        if start>num:
            specificIndex = start

    cuttedText = text[0:specificIndex+1]
    return(cuttedText)


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
    else:
        raise Exception("failed to find gender")
    return gender

def extract_article(account,num):
    """
    Yahooブログのあるユーザの記事テキストを取得する
    @param <str> account アカウント名
    @param <int> num テキスト文字数
    @return <str> テキスト
    """
    page = 0
    text = ""
    while True:
        page = page + 1
        if page>num:
            # ループしすぎた場合は処理を抜ける。
            # 集めたい文字数はnum個なので、記事の数がnumより大きいわけないという判断から
            raise Exception("many loop error")
        url = url = "https://blogs.yahoo.co.jp/" + account + "/MYBLOG/yblog.html";
        params = {"p":page}
        html = requests.get(url,params=params).text
        soup = BeautifulSoup(html,"html5lib")
        contentTags = soup.findAll(class_ = "entryTd")
        if len(contentTags)==0:
            # このpageの記事は0件だったので、ループを抜ける。
            raise Exception("text too short error")
        for contentTag in contentTags:
            contentText = contentTag.text
            contentText = contentText.replace(u"\n","").replace(u"\r","") # 改行文字を削除
            contentText = contentText.replace(u" ","").replace(u"　","") # シフトを削除
            text = text + contentText
            if len(text)>=num:
                # 抽出したテキストの文字数がnumを超えた時、関数を抜ける。
                return text


def main():
    account = random_account()

    try:
        gender = extract_gender(account)
        print(gender)
    except:
        print("性別抽出に失敗")

    try:
        text = extract_article(account,5000)
        print(text)
    except:
        print("テキスト抽出に失敗")



if __name__ == "__main__":
    main()
