#!/usr/bin/env python3
"""
快速测试回测引擎
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*60)
print("通达信选股工具 - 快速测试")
print("="*60)

# 1. 创建模拟数据
print("\n1. 创建模拟股票数据...")
dates = pd.date_range('2024-01-01', '2024-02-01', freq='B')
np.random.seed(123)

# 生成股价数据
price = 100 + np.cumsum(np.random.randn(len(dates)) * 1.5)

data = pd.DataFrame({
    'open': price * 0.99,
    'high': price * 1.01,
    'low': price * 0.98,
    'close': price,
    'volume': np.random.randint(1000000, 5000000, len(dates))
}, index=dates)

print(f"✅ 创建了 {len(data)} 个交易日的模拟数据")
print(f"   起始价: {price[0]:.2f}, 结束价: {price[-1]:.2f}")
print(f"   模拟股票代码: TEST.SZ")

# 2. 测试移动平均线计算
print("\n2. 测试技术指标计算...")
data['ma5'] = data['close'].rolling(5).mean()
data['ma20'] = data['close'].rolling(20).mean()

# 计算金叉信号
data['signal'] = 0
data.loc[data['ma5'] > data['ma20'], 'signal'] = 1
data.loc[data['ma5'] < data['ma20'], 'signal'] = -1

# 计算信号变化
data['position'] = data['signal'].diff()

# 统计信号
buy_signals = (data['position'] > 0).sum()
sell_signals = (data['position'] < 0).sum()

print(f"✅ 技术指标计算完成")
print(f"   买入信号: {buy_signals} 次")
print(f"   卖出信号: {sell_signals} 次")

# 3. 模拟交易
print("\n3. 模拟交易回测...")

initial_capital = 100000.0
cash = initial_capital
positions = 0
trades = []

for date, row in data.iterrows():
    price = row['close']
    
    # 如果有买入信号且没有持仓
    if row['position'] > 0 and positions == 0:
        # 计算可买数量（按手，100股一手）
        quantity = int(cash * 0.5 / price / 100) * 100
        if quantity > 0:
            cost = quantity * price
            commission = cost * 0.0003
            cash -= (cost + commission)
            positions = quantity
            trades.append({
                'date': date,
                'action': 'BUY',
                'price': price,
                'quantity': quantity,
                'value': cost
            })
    
    # 如果有卖出信号且有持仓
    elif row['position'] < 0 and positions > 0:
        value = positions * price
        commission = value * (0.0003 + 0.001)  # 佣金+印花税
        cash += (value - commission)
        trades.append({
            'date': date,
            'action': 'SELL',
            'price': price,
            'quantity': positions,
            'value': value
        })
        positions = 0

# 计算最终价值
final_value = cash + positions * data['close'].iloc[-1]
total_return = (final_value - initial_capital) / initial_capital

print(f"✅ 回测模拟完成")
print(f"   初始资金: ¥{initial_capital:,.2f}")
print(f"   最终价值: ¥{final_value:,.2f}")
print(f"   总收益率: {total_return:.2%}")
print(f"   交易次数: {len(trades)}")

if trades:
    print(f"\n交易记录:")
    for i, trade in enumerate(trades, 1):
        action = "买入" if trade['action'] == 'BUY' else "卖出"
        print(f"   {i}. {trade['date'].date()} {action} "
              f"{trade['quantity']}股 @ ¥{trade['price']:.2f}")

# 4. 性能分析
print("\n4. 性能分析...")

# 计算日收益率
portfolio_values = []
current_value = initial_capital
positions_held = 0

for date, row in data.iterrows():
    price = row['close']
    current_value = cash + positions_held * price
    portfolio_values.append(current_value)
    
    # 更新持仓（简化）
    if row['signal'] == 1:
        positions_held = int(initial_capital * 0.5 / price / 100) * 100
        cash = initial_capital - positions_held * price
    elif row['signal'] == -1:
        positions_held = 0
        cash = current_value

# 计算风险指标
portfolio_series = pd.Series(portfolio_values, index=data.index)
returns = portfolio_series.pct_change().dropna()

if len(returns) > 1:
    # 年化收益率
    annual_return = (1 + total_return) ** (252 / len(data)) - 1
    
    # 最大回撤
    cumulative = portfolio_series
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # 夏普比率（假设无风险利率3%）
    excess_returns = returns - 0.03/252
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std() if returns.std() > 0 else 0
    
    print(f"✅ 性能指标计算完成")
    print(f"   年化收益率: {annual_return:.2%}")
    print(f"   最大回撤: {max_drawdown:.2%}")
    print(f"   夏普比率: {sharpe_ratio:.2f}")
    print(f"   日收益率均值: {returns.mean():.4%}")
    print(f"   日收益率标准差: {returns.std():.4%}")

print("\n" + "="*60)
print("快速测试完成！")
print("="*60)

# 5. 数据预览
print("\n5. 数据预览（前5行）:")
print(data[['close', 'ma5', 'ma20', 'signal']].head())

print("\n📊 总结:")
print(f"• 测试期间: {dates[0].date()} 到 {dates[-1].date()}")
print(f"• 交易日数: {len(data)}")
print(f"• 策略: 5日/20日移动平均线交叉")
print(f"• 初始资金: ¥{initial_capital:,.2f}")
print(f"• 最终价值: ¥{final_value:,.2f}")
print(f"• 总收益率: {total_return:.2%}")