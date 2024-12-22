import backtrader as bt

class TestStrategy(bt.Strategy):
    def next(self):
        if self.data.close[0] > self.data.close[-1]:  # Example logic
            self.buy(size=10)
        elif self.data.close[0] < self.data.close[-1]:
            self.sell(size=10)

cerebro = bt.Cerebro()
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)
cerebro.addstrategy(TestStrategy)
cerebro.run()
cerebro.plot()
