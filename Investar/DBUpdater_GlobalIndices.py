import pandas as pd
import pymysql
from pandas_datareader import data as pdr
from datetime import datetime

class DBUpdater_GlobalIndices:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        print('생성자')
        self.conn = pymysql.connect(host='localhost', user='root',
                                        password='Song5056!!', db='GlobalIndices', charset='utf8')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS index_info (
                symbol VARCHAR(20),
                value VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (symbol))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                symbol VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                adj_close BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
        self.conn.commit()
        self.symbols = dict()

    def __del__(self):
            """소멸자: MariaDB 연결 해제"""
            print('소멸자')
            self.conn.close()


    def read_GlobalIndices_symbol(self):
        file = "/Users/jungminsong/PycharmProjects/Python_Stock_Analysis/Investar/WorldIndices_SymbolandName.xlsx"
        globalIndices = pd.read_excel(file, header=0)
        # globalIndices.symbol = globalIndices.symbol.map('{:06d}'.format)
        print("======read_globalIndices_symbol========\n", globalIndices)
        return globalIndices

    def update_index_info(self):
        """global index symbol을 index_info 테이블에 업데이트한 후 익셔너리에 저장"""
        sql = "SELECT * FROM index_info"
        df = pd.read_sql(sql, self.conn)  # index_info 테이블을 read_sql() 함수로 읽는다.
        # print("======update_index_info-1========\n", df)
        for idx in range(len(df)):
            self.symbols[df['symbol'].values[idx]] = df['value'].values[idx]    # 위에서 읽은 데이터프레임을 이용해서 symbol과 value로 symbol 딕셔너리를 만든다.
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM index_info"  # SELECT max() 구문을 이용해서 DB에서 가장 최근 업데이트 날짜를 가져온다.
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-d') < today:  # 위에서 구한 날짜가 존재하지 않거나 오늘보다 오래된 경우에만 저장한다.
                globalIndices = self.read_GlobalIndices_symbol()    # global index symbol 목록 파일을 읽어서 globalIndices 데이터 프레임에 저장한다
                for idx in range(len(globalIndices)):
                    symbol = globalIndices.symbol.values[idx]
                    value = globalIndices.value.values[idx]
                    sql = f"REPLACE INTO index_info (symbol, value, last_update) VALUES ('{symbol}', '{value}', '{today}')"
                    curs.execute(sql)   # Replace Into 구문을 이용해서 'symbol, value, 오늘날짜' 행을 DB에 저장한다.
                    self.symbols[symbol] = value    # symbols 딕셔너리에 키-값으로 symbol과 value를 추가한다
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO index_info VALIES ({symbol}, {value}, {today}")
                    self.conn.commit()
                    print('')
        # print("======update_index_info-2========\n", df)

    def get_GlobalIndices_price(self, symbol):
        try:
            df = pd.DataFrame() # 데이터 프레임 생성
            index = pdr.get_data_yahoo(symbol)
            # df['Date'] = df['Date'].replace('%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
            df = df.append(index)
            df = df.dropna()
            # print("======get_GlobalIndices_price========\n", df)
            # print("\n======get_GlobalIndices_price.info========\n", df.info(symbol))
            # print("\n======get_GlobalIndices_price,columns========\n", df.columns)
            # print("\n======get_GlobalIndices_price,rows========\n", df.rows)


        except Exception as e:
            print("Exceoption occured:", str(e))
            return None
        return df

    def replace_into_db(self, df, num, symbol, value):
        """get_data_yahoo에서 확보한 global index 시세를 DB에 Replace"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():       # 인수로 넘겨받은 데이터프레임을 튜플로 순회처리한다.
                # sql = f"REPLACE INTO daily_price VALUES('{}', '{}', {}, {}, {}, {}, {}, {})".format(symbol, r.date, r.open, r.high, r.low, r.close, r.adj_close, r.volume)
                sql = f"REPLACE INTO daily_price VALUES('{symbol}', '{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, {r.adj_close}, {r.volume})"
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} row > REPLACE INTO daily_price [OK]'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), num+1, value, symbol, len(df)))

    def update_daily_price(self):
        """Global index의 주식 시세를 yahoo로 부터 받아서 DB에 업데이트"""
        print("updata_daily_price-1")
        for idx, symbol in enumerate(self.symbols):
            print("updata_daily_price-2")
            df = self.read_GlobalIndices_symbol()
            print(df)
            if df is None:
                continue
            self.replace_into_db(df, idx, symbol, self.symbols[symbol])
            print(df)
        print("updata_daily_price-3")

if __name__ == '__main__':
    dbu_Global = DBUpdater_GlobalIndices()
    dbu_Global.read_GlobalIndices_symbol()
    dbu_Global.update_daily_price()

    #
    # dbu_Global.update_index_info()  # update_index_info() 메서드를 호출하여 global index 목록을 DB에 업데이트 한다.
    # dbu_Global.get_GlobalIndices_price("^GSPC")
    # dbu_Global.get_GlobalIndices_price(symbol)