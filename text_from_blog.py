#coding:utf-8
import re
import requests
from bs4 import BeautifulSoup
from simplemysql import SimpleMysql

"""
yahooブログからテキストを抽出する関数
@param account yahooブログのアカウント名
@param maxNum 抽出したいテキストの最大文字数を指定
@return テキスト, 参照された記事数
"""
def extract(account,maxNum):
    page = 0
    text = ""
    articleNum = 0
    while True:
        page = page + 1
        url = "https://blogs.yahoo.co.jp/" + account + "/MYBLOG/yblog.html";
        params = {"p":page}
        html = requests.get(url,params=params).text
        soup = BeautifulSoup(html,"html5lib")
        contentTags = soup.findAll(class_ = "entryTd")
        if not contentTags: # 配列が空ならば、もうこれ以上記事はないということ
            return text,articleNum
        for i,contentTag in enumerate(contentTags):
            articleNum = articleNum + 1
            contentText = contentTag.text
            """
            正規表現で"/n"と" "を取り除こうとしたが、シフト(" ")の方がうまく除去できなかった
            contentText = re.sub(r"[(\n+)( +)]",r"",contentText)
            """
            contentText = contentText.replace(u"\n","").replace(u" ","").replace(u"　","")
            if (len(text) + len(contentText))>maxNum:
                return text,articleNum
            text = text + contentText


def main():
    db = SimpleMysql(host="127.0.0.1",db="ybdb",user="yoneda",passwd="qweewqq")
    accounts = db.getAll("account")
    for account in accounts:
        name = account[1]
        gender = account[2]
        text, articleNum= extract(name,5000)
        db.insert("blog",{"content":text,"article_num": articleNum,"gender":gender})
        db.commit()
        print("text:"+text[0:140])
        print("account:"+name)
        print("articleNum:"+str(articleNum))
        print("gender:"+str(gender))


if __name__ == "__main__":
    main()
