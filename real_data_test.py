#!/usr/bin/env python3
"""
使用真实数据测试回测
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("通达信选股工具 - 真实数据测试")
print("="*60)

try:
    # 尝试导入数据提供器
    from src.data.data_provider import create_data_provider
    print("✅ 成功导入数据提供器模块")
    
    # 创建数据提供器
    print("\n1. 初始化数据提供器...")
    try:
        provider = create_data_provider("akshare")
        print("✅ AkShare数据源初始化成功")
    except Exception as e:
        print(f"❌ 数据源初始化失败: {e}")
        print("使用模拟数据继续测试...")
        provider = None
    
    if provider:
        # 尝试获取真实数据
        print("\n2. 获取真实股票数据...")
        try:
            # 获取平安银行最近一个月的数据
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            print(f"   股票: 000001.SZ (平安银行)")
            print(f"   时间范围: {start_date} 到 {end_date}")
            
            df = provider.get_daily_data(
                symbol="000001.SZ",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
            
            if df.empty:
                print("❌ 未获取到数据，使用模拟数据")
                raise ValueError("数据为空")
                
            print(f"✅ 成功获取 {len(df)} 条数据")
            print(f"   日期范围: {df.index[0].date()} 到 {df.index[-1].date()}")
            print(f"   价格范围: ¥{df['close'].min():.2f} - ¥{df['close'].max():.2f}")
            
            # 显示数据预览
            print(f"\n数据预览:")
            print(df[['open', 'high', 'low', 'close', 'volume']].head())
            
            data = {"000001.SZ": df}
            
        except Exception as e:
            print(f"❌ 获取真实数据失败: {e}")
            print("使用模拟数据继续测试...")
            provider = None
    
    # 如果获取真实数据失败，使用模拟数据
    if not provider:
        print("\n使用模拟数据进行测试...")
        
        # 创建模拟数据
        dates = pd.date_range('2024-01-01', '2024-02-01', freq='B')
        np.random.seed(42)
        
        # 生成有趋势的股价
        trend = np.linspace(0, 10, len(dates))
        noise = np.random.randn(len(dates)) * 2
        price = 10 + trend + noise  # 起始价10元左右
        
        df = pd.DataFrame({
            'open': price * 0.99,
            'high': price * 1.01,
            'low': price * 0.98,
            'close': price,
            'volume': np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)
        
        print(f"✅ 创建了 {len(df)} 个交易日的模拟数据")
        print(f"   模拟股票: TEST.SZ")
        print(f"   起始价: ¥{price[0]:.2f}, 结束价: ¥{price[-1]:.2f}")
        
        data = {"TEST.SZ": df}
    
    # 3. 测试回测引擎
    print("\n3. 测试回测引擎...")
    try:
        from src.backtest.backtest_engine import create_backtest_engine, MovingAverageCrossover
        
        # 创建策略
        strategy = MovingAverageCrossover(short_window=5, long_window=20)
        print(f"✅ 创建策略: {strategy.name}")
        
        # 创建回测引擎
        engine = create_backtest_engine(
            initial_capital=100000.0,
            commission_rate=0.0003,
            slippage=0.001
        )
        print("✅ 回测引擎创建成功")
        
        # 运行回测
        print("\n4. 运行回测...")
        results = engine.run(data, strategy)
        print("✅ 回测运行完成")
        
        # 显示结果
        print("\n5. 回测结果:")
        print("-"*40)
        
        print(f"初始资金: ¥{results['initial_capital']:,.2f}")
        print(f"最终价值: ¥{results['final_value']:,.2f}")
        print(f"绝对收益: ¥{results['final_value'] - results['initial_capital']:,.2f}")
        print(f"总收益率: {results['total_return']:.2%}")
        print(f"年化收益率: {results['annual_return']:.2%}")
        print(f"最大回撤: {results['max_drawdown']:.2%}")
        print(f"夏普比率: {results['sharpe_ratio']:.2f}")
        print(f"胜率: {results['win_rate']:.2%}")
        print(f"总交易次数: {results['total_trades']}")
        
        # 显示交易详情
        if results['total_trades'] > 0:
            print(f"\n交易详情:")
            trades = results['trade_details']
            for i, trade in enumerate(trades[:5], 1):  # 显示前5笔交易
                action = "买入" if trade['action'] == 'BUY' else "卖出"
                print(f"  {i}. {trade['symbol']} {action} "
                      f"{trade['quantity']}股 @ ¥{trade['price']:.2f}")
            
            if len(trades) > 5:
                print(f"  ... 还有{len(trades)-5}笔交易")
        
        # 性能分析
        print("\n6. 性能分析:")
        if 'portfolio_values' in results and len(results['portfolio_values']) > 1:
            values = results['portfolio_values']
            returns = np.diff(values) / values[:-1]
            
            print(f"平均日收益率: {returns.mean():.4%}")
            print(f"日收益率标准差: {returns.std():.4%}")
            print(f"最大单日涨幅: {returns.max():.4%}")
            print(f"最大单日跌幅: {returns.min():.4%}")
            
            # 计算盈亏比（简化）
            if len(returns) > 0:
                winning_days = (returns > 0).sum()
                losing_days = (returns < 0).sum()
                print(f"盈利天数: {winning_days} ({winning_days/len(returns):.1%})")
                print(f"亏损天数: {losing_days} ({losing_days/len(returns):.1%})")
        
    except Exception as e:
        print(f"❌ 回测测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        if provider:
            print("\n7. 清理资源...")
            provider.cleanup()
            print("✅ 资源清理完成")
    
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所有依赖")
    print("运行: pip install pandas numpy akshare")

print("\n" + "="*60)
print("测试完成！")
print("="*60)