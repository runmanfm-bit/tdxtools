#!/usr/bin/env python3
"""
简化版回测示例
使用模拟数据进行快速测试
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入我们的模块
from src.backtest.backtest_engine import create_backtest_engine, MovingAverageCrossover


def create_mock_data():
    """创建模拟股票数据"""
    print("创建模拟股票数据...")
    
    # 生成日期范围（最近3个月）
    dates = pd.date_range('2024-01-01', '2024-03-31', freq='B')
    np.random.seed(42)  # 固定随机种子以便复现
    
    # 生成有趋势的股价（模拟上涨趋势）
    n_days = len(dates)
    trend = np.linspace(0, 15, n_days)  # 上涨趋势
    noise = np.random.randn(n_days) * 3  # 随机波动
    price = 100 + trend + noise  # 起始价100元
    
    # 创建DataFrame
    data = pd.DataFrame({
        'open': price * 0.99,
        'high': price * 1.01,
        'low': price * 0.98,
        'close': price,
        'volume': np.random.randint(1000000, 5000000, n_days)
    }, index=dates)
    
    print(f"✅ 创建了 {n_days} 个交易日的模拟数据")
    print(f"   日期范围: {dates[0].date()} 到 {dates[-1].date()}")
    print(f"   起始价: {price[0]:.2f}, 结束价: {price[-1]:.2f}")
    print(f"   总涨幅: {(price[-1] - price[0]) / price[0]:.2%}")
    
    return data


def run_simple_backtest():
    """运行简化回测"""
    print("\n" + "="*60)
    print("通达信选股工具 - 简化回测示例")
    print("="*60)
    
    # 1. 创建模拟数据
    print("\n1. 准备数据...")
    data = create_mock_data()
    
    # 2. 创建策略
    print("\n2. 创建交易策略...")
    strategy = MovingAverageCrossover(short_window=5, long_window=20)
    print(f"✅ 策略: {strategy.name}")
    print(f"   短期均线: {strategy.short_window}日")
    print(f"   长期均线: {strategy.long_window}日")
    
    # 3. 创建回测引擎
    print("\n3. 初始化回测引擎...")
    engine = create_backtest_engine(
        initial_capital=100000.0,  # 10万元初始资金
        commission_rate=0.0003,    # 佣金率0.03%
        slippage=0.001             # 滑点0.1%
    )
    print("✅ 回测引擎初始化成功")
    
    # 4. 运行回测
    print("\n4. 运行回测...")
    try:
        # 使用模拟数据运行回测
        stock_data = {"模拟股票": data}
        results = engine.run(stock_data, strategy)
        print("✅ 回测运行完成")
    except Exception as e:
        print(f"❌ 回测运行失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. 显示结果
    print("\n5. 回测结果:")
    print("-"*40)
    
    # 基础结果
    print(f"初始资金: ¥{results['initial_capital']:,.2f}")
    print(f"最终价值: ¥{results['final_value']:,.2f}")
    print(f"绝对收益: ¥{results['final_value'] - results['initial_capital']:,.2f}")
    print(f"总收益率: {results['total_return']:.2%}")
    print(f"年化收益率: {results['annual_return']:.2%}")
    print(f"最大回撤: {results['max_drawdown']:.2%}")
    print(f"夏普比率: {results['sharpe_ratio']:.2f}")
    print(f"胜率: {results['win_rate']:.2%}")
    print(f"总交易次数: {results['total_trades']}")
    
    # 交易详情
    if results['total_trades'] > 0:
        print(f"\n交易详情:")
        trades = results['trade_details']
        for i, trade in enumerate(trades[:10], 1):  # 显示前10笔交易
            action = "买入" if trade['action'] == 'BUY' else "卖出"
            print(f"  {i}. {trade['symbol']} {action} "
                  f"{trade['quantity']}股 @ ¥{trade['price']:.2f}")
        
        if len(trades) > 10:
            print(f"  ... 还有{len(trades)-10}笔交易")
    
    # 投资组合历史
    if 'portfolio_history' in results and len(results['portfolio_history']) > 0:
        history = results['portfolio_history']
        print(f"\n投资组合历史 ({len(history)}个交易日):")
        
        # 显示关键日期的组合状态
        key_dates = [0, len(history)//4, len(history)//2, len(history)-1]
        for idx in key_dates:
            day = history[idx]
            date_str = day['date'].strftime('%Y-%m-%d')
            print(f"  {date_str}: 现金¥{day['cash']:,.2f}, "
                  f"总价值¥{day['total_value']:,.2f}")
    
    print("\n" + "="*60)
    print("回测完成！")
    print("="*60)
    
    return results


def run_multiple_strategies():
    """测试多个策略参数"""
    print("\n" + "="*60)
    print("多策略参数测试")
    print("="*60)
    
    # 创建模拟数据
    data = create_mock_data()
    stock_data = {"模拟股票": data}
    
    # 测试不同的参数组合
    param_combinations = [
        (5, 20),   # 短期5日，长期20日
        (10, 30),  # 短期10日，长期30日
        (20, 60),  # 短期20日，长期60日
    ]
    
    results = []
    
    for short_win, long_win in param_combinations:
        print(f"\n测试参数: MA({short_win}, {long_win})")
        
        strategy = MovingAverageCrossover(short_win, long_win)
        engine = create_backtest_engine(100000.0)
        
        try:
            result = engine.run(stock_data, strategy)
            results.append({
                'params': (short_win, long_win),
                'total_return': result['total_return'],
                'max_drawdown': result['max_drawdown'],
                'sharpe_ratio': result['sharpe_ratio'],
                'total_trades': result['total_trades']
            })
            
            print(f"  收益率: {result['total_return']:.2%}")
            print(f"  最大回撤: {result['max_drawdown']:.2%}")
            print(f"  夏普比率: {result['sharpe_ratio']:.2f}")
            print(f"  交易次数: {result['total_trades']}")
            
        except Exception as e:
            print(f"  测试失败: {e}")
    
    # 找出最佳参数
    if results:
        best_by_return = max(results, key=lambda x: x['total_return'])
        best_by_sharpe = max(results, key=lambda x: x['sharpe_ratio'])
        
        print("\n" + "-"*40)
        print("最佳参数分析:")
        print(f"最高收益率: MA{best_by_return['params']} = {best_by_return['total_return']:.2%}")
        print(f"最高夏普比率: MA{best_by_sharpe['params']} = {best_by_sharpe['sharpe_ratio']:.2f}")
    
    return results


if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 单策略回测")
    print("2. 多策略参数测试")
    
    try:
        choice = input("请输入选择 (1 或 2): ").strip()
    except:
        choice = "1"  # 默认选择
    
    if choice == "1":
        run_simple_backtest()
    elif choice == "2":
        run_multiple_strategies()
    else:
        print("无效选择，运行单策略回测")
        run_simple_backtest()