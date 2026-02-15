"""
基础回测引擎
实现股票策略的回测功能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class TradeAction(Enum):
    """交易动作枚举"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class Trade:
    """交易记录类"""
    
    def __init__(
        self,
        symbol: str,
        action: TradeAction,
        date: datetime,
        price: float,
        quantity: int,
        commission: float = 0.0
    ):
        self.symbol = symbol
        self.action = action
        self.date = date
        self.price = price
        self.quantity = quantity
        self.commission = commission
        self.value = price * quantity
        
    def __repr__(self):
        return f"Trade({self.symbol}, {self.action.value}, {self.date.date()}, 价格:{self.price:.2f}, 数量:{self.quantity})"


class Portfolio:
    """投资组合类"""
    
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, int] = {}  # 持仓 {symbol: quantity}
        self.position_values: Dict[str, float] = {}  # 持仓市值
        self.trades: List[Trade] = []
        self.history: List[Dict] = []  # 每日组合状态历史
        
    def buy(
        self, 
        symbol: str, 
        price: float, 
        quantity: int,
        commission_rate: float = 0.0003
    ) -> bool:
        """
        买入股票
        
        Args:
            symbol: 股票代码
            price: 买入价格
            quantity: 买入数量
            commission_rate: 佣金率
            
        Returns:
            是否成功买入
        """
        cost = price * quantity
        commission = cost * commission_rate
        
        if self.cash >= cost + commission:
            self.cash -= (cost + commission)
            
            if symbol in self.positions:
                self.positions[symbol] += quantity
            else:
                self.positions[symbol] = quantity
                
            trade = Trade(symbol, TradeAction.BUY, datetime.now(), price, quantity, commission)
            self.trades.append(trade)
            
            logger.info(f"买入 {symbol}: {quantity}股 @ {price:.2f}, 佣金:{commission:.2f}")
            return True
        else:
            logger.warning(f"资金不足，无法买入 {symbol}: 需要{cost+commission:.2f}, 可用{self.cash:.2f}")
            return False
    
    def sell(
        self, 
        symbol: str, 
        price: float, 
        quantity: int,
        commission_rate: float = 0.0013  # 卖出有印花税
    ) -> bool:
        """
        卖出股票
        
        Args:
            symbol: 股票代码
            price: 卖出价格
            quantity: 卖出数量
            commission_rate: 佣金率+印花税
            
        Returns:
            是否成功卖出
        """
        if symbol not in self.positions or self.positions[symbol] < quantity:
            logger.warning(f"持仓不足，无法卖出 {symbol}")
            return False
            
        value = price * quantity
        commission = value * commission_rate
        
        self.cash += (value - commission)
        self.positions[symbol] -= quantity
        
        if self.positions[symbol] == 0:
            del self.positions[symbol]
            
        trade = Trade(symbol, TradeAction.SELL, datetime.now(), price, quantity, commission)
        self.trades.append(trade)
        
        logger.info(f"卖出 {symbol}: {quantity}股 @ {price:.2f}, 佣金:{commission:.2f}")
        return True
    
    def update_position_values(self, price_data: Dict[str, float]):
        """
        更新持仓市值
        
        Args:
            price_data: 当前价格 {symbol: price}
        """
        total_value = self.cash
        self.position_values.clear()
        
        for symbol, quantity in self.positions.items():
            if symbol in price_data:
                value = quantity * price_data[symbol]
                self.position_values[symbol] = value
                total_value += value
            else:
                logger.warning(f"未找到{symbol}的价格数据")
                
        return total_value
    
    def record_daily_snapshot(self, date: datetime, total_value: float):
        """
        记录每日组合快照
        
        Args:
            date: 日期
            total_value: 总市值
        """
        snapshot = {
            'date': date,
            'cash': self.cash,
            'total_value': total_value,
            'positions': self.positions.copy(),
            'position_values': self.position_values.copy()
        }
        self.history.append(snapshot)
    
    def get_summary(self) -> Dict:
        """获取组合摘要"""
        return {
            'initial_capital': self.initial_capital,
            'current_cash': self.cash,
            'current_positions': self.positions,
            'total_trades': len(self.trades),
            'buy_trades': len([t for t in self.trades if t.action == TradeAction.BUY]),
            'sell_trades': len([t for t in self.trades if t.action == TradeAction.SELL])
        }


class Strategy:
    """策略基类"""
    
    def __init__(self, name: str = "BaseStrategy"):
        self.name = name
        self.signals: List[Dict] = []
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号
        
        Args:
            data: 股票数据
            
        Returns:
            包含信号的DataFrame
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术指标
        
        Args:
            data: 原始数据
            
        Returns:
            包含指标的数据
        """
        return data


class MovingAverageCrossover(Strategy):
    """移动平均线交叉策略"""
    
    def __init__(self, short_window: int = 5, long_window: int = 20):
        super().__init__(f"MA_Crossover_{short_window}_{long_window}")
        self.short_window = short_window
        self.long_window = long_window
        
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算移动平均线"""
        data = data.copy()
        data['ma_short'] = data['close'].rolling(window=self.short_window).mean()
        data['ma_long'] = data['close'].rolling(window=self.long_window).mean()
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        data = self.calculate_indicators(data)
        
        # 初始化信号列
        data['signal'] = 0
        
        # 金叉：短线上穿长线，买入信号
        data.loc[data['ma_short'] > data['ma_long'], 'signal'] = 1
        
        # 死叉：短线下穿长线，卖出信号
        data.loc[data['ma_short'] < data['ma_long'], 'signal'] = -1
        
        # 信号变化点
        data['positions'] = data['signal'].diff()
        
        return data


class BacktestEngine:
    """回测引擎"""
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission_rate: float = 0.0003,
        slippage: float = 0.001
    ):
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage  # 滑点
        self.portfolio = Portfolio(initial_capital)
        self.results: Dict = {}
        
    def run(
        self,
        data: Dict[str, pd.DataFrame],
        strategy: Strategy,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        运行回测
        
        Args:
            data: 股票数据 {symbol: DataFrame}
            strategy: 策略实例
            start_date: 回测开始日期
            end_date: 回测结束日期
            
        Returns:
            回测结果
        """
        logger.info(f"开始回测: {strategy.name}")
        
        if not data:
            raise ValueError("没有数据可供回测")
            
        # 确定时间范围
        all_dates = set()
        for df in data.values():
            all_dates.update(df.index)
            
        dates = sorted(list(all_dates))
        
        if start_date:
            dates = [d for d in dates if d >= pd.Timestamp(start_date)]
        if end_date:
            dates = [d for d in dates if d <= pd.Timestamp(end_date)]
            
        if not dates:
            raise ValueError("在指定时间范围内没有数据")
            
        logger.info(f"回测时间范围: {dates[0].date()} 到 {dates[-1].date()}, 共{len(dates)}个交易日")
        
        # 为每只股票生成信号
        signals = {}
        for symbol, df in data.items():
            signals[symbol] = strategy.generate_signals(df)
            
        # 逐日回测
        for date in dates:
            daily_prices = {}
            
            # 获取当日价格
            for symbol, df in data.items():
                if date in df.index:
                    daily_prices[symbol] = df.loc[date, 'close']
                    
            if not daily_prices:
                continue
                
            # 执行交易信号
            for symbol, signal_df in signals.items():
                if date in signal_df.index:
                    signal_row = signal_df.loc[date]
                    
                    # 检查是否有交易信号
                    if 'positions' in signal_row and abs(signal_row['positions']) > 0:
                        price = daily_prices.get(symbol)
                        if price:
                            # 考虑滑点
                            trade_price = price * (1 + self.slippage) if signal_row['positions'] > 0 else price * (1 - self.slippage)
                            
                            if signal_row['positions'] > 0:  # 买入信号
                                # 计算买入数量（这里简化：使用可用资金的50%）
                                available_cash = self.portfolio.cash * 0.5
                                quantity = int(available_cash / trade_price / 100) * 100  # 按手买入
                                
                                if quantity > 0:
                                    self.portfolio.buy(symbol, trade_price, quantity, self.commission_rate)
                                    
                            elif signal_row['positions'] < 0:  # 卖出信号
                                if symbol in self.portfolio.positions:
                                    quantity = self.portfolio.positions[symbol]
                                    self.portfolio.sell(symbol, trade_price, quantity, self.commission_rate + 0.001)  # 加印花税
            
            # 更新组合市值并记录快照
            total_value = self.portfolio.update_position_values(daily_prices)
            self.portfolio.record_daily_snapshot(date, total_value)
        
        # 计算回测结果
        self._calculate_results(dates, data)
        
        logger.info(f"回测完成，总交易次数: {len(self.portfolio.trades)}")
        return self.results
    
    def _calculate_results(self, dates: List, data: Dict[str, pd.DataFrame]):
        """计算回测结果指标"""
        if not self.portfolio.history:
            self.results = {"error": "没有回测历史数据"}
            return
            
        # 提取每日总市值
        portfolio_values = [h['total_value'] for h in self.portfolio.history]
        dates_history = [h['date'] for h in self.portfolio.history]
        
        # 计算收益率
        returns = pd.Series(portfolio_values).pct_change().dropna()
        
        # 基础指标
        total_return = (portfolio_values[-1] - self.initial_capital) / self.initial_capital
        annual_return = (1 + total_return) ** (252 / len(portfolio_values)) - 1 if len(portfolio_values) > 1 else 0
        
        # 最大回撤
        cumulative = pd.Series(portfolio_values)
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # 夏普比率（简化，假设无风险利率3%）
        if len(returns) > 1:
            excess_returns = returns - 0.03/252
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std() if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
            
        # 胜率（仅统计完整交易）
        trades = self.portfolio.trades
        if len(trades) >= 2:
            # 这里简化计算，实际需要配对买入卖出交易
            winning_trades = 0
            total_trades = 0
            
            # 简单统计：买入后价格上涨的比例
            for i in range(len(trades)-1):
                if trades[i].action == TradeAction.BUY and trades[i+1].action == TradeAction.SELL:
                    total_trades += 1
                    if trades[i+1].price > trades[i].price:
                        winning_trades += 1
                        
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
        else:
            win_rate = 0
            
        self.results = {
            'initial_capital': self.initial_capital,
            'final_value': portfolio_values[-1],
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': len(trades),
            'trade_details': [t.__dict__ for t in trades],
            'portfolio_history': self.portfolio.history,
            'dates': dates_history,
            'portfolio_values': portfolio_values
        }
    
    def get_results(self) -> Dict:
        """获取回测结果"""
        return self.results
    
    def print_summary(self):
        """打印回测摘要"""
        if not self.results:
            print("没有回测结果")
            return
            
        print("\n" + "="*50)
        print("回测结果摘要")
        print("="*50)
        print(f"初始资金: ¥{self.results['initial_capital']:,.2f}")
        print(f"最终价值: ¥{self.results['final_value']:,.2f}")
        print(f"总收益率: {self.results['total_return']:.2%}")
        print(f"年化收益率: {self.results['annual_return']:.2%}")
        print(f"最大回撤: {self.results['max_drawdown']:.2%}")
        print(f"夏普比率: {self.results['sharpe_ratio']:.2f}")
        print(f"胜率: {self.results['win_rate']:.2%}")
        print(f"总交易次数: {self.results['total_trades']}")
        print("="*50)


# 工厂函数
def create_backtest_engine(
    initial_capital: float = 100000.0,
    commission_rate: float = 0.0003,
    slippage: float = 0.001
) -> BacktestEngine:
    """创建回测引擎实例"""
    return BacktestEngine(initial_capital, commission_rate, slippage)


if __name__ == "__main__":
    # 测试代码
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建示例数据
    dates = pd.date_range('2024-01-01', '2024-03-31', freq='B')
    np.random.seed(42)
    
    # 生成模拟股价数据
    price = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
    data = pd.DataFrame({
        'open': price * 0.99,
        'high': price * 1.01,
        'low': price * 0.98,
        'close': price,
        'volume': np.random.randint(100000, 1000000, len(dates))
    }, index=dates)
    
    # 创建策略
    strategy = MovingAverageCrossover(short_window=5, long_window=20)
    
    # 创建回测引擎
    engine = create_backtest_engine(initial_capital=100000)
    
    # 运行回测
    results = engine.run({'TEST': data}, strategy)
    
    # 打印结果
    engine.print_summary()