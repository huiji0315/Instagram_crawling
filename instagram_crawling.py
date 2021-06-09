import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# 브라우저 열기(버전에 맞는 크롬 드라이버의 local 경로 작성)
browser = webdriver.Chrome(
    'C:/Users/huiji/Downloads/chromedriver_win32 (1)/chromedriver.exe')

# 인스타그램 접속하기
url = "https://www.instagram.com"
browser.get(url)
time.sleep(3)

# 인스타그램 로그인하기(개인정보 입력)
username = 'id'
userpw = 'password'

browser.find_element_by_name('username').send_keys(username)
browser.find_element_by_name('password').send_keys(userpw)
time.sleep(2)

# 로그인 버튼 클릭하기
browser.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[3]/button/div').click()
time.sleep(5)

# 나중에 저장하기 클릭하기
browser.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
time.sleep(5)

# 알림설정 나중에하기 클릭하기
browser.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
time.sleep(5)

# 검색결과(searching 부분에 검색할 키워드 입력)
searching = '여행에미치다'
url = f'https://www.instagram.com/explore/tags/{searching}/'
browser.get(url)
time.sleep(7)

# 첫번째 게시물 클릭하기
first_article = browser.find_elements_by_css_selector('div._9AhH0')[0]
first_article.click()
time.sleep(3)

# 데이터 수집하기
num = 500

results = []  # 전체 게시물 정보 저장할 변수/위치/공간
for n in range(num):
    try:
        # 게시물 정보 수집하기
        html = browser.page_source
        source = BeautifulSoup(html, 'html.parser')
        hashtags = []
        tags = ''
        # 본문 찾기 + 해시태그 추출
        try:
            content = source.select('div.C4VMK > span')[0]
            tags = content.select('a.xil3i')
            # print(type(content), type(tags))
            if len(tags) == 0:  # 본문에 해시태그 없으면
                try:
                    content = source.select('div.C4VMK > span')[
                        1]  # 첫번째 댓글에서 추출
                    tags = content.select('a.xil3i')
                except:
                    content = ''  # 첫번째 댓글이 없다면

        except:
            content = ''  # 본문이 없다면

        for i in range(len(tags)):  # 해시태그 없으면 저장안됨
            # print(tags[i].text)
            hashtags.append(tags[i].text)
        # print(hashtags)

        # 작성일자
        # date = source.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
        '''
        # 위치
        try:
            location = source.select('a.O4GlU')[0].text
        except:
            location = ''  # 장소가 없다면
            # print(len(location))
        '''
        # print(hashtags, date, location)
        # data = [hashtags, date, location]  # 게시물 1개 정보 저장
        # data = [hashtags, location]
        data = [hashtags]
        results.append(data)

        # 다음 게시물 클릭하기
        next_button = browser.find_elements_by_css_selector(
            'a._65Bje.coreSpriteRightPaginationArrow')[0]
        next_button.click()
        time.sleep(3+len(results)/1000)

    except:
        try:
            time.sleep(3+len(results)/100)
        except:
            try:
                time.sleep(3+len(results)/10)
            except:
                time.sleep(3+300)  # 5분 delay

    print("n= ", n+1, hashtags)

# 엑셀에 저장하기(local 컴퓨터에서 파일을 저장할 경로 입력)
df = pd.DataFrame(results)
# df.columns = ['hashtags', 'date', 'location']
# df.columns = ['hashtags', 'location']
df.columns = ['hashtags']
df.to_excel(
    'C:/Users/huiji/Desktop/Crawling/여행에미치다_210609_500.xlsx', index=False)

# browser.close()
