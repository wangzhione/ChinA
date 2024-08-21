import yfinance
import pandas
import matplotlib.pyplot as plot

# 四川成谕 601107.SS
# 上证指数 000001.SS
# 铁路公路 399957.SZ

# 获取 股票 stock 和 板块 plate or 指数 index 的历史数据
stock_data = yfinance.Ticker('601107.SS')
plate_data = yfinance.Ticker('000001.SS')

# 获取最近一年的数据
stock_hist = stock_data.history(period='1y')
plate_hist = plate_data.history(period='1y')

# 计算相对强度
relative_strength = 10000 * stock_hist['Close'] / plate_hist['Close']

# 创建一个新的 DataFrame 用于存储相对强度数据
data_frame = pandas.DataFrame({
    'Date': stock_hist.index,
    'StockClose': stock_hist['Close'],
    'PlateClose': plate_hist['Close'],
    'RelativeStrength': relative_strength
})

# 设置日期作为索引
data_frame.set_index('Date', inplace=True)

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
plot.bar(data_frame.index, stock_hist['Volume'], color='g')
plot.xlabel('Date')
plot.ylabel('Volume')
plot.title('Trading Volume')
plot.grid(True)

plot.tight_layout()
plot.show()