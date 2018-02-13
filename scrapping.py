# coding:utf-8
import re
import sys
import requests
import MySQLdb
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
    return gender

def extract_text(account,num):
    """
    Yahooブログのあるユーザの記事テキストを取得する
    @param <str> account アカウント名
    @param <int> num テキスト文字数
    @return <str> テキスト or None
    """
    page = 0
    text = ""
    while True:
        page = page + 1
        if page>num:
            # ループしすぎた場合は処理を抜ける。
            # 集めたい文字数はnum個なので、記事の数がnumより大きいわけないという判断から
            break
        url = url = "https://blogs.yahoo.co.jp/" + account + "/MYBLOG/yblog.html";
        params = {"p":page}
        html = requests.get(url,params=params).text
        soup = BeautifulSoup(html,"html5lib")
        contentTags = soup.findAll(class_ = "entryTd")
        if len(contentTags)==0:
            # このpageの記事は0件だったので、ループを抜ける。
            break
        for contentTag in contentTags:
            contentText = contentTag.text
            contentText = contentText.replace(u"\n","").replace(u"\r","") # 改行文字を削除
            contentText = contentText.replace(u" ","").replace(u"　","") # シフトを削除
            text = text + contentText
            # print(len(text))
            if len(text)>=num:
                # 抽出したテキストの文字数がnumを超えた時、関数を抜ける。
                return text
    return None

def save_to_mysql(row):
    """
    データをテーブルに挿入する関数
    @param rows <list> 挿入したいデータ
    """
    connect = MySQLdb.connect(user="root",host="localhost",db="ybdb")
    cursor = connect.cursor()
    sql = "insert into blog2000(account,gender,content) values(%s,%s,%s)"
    cursor.execute(sql,(row[0],row[1],row[2]))
    connect.commit()
    connect.close()

def get_from_mysql():
    """
    テーブルからデータをすべて取り出す関数
    @return rows
    """
    connect = MySQLdb.connect(user="root",host="localhost",db="ybdb")
    cursor = connect.cursor()
    sql = "select * from blog2000"
    cursor.execute(sql)
    blogs = cursor.fetchall()
    return blogs

def check_duplicate_account(account,rows):
    """
    アカウントがデータベースに既に存在するかどうかをチェックする関数
    """
    isDuplicate = False
    for row in rows:
        if account==row[1]:
            isDuplicate = True
    return isDuplicate

def main():
    num = 5000
    for i in range(0,100):
        account = random_account()
        gender = extract_gender(account)
        text = extract_text(account,num)
        rows = get_from_mysql()
        isDuplicate = check_duplicate_account(account,rows)
        if isDuplicate==True : print("duplicate!")
        if gender!=-1 and text!=None and isDuplicate==False:
            save_to_mysql([account,gender,text])


if __name__ == "__main__":
    main()
