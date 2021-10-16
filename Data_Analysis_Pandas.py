import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt
from scipy import stats

# 주가 변동률(일간)
sec = pdr.get_data_yahoo('005930.ks', start = '2018-05-04')
sec_dpc = (sec['Close']-sec['Close'].shift(1))/ sec['Close'].shift(1) * 100     # 일간 변동률  계산
sec_dpc.iloc[0] = 0     # 첫번째 날의 값(NaN)을 0으로 대체
sec_dpc_cs = sec_dpc.cumsum() # 일간 변동률의 누적합

msft = pdr.get_data_yahoo('MSFT', start = '2018-05-04')
msft_dpc = (msft['Close']-msft['Close'].shift(1))/ msft['Close'].shift(1) * 100
msft_dpc.iloc[0] = 0
msft_dpc_cs = msft_dpc.cumsum() # 일간 변동률의 누적합 계산

# 주가 변동률 히스토그램 작성
# plt.plot(sec.index, sec_dpc_cs, 'b', label = "Samsung Electronics")
# plt.plot(msft.index, msft_dpc_cs, 'r--', label = "Mircosoft")
# plt.ylabel('Change %')
# plt.grid(True)
# plt.legend(loc = 'best')

# MDD 계산
window = 252
peak = sec['Close'].rolling(window, min_periods = 1).max()
drawdown = sec['Close']/peak - 1.0
max_dd = drawdown.rolling(window, min_periods = 1).min()

# # MDD 그래프 작성
# plt.figure(figsize=(9, 7))
# plt.subplot(211)
# sec['Close'].plot(label = 'SEC', title = 'SEC MDD', grid = True, legend = True)
# plt.subplot(212)
# drawdown.plot(c = 'blue', label = 'SEC DD', grid = True, legend = True)
# max_dd.plot(c = 'red', label = 'SEC MDD', grid = True, legend = True)

# 지수화
sec_indexation = (sec.Close / sec.Close.loc['2018-05-04']) * 100
msft_indexation = (msft.Close / msft.Close.loc['2018-05-04']) * 100

# 지수화 비교 그래프 작성
# plt.figure(figsize=(9, 5))
# plt.plot(sec_indexation.index, sec_indexation, 'r--', label = "SEC")
# plt.plot(msft_indexation.index, msft_indexation, 'b', label = "MSFT")
# plt.grid(True)
# plt.legend(loc = 'best')


# 산점도 작성
# print(len(sec), len(msft))
df = pd.DataFrame({'X':sec['Close'], 'Y':msft['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

# 선형회귀분석
regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'

# 상관계수 구하기
print(df.corr())        # 데이터프레임으로 상관계수 구하기
print(df['X'].corr(df['Y']))
# plt.grid(True)
# plt.legend(loc = 'best')

# 결정계수(R-squared) 구하기
r_squre = df['X'].corr(df['Y'])
print(plt.show())
print(regr)

# 산점도, 회귀선 그래프 작성
plt.figure(figsize=(9, 5))
plt.plot(df.X, df.Y, '.')
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend(['SEG x MSFT', regr_line])
plt.title(f'SEC x MSFT (R = {regr.rvalue:.2f}')
plt.xlabel('Samsung')
plt.ylabel('Microsoft')
print(plt.show())

# print(sec_dpc.head())
# print(sec_dpc.describe())
# print(sec_dpc_cs)

