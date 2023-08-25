# 建立連綫
import urllib.request as req

# 製作放結果的容器
all_post_titles=[]
all_post_likes=[]
all_post_time=[]

# 取得每一頁的内容
def getData(url):
    # 建立 Request 物件，附加 User-Agent 資訊讓我們看起來更像一般使用者
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    })

    # 發送連綫
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
        # print(data)

    # 解析 HTML 格式資料，取得每⼀篇文章的標題、推文數、和發佈時間
    import bs4
    root=bs4.BeautifulSoup(data, "html.parser")
    post_info=root.find_all("div", class_="title")
    post_likes=root.find_all("div", class_="nrec")

    # 取得每一篇文章的發佈時間
    def getTime():
        for post_time in post_info:
            if post_time.a in post_time:
                post_link=post_time.a["href"]
                post_com_link="https://www.ptt.cc" + post_link
                time_request=req.Request(post_com_link, headers={
                    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
                })
            with req.urlopen(time_request) as details:
                post_detail=details.read().decode("utf-8")
                
            # 取得每一篇文章的所有 HTML 資料
            detail=bs4.BeautifulSoup(post_detail, "html.parser")
            post_header=detail.find_all("span", class_="article-meta-value")
            # 取得每一篇文章的時間
            post_time=post_header[3].string
            return post_time

    # 取出每一篇文章的標題
    for post_title in post_info:
        if post_title.a in post_title:
            all_post_titles.append(post_title.a.string)
            timeurl=getTime()
            all_post_time.append(timeurl)
        else:
            clean=post_title.string.strip()
            all_post_titles.append(clean)
            all_post_time.append(None)
    
    # 取得每一篇文章的推文數
    for post_like in post_likes:
        all_post_likes.append(post_like.string)

    # 取得往上一頁的連結
    nextPage=root.find("a", string="‹ 上頁")
    nextPage=nextPage["href"]
    nextPage_com_link="https://www.ptt.cc" + nextPage
    return nextPage_com_link

# 呼叫 getData 函式取得每一頁的内容並到下一頁
Pageurl="https://www.ptt.cc/bbs/movie/index.html"
count=0
while count<3:
    Pageurl=getData(Pageurl)
    count+=1

import csv
with open("movie.txt",mode="w",newline="",encoding="utf-8") as info:
    for x in range(0,len(all_post_titles)):
        movie_info=csv.writer(info)
        movie_info.writerow([all_post_titles[x],all_post_likes[x],all_post_time[x]])



