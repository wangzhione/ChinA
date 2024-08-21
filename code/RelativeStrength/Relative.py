import requests
import pandas
import matplotlib.pyplot as plot
from datetime import datetime, timedelta

# 获取当前日期
end_date = datetime.today().strftime('%Y%m%d')
# 获取一年前的日期
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y%m%d')


# 获取股票的历史数据
def get_stock_data(stock_code):
    url = f'http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={stock_code}&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60&klt=101&fqt=1&beg={start_date}&end={end_date}'
    response = requests.get(url)
    data = response.json()
    kline = data['data']['klines']
    df = pandas.DataFrame([item.split(',') for item in kline], columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Turnover'])
    df['Date'] = pandas.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df[['Close', 'Volume']]
    df = df.apply(pandas.to_numeric)
    return df

# 获取板块指数的历史数据
def get_index_data(index_code):
    url = f'http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={index_code}&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60&klt=101&fqt=1&beg={start_date}&end={end_date}'
    response = requests.get(url)
    data = response.json()
    kline = data['data']['klines']
    df = pandas.DataFrame([item.split(',') for item in kline], columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Turnover'])
    df['Date'] = pandas.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df[['Close']]
    df = df.apply(pandas.to_numeric)
    return df

# 四川成谕 601107
# 上证指数 000001
# 铁路公路 BK0421

# 获取四川成渝和中证全指交通运输指数的数据
stock_data = get_stock_data('601107')
index_data = get_index_data('000957')

# 计算相对强度
relative_strength = 10000 * stock_data['Close'] / index_data['Close']

# 创建一个新的 DataFrame 用于存储相对强度数据
data_frame = pandas.DataFrame({
    'StockClose': stock_data['Close'],
    'IndexClose': index_data['Close'],
    'RelativeStrength': relative_strength
})

# 绘制图表
plot.figure(figsize=(14, 12))

# 子图：股价图
plot.subplot(3, 1, 1)
plot.plot(data_frame.index, data_frame['StockClose'], label='Stock Price', color='b')
plot.xlabel('Date')
plot.ylabel('Stock Price')
plot.title('Stock Price')
plot.legend()
plot.grid(True)

# 子图：相对强度图
plot.subplot(3, 1, 2)
plot.plot(data_frame.index, data_frame['RelativeStrength'], label='Relative Strength', color='r')
plot.xlabel('Date')
plot.ylabel('Relative Strength')
plot.title('Relative Strength')
plot.legend()
plot.grid(True)

# 子图：交易量图
plot.subplot(3, 1, 3)
plot.bar(data_frame.index, stock_data['Volume'], color='g')
plot.xlabel('Date')
plot.ylabel('Volume')
plot.title('Trading Volume')
plot.grid(True)

plot.tight_layout()
plot.show()
