from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import os
import sys
import urllib.request
import json
import ssl
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager as fm
import pytagcloud
import pygame
import simplejson
import webbrowser

def get_tags(text, ntags=200):
    spliter = Okt()
    nouns = spliter.nouns(text)
    pp = spliter.pos(text)

    count = Counter(nouns)
    return_list = list()

    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)
    return return_list


# rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False


def savewordcloud(wordstr, filename):
    taglist = pytagcloud.make_tags(dict(wordstr).items(),maxsize = 80)
    print(taglist)
    pytagcloud.create_tag_image(taglist, filename, size=(900, 600),  rectangular=False, layout=pytagcloud.LAYOUT_MOST_HORIZONTAL)
    webbrowser.open(filename)


def youtube_reply(scrollnumber_main, scrollnumber_in_video):  #########검색창에서의 pagedown 횟수와 동영상 안에서의 pagedown 횟수를 지정한다.
    searchtext = input('무엇에 대해 검색할까요?:')
    _driverPath = "C:/Users/terry/Downloads/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(_driverPath)
    driver.implicitly_wait(2)  ###컴퓨터 사양에 따라 대기시간이 있는 경우도 있어서 텀을 준다.
    driver.get('https://www.youtube.com/results?search_query=%s' % searchtext)  ##구글의 경우는 https://google.com
    body = driver.find_element_by_tag_name('body')

    numpage_main = scrollnumber_main  ###함수의 인자 pagenumber : 검색페이지에서 스크롤을 얼마나 할지 결정한다.

    while numpage_main > 0:  ###PAGE_DOWN키를 50번 누르기 위한 반복문
        body.send_keys(Keys.PAGE_DOWN)  ###body라는 태그값에 들어가서 웹페이지에 PAGE_DOWN이라는 키값을 전송한다.
        time.sleep(0.5)  ###인터넷이 느려서 버벅이는 경우를 감안해서 딜레이를 준다.
        numpage_main -= 1

    html = driver.page_source  ##페이지 다운을 눌러서 커진 소스코드를 그래도 가져온다.
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all('a', {'id': 'video-title'})

    title_list = list()
    for temp in titles:
        title_list.append(temp['href'])

    #############################
    #####페이지를 종료한다.######
    #############################
    driver.close()

    #########################################################################################
    #########실제 크롤링 시에는 지워야 할 부분이다. 일부러 argument로 설정하지 않았다.#######
    #########################################################################################
    howmany = 20  # 시범으로 딱 12개 페이지만 크롤링해오고 싶다.
    count = 0
    #########################################################################################
    #########################################################################################
    #########실제 크롤링 시에는 지워야 할 부분이다. 일부러 argument로 설정하지 않았다.#######
    #########################################################################################
    for temp in title_list:
        _driverPath = "C:/Users/terry/Downloads/chromedriver_win32/chromedriver.exe"
        driver = webdriver.Chrome(_driverPath)
        driver.implicitly_wait(0.7)  ###컴퓨터 사양에 따라 대기시간이 있는 경우도 있어서 텀을 준다.
        driver.get('https://www.youtube.com%s' % temp)  ##구글의 경우는 https://google.com

        #########################################################################################
        #########실제 크롤링 시에는 지워야 할 부분이다. 일부러 argument로 설정하지 않았다.#######
        #########################################################################################
        count += 1
        if count == howmany:
            break
        #########################################################################################
        #########실제 크롤링 시에는 지워야 할 부분이다. 일부러 argument로 설정하지 않았다.#######
        #########################################################################################

        body = driver.find_element_by_tag_name('body')  # find_element_by_tag_name: 오른쪽에 있는 'body'라는 태그값을 찾는다.

        numpage_in_video = scrollnumber_in_video

        while numpage_in_video > 0:  ###PAGE_DOWN키를 30번 누르기 위한 반복문
            body.send_keys(Keys.PAGE_DOWN)  ###body라는 태그값에 들어가서 웹페이지에 PAGE_DOWN이라는 키값을 전송한다.
            time.sleep(0.2)  ###인터넷이 느려서 버벅이는 경우를 감안해서 딜레이를 준다.
            numpage_in_video -= 1

        html = driver.page_source  ##페이지 다운을 눌러서 커진 소스코드를 그래도 가져온다.
        soup = BeautifulSoup(html, 'lxml')
        reply = soup.find_all('yt-formatted-string', 'style-scope ytd-comment-renderer')

        reply_list = list()

        ##############################################
        ####txt파일로 저장한다.#######################
        ##############################################
        reply_text = open('유튜브_%s.txt' % searchtext, 'a', encoding='utf-8')  ######일단 텍스트파일을 연다.
        ##############################################

        for temp in reply:
            reply_temp = temp.get_text()  #####temp.get_text()라는 함수를 하나의 변수로 사용하기 위해서 reply_temp라는 변수를 생성해준다.

            if reply_temp == '':  #####이스케이프 코드등을 제거해준다.
                pass
            elif '\n' in reply_temp:
                reply_temp = reply_temp.replace('\n', '')
                reply_list.append(reply_temp)
                reply_text.write(reply_temp)  ######이스케이프 코드를 제거한 문자열을 텍스트파일에 저장한다.
            else:
                #################리스트에 저장한다.#############################3
                reply_list.append(reply_temp)  ########temp.get_text() 안쓰고 temp.text로 해도 똑같다.
                reply_text.write(reply_temp)  ######문제없는 문자열을 텍스트파일에 저장한다.

        #############################
        #####페이지를 종료한다.######
        #############################
        driver.close()

        reply_text.close()  ######   '%s.txt'%searchtext 라는 txt파일을 닫아준다.

        ##############################################
        ####csv파일로 저장한다.#######################
        ##############################################
        reply_data = pd.DataFrame(pd.Series(reply_list))  ##csv로 저장하기 위해서 일단 DataFrame형태로 바꾼다.
        reply_data.to_csv('유튜브_%s.csv' % searchtext, mode='a', header=False, index=False, encoding='utf-8')

    reply_text = open('유튜브_%s.txt' % searchtext, 'r', encoding='utf-8')
    data = reply_text.read()
    reply_string = ''
    reply_string += data
    reply_text.close()

    rdata = get_tags(reply_string)
    rdata

    dictresult = {}
    for temp in rdata:
        dictresult[temp['tag']] = temp['count']

    wc = WordCloud(background_color='white', max_words=20000,
                   font_path="C:/Users/terry/Downloads/Nanum_Gothic/NanumGothic-Bold.ttf").generate_from_frequencies(dictresult)
    wc.words_
    plt.figure(figsize=(15, 15))
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig('cloud.png')
    plt.show()

if __name__ == '__main__':
    youtube_reply(20, 20)