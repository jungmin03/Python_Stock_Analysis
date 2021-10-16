# read html() 함수로 파일 읽기
# import pandas as pd
# krx_list = pd.read_excel('/Users/jungminsong/Downloads/상장법인목록 (4).xlsx')
# krx_list.종목코드 = krx_list.종목코드.map('{:06d}'.format)
# print(krx_list)

import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import mplfinance as mpf
# from matplotlib import pyplot as plt
# from matplotlib import dates as mdates


# 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
# print(last_page)

# 전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(response_page)[0])

df = df.dropna() # n/a 제거
df = df.reset_index(drop=True) # 인덱스 리셋
# print(df)


# 차트 출력을 위해 데이터프레임 가공하기
df = df.iloc[0:30]
df = df.rename(columns = {'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by = 'Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# 엠피엘파이낸스로 캔들 차트 그리기
mpf.plot(df, title = 'Celltrion candle chart', type = 'candle')
kwargs = dict(title = 'Celltrion candle chart', type = 'candle',
              mav = (2, 4, 6), volume = True, ylabel = 'ohlc candles')
mc = mpf.make_marketcolors(up = 'r', down = 'b', inherit = True)
s = mpf.make_mpf_style(marketcolors = mc)
mpf.plot(df, **kwargs, style=s)

# df = df.sort_values(by = '날짜')
# for idx in range(0, len(df)):
#     dt = datetime.strptime(df['날짜'].values[idx], '%Y.%m.%d').date()
#     df['날짜'].values[idx] = mdates.date2num(dt)
# ohlc = df[['날짜', '시가', '고가', '저가', '종가']]

# 날짜, 종가 컬럼으로 차트 그리기
# plt.title('Celltrion (close)')
# plt.xticks(rotation = 45)
# plt.plot(df['날짜'], df['종가'], 'co-')
# plt.grid(color = 'gray', linestyle = '--')
# plt.show()

# # 엠피엘_파이낸스로 캔들차트 그리기
# plt.figure(figsize = (9, 6))
# ax = plt.subplot(1, 1, 1)
# plt.title('Celltrion (mpl_finance candle stick)')
# candlestick_ohlc(ax, ohlc.values, width = 0.7, colorup = 'red', colordown = 'blue')
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.xticks(rotation = 45)
# plt.grid(color = 'gray', linestyle = '--')
# plt.show()