#!/usr/bin/env python3
"""
基础回测示例
演示如何使用通达信选股工具进行策略回测
"""

import sys
import os
import logging
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.data_provider import create_data_provider
from src.backtest.backtest_engine import create_backtest_engine, MovingAverageCrossover

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_basic_backtest():
    """运行基础回测示例"""
    print("="*60)
    print("通达信选股工具 - 基础回测示例")
    print("="*60)
    
    # 1. 创建数据提供器
    print("\n1. 初始化数据提供器...")
    try:
        # 使用AkShare数据源（免费）
        provider = create_data_provider("akshare")
        print("✅ 数据提供器初始化成功")
    except Exception as e:
        print(f"❌ 数据提供器初始化失败: {e}")
        return
    
    # 2. 获取股票数据
    print("\n2. 获取股票数据...")
    symbols = ["000001.SZ", "000002.SZ"]  # 平安银行, 万科A
    
    # 设置时间范围（最近3个月）
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    print(f"   时间范围: {start_date} 到 {end_date}")
    print(f"   股票列表: {symbols}")
    
    try:
        data = provider.get_multiple_stocks(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if not data:
            print("❌ 未获取到任何股票数据")
            provider.cleanup()
            return
            
        # 打印数据统计
        for symbol, df in data.items():
            print(f"   {symbol}: {len(df)} 条记录, 日期范围: {df.index[0].date()} 到 {df.index[-1].date()}")
        
        print("✅ 数据获取成功")
        
    except Exception as e:
        print(f"❌ 数据获取失败: {e}")
        provider.cleanup()
        return
    
    # 3. 创建策略
    print("\n3. 创建交易策略...")
    strategy = MovingAverageCrossover(short_window=5, long_window=20)
    print(f"✅ 策略创建成功: {strategy.name}")
    
    # 4. 创建回测引擎
    print("\n4. 初始化回测引擎...")
    engine = create_backtest_engine(
        initial_capital=100000.0,  # 10万元初始资金
        commission_rate=0.0003,    # 佣金率0.03%
        slippage=0.001             # 滑点0.1%
    )
    print("✅ 回测引擎初始化成功")
    
    # 5. 运行回测
    print("\n5. 运行回测...")
    try:
        results = engine.run(data, strategy, start_date, end_date)
        print("✅ 回测运行完成")
    except Exception as e:
        print(f"❌ 回测运行失败: {e}")
        provider.cleanup()
        return
    
    # 6. 显示结果
    print("\n6. 回测结果:")
    engine.print_summary()
    
    # 7. 详细分析
    print("\n7. 详细分析:")
    results = engine.get_results()
    
    if results and 'total_trades' in results:
        print(f"   总交易次数: {results['total_trades']}")
        
        # 显示前5笔交易
        if results['total_trades'] > 0 and 'trade_details' in results:
            print(f"\n   最近5笔交易:")
            trades = results['trade_details'][:5]
            for i, trade in enumerate(trades, 1):
                action = "买入" if trade.get('action') == "BUY" else "卖出"
                print(f"   {i}. {trade.get('symbol')} {action} "
                      f"{trade.get('quantity')}股 @ ¥{trade.get('price'):.2f}")
    
    # 8. 性能指标
    print("\n8. 性能指标:")
    if 'portfolio_history' in results and len(results['portfolio_history']) > 0:
        history = results['portfolio_history']
        first_value = history[0]['total_value']
        last_value = history[-1]['total_value']
        
        print(f"   期初市值: ¥{first_value:,.2f}")
        print(f"   期末市值: ¥{last_value:,.2f}")
        print(f"   绝对收益: ¥{last_value - first_value:,.2f}")
        
        # 计算日收益率统计
        if 'portfolio_values' in results and len(results['portfolio_values']) > 1:
            import numpy as np
            values = results['portfolio_values']
            returns = np.diff(values) / values[:-1]
            
            print(f"   平均日收益率: {returns.mean():.4%}")
            print(f"   日收益率标准差: {returns.std():.4%}")
            print(f"   最大单日涨幅: {returns.max():.4%}")
            print(f"   最大单日跌幅: {returns.min():.4%}")
    
    # 9. 清理资源
    print("\n9. 清理资源...")
    provider.cleanup()
    print("✅ 资源清理完成")
    
    print("\n" + "="*60)
    print("示例运行完成！")
    print("="*60)


def run_single_stock_backtest():
    """单只股票回测示例"""
    print("\n" + "="*60)
    print("单只股票回测示例")
    print("="*60)
    
    # 简化版本，只测试一只股票
    provider = create_data_provider("akshare")
    
    try:
        # 获取平安银行数据
        df = provider.get_daily_data(
            symbol="000001.SZ",
            start_date="2024-01-01",
            end_date="2024-03-31",
            adjust="qfq"
        )
        
        if df.empty:
            print("未获取到数据")
            return
            
        print(f"获取到 {len(df)} 条平安银行数据")
        
        # 创建策略和引擎
        strategy = MovingAverageCrossover(10, 30)
        engine = create_backtest_engine(50000.0)
        
        # 运行回测
        results = engine.run({"000001.SZ": df}, strategy)
        
        # 显示简要结果
        print(f"\n回测结果:")
        print(f"初始资金: ¥{results['initial_capital']:,.2f}")
        print(f"最终价值: ¥{results['final_value']:,.2f}")
        print(f"总收益率: {results['total_return']:.2%}")
        print(f"交易次数: {results['total_trades']}")
        
    finally:
        provider.cleanup()


if __name__ == "__main__":
    print("选择运行模式:")
    print("1. 完整示例（多只股票）")
    print("2. 简化示例（单只股票）")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        run_basic_backtest()
    elif choice == "2":
        run_single_stock_backtest()
    else:
        print("无效选择，运行完整示例")
        run_basic_backtest()