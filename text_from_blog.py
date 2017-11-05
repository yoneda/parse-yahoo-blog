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
        contentTags = soup.findAll(class_ = "entryTd userDefText")
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
    text = extract("kirara21_0618",5000)
    print(text)
    print(len(text))
    """
    url = "https://blogs.yahoo.co.jp/kirara21_0618/MYBLOG/yblog.html?m=lc&p=1"
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text,"html5lib")
    contentTags = soup.findAll(class_ = "entryTd userDefText")
    for i,contentTag in enumerate(contentTags):
        contentText = contentTag.text
        # 正規表現で[/n]と[ ]を取り除こうとしたが、シフトの方がうまくいかなかった
        # contentText = re.sub(r"[(\n+)( +)]",r"",contentText)
        contentText = contentText.replace(u"\n","").replace(u" ","").replace(u"　","")
        print(i)
        print(len(contentText))
    """

if __name__ == "__main__":
    main()
