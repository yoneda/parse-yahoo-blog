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
    r = None
    try:
        r = requests.get(url)
    except:
        return ""
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
    r = None
    try:
        r = requests.get(url)
    except:
        return -1
    text = r.text
    soup = BeautifulSoup(text,"html5lib")
    genderTag = soup.find(class_="usercard__desc")
    genderText = genderTag.string
    if genderText.find(u"男性")!=-1:
        return 0
    elif genderText.find(u"女性")!=-1:
        return 1
    return -1

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
        html = None
        try: html = requests.get(url,params=params).text
        except: return None # requestsのアクセス回数が超過してしまった場合はNoneを返す
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

def save_to_mysql(row,db,table):
    """
    データをテーブルに挿入する関数
    @param rows <list> 挿入したいデータ
    """
    connect = MySQLdb.connect(user="root",host="localhost",db=db)
    cursor = connect.cursor()
    sql = "insert into "+table+"(account,gender,content) values(%s,%s,%s)"
    cursor.execute(sql,(row[0],row[1],row[2]))
    connect.commit()
    connect.close()

def get_from_mysql(db,table):
    """
    テーブルからデータをすべて取り出す関数
    @return rows
    """
    connect = MySQLdb.connect(user="root",host="localhost",db=db)
    cursor = connect.cursor()
    sql = "select * from "+table
    cursor.execute(sql)
    blogs = cursor.fetchall()
    return blogs

def check_duplicate_account(account,rows):
    """
    アカウントがデータベースに既に存在するかどうかをチェックする関数
    @param <str> account アカウント名
    @param <list> rows データベースから取得したデータ
    @return <bool> 重複があったらTrue、なければFalse
    """
    isDuplicate = False
    for row in rows:
        if account==row[1]:
            isDuplicate = True
    return isDuplicate

def male_female_count(rows):
    """
    データベースのデータのうち、男性の数と女性の数を返す
    @param <list> rows データベースから取得したデータ
    @return <int,int> male,female 男性の数m女性の数
    """
    maleCounter = 0
    femaleCounter = 0
    for row in rows:
        if row[2]==0:
            maleCounter = maleCounter + 1
        elif row[2]==1:
            femaleCounter = femaleCounter + 1
    return maleCounter,femaleCounter

def check_gendermax(male,female,malemax,femalemax,gender):
    """
    今回追加しようとしている性別が、限度数に達していないか確認する関数
    男性を追加しようとしている場合、maleがmaxに到達していたらNG
    女性を追加しようとしている場合、femaleがmaxに到達していたらNG
    @param <int> male 現在の男性カウント
    @param <int> female 現在の女性カウント
    @param <int> malemax 最大の男性カウント
    @param <int> femalemax 最大の女性カウント
    @return <int> gender 今回追加しようとしている性別
    """
    isGendermax = False
    if gender==0 and male>=malemax:
        isGendermax = True
    if gender==1 and female>=femalemax:
        isGendermax = True
    return isGendermax

def remove_4byte(text):
    """
    テキストから4バイトの文字を削除
    @param text テキスト
    @param text 4バイト文字を削除したテキスト
    """
    newtext = ""
    for i,t in enumerate(text):
        bytelen = len(t.encode("utf-8"))
        if bytelen < 4:
            newtext = newtext + text[i]
    return newtext


def main():
    # この5つのパラメータを変更する
    # mumは1ユーザあたりに取得したい文字数
    # malemaxは男性ユーザ数の上限
    # femalemaxは女性ユーザ数の上限
    # dbnameはデータベース名
    # tableはテーブル名
    num = 5000
    malemax = 700
    femalemax = 700
    db = "ybdb"
    table = "blog2000"

    while True:
        # 終了条件
        rows = get_from_mysql(db,table)
        male,female = male_female_count(rows)
        if male>=malemax and female>=femalemax:
            break

        account = random_account()
        if account=="": continue
        print("account={}".format(account))
        if check_duplicate_account(account,rows)==True: continue
        gender = extract_gender(account)
        print("gender={}".format(gender))
        if gender==-1: continue
        if check_gendermax(male,female,malemax,femalemax,gender)==True: continue
        text = extract_text(account,num)
        if text!=None:
            text = remove_4byte(text)
            print("text={}".format(text[0:20]))
            save_to_mysql([account,gender,text],db,table)



if __name__ == "__main__":
    main()
