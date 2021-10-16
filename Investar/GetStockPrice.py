# YahooFinance로부터 주가 데이터 받기
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import xlwt, openpyxl

# WorldIndices = ["^GSPC", "^DJI", "^IXIC", "^NYA", "^XAX", "^BUK100P", "^RUT", "^VIX", "^FTSE", "^GDAXI", "^FCHI",
#                 "^STOXX50E", "^N100", "^BFX", "IMOEX.ME", "^N225", "^HSI", "000001.SS", "399001.SZ", "^STI", "^AXJO",
#                 "^AORD", "^BSESN", "^JKSE", "^KLSE", "^NZ50", "^KS11", "^TWII", "^GSPTSE", "^BVSP", "^MXX", "^IPSA",
#                 "^MERV", "^TA125.TA", "^CASE30", "^JN0U.JO"
#                 ]

WorldIndices = {"^GSPC" : "SandP500", "^DJI" : "DowJonesIndustrialAverage", "^IXIC" : "NASDAQ_Composite",
                "^NYA" : "NYSE_COMPOSITE(DJ)", "^XAX" : "NYSE_AMEX_COMPOSITE_INDEX", "^BUK100P" : "Cboe_UK_100",
                "^RUT" : "Russell_2000", "^VIX" : "Vix", "^FTSE" : "FTSE_100", "^GDAXI" : "DAX_PERFORMANCE-INDEX",
                "^FCHI" : "CAC_40", "^STOXX50E" : "ESTX_50_PR.EUR", "^N100" : "EURONEXT_100", "^BFX" : "BEL_20",
                "IMOEX.ME" : "MOEX_Russia_Index", "^N225" : "Nikkei_225", "^HSI" : "HANG_SENG_INDEX",
                "000001.SS" : "SSE_Composite_Index", "399001.SZ" : "Shenzhen_Component", "^STI" : "STI_Index",
                "^AXJO" : "S&P_ASX_200", "^AORD" : "ALL_ORDINARIES", "^BSESN" : "S&P_BSE_SENSEX",
                "^JKSE" : "Jakarta_Composite_Index", "^KLSE" : "FTSE_Bursa_Malaysia_KLCI", "^NZ50" : "S&P_NZX_50_INDEX_GROSS",
                "^KS11" : "KOSPI_Composite_Index", "^TWII" : "TSEC_weighted_index", "^GSPTSE" : "S&P_TSX_Composite_index",
                "^BVSP" : "IBOVESPA", "^MXX" : "IPC_MEXICO", "^IPSA" : "S&P_CLX_IPSA", "^MERV" : "MERVAL",
                "^TA125.TA" : "TA-125", "^CASE30" : "EGX_30_Price_Return_Index", "^JN0U.JO" : "Top_40_USD_Net_TRI_Index"
                }

# 지수별 엑셀 Sheet 생성(https://abooda.tistory.com/26?category=969086 참조)
xlxs_dir = '/Users/jungminsong/PycharmProjects/Python_Stock_Analysis/Investar/WorldIndices.xlsx'
wb = openpyxl.Workbook(xlxs_dir)
for value in WorldIndices.values():
    wb.create_sheet(title = value)
    print(value)
wb.save(xlxs_dir)

# 지수별 데이터 받기
writer = pd.ExcelWriter(xlxs_dir, engine = 'openpyxl')
i = 0
for key, value in WorldIndices.items():
    df_i = pd.DataFrame()
    index = pdr.get_data_yahoo(key)
    df_i = df_i.append(index)
    df_i = df_i.dropna()
    print(df_i)

    # 액셀 Sheet에 지수 입력
    df_i.to_excel(writer, sheet_name = value)
writer.save()



# with pd.ExcelWriter(xlxs_dir) as writer:
    #  df_i.to_excel(writer, sheet_name = value)

# KOSPI.to_csv('/Users/jungminsong/Desktop/Global_Index/KOSPI.csv')
#
# window = 252
# peak = KOSPI['Adj Close'].rolling(window, min_periods=1).max()
# drawdown = KOSPI['Adj Close']/peak - 1.0
# max_dd = drawdown.rolling(window, min_periods=1).min()
#
# print(max_dd.min())
# print(max_dd[max_dd == -0.6465940403573595])

