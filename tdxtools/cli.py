#!/usr/bin/env python3
"""
通达信选股工具命令行界面
"""

import argparse
import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_provider import create_data_provider
from src.backtest.backtest_engine import create_backtest_engine, MovingAverageCrossover
from src.strategy.tdx_formula_parser import TDXFormulaParser

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """设置环境"""
    print("="*60)
    print("通达信选股成功率测试工具")
    print("="*60)


def test_data_source(args):
    """测试数据源"""
    print("\n测试数据源连接...")
    
    try:
        provider = create_data_provider(args.data_source)
        
        # 测试获取数据
        df = provider.get_daily_data(
            symbol="000001.SZ",
            start_date="2024-01-01",
            end_date="2024-01-10",
            adjust="qfq"
        )
        
        if df.empty:
            print("❌ 数据获取失败")
        else:
            print(f"✅ 数据源连接成功")
            print(f"   获取到 {len(df)} 条数据")
            print(f"   日期范围: {df.index[0].date()} 到 {df.index[-1].date()}")
            print(f"   数据列: {', '.join(df.columns.tolist())}")
            
        provider.cleanup()
        
    except Exception as e:
        print(f"❌ 数据源测试失败: {e}")


def run_backtest(args):
    """运行回测"""
    print(f"\n运行回测: {args.strategy}")
    
    # 创建数据提供器
    provider = create_data_provider(args.data_source)
    
    try:
        # 获取数据
        print(f"获取股票数据: {args.symbols}")
        data = provider.get_multiple_stocks(
            symbols=args.symbols,
            start_date=args.start_date,
            end_date=args.end_date,
            adjust=args.adjust
        )
        
        if not data:
            print("❌ 未获取到任何数据")
            return
            
        # 创建策略
        if args.strategy == "ma_crossover":
            strategy = MovingAverageCrossover(
                short_window=args.short_window,
                long_window=args.long_window
            )
        else:
            print(f"❌ 不支持的策略: {args.strategy}")
            return
            
        # 创建回测引擎
        engine = create_backtest_engine(
            initial_capital=args.capital,
            commission_rate=args.commission,
            slippage=args.slippage
        )
        
        # 运行回测
        results = engine.run(data, strategy, args.start_date, args.end_date)
        
        # 显示结果
        engine.print_summary()
        
        # 保存结果
        if args.output:
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                # 转换日期为字符串
                results_serializable = results.copy()
                if 'dates' in results_serializable:
                    results_serializable['dates'] = [d.isoformat() for d in results_serializable['dates']]
                if 'trade_details' in results_serializable:
                    for trade in results_serializable['trade_details']:
                        if 'date' in trade:
                            trade['date'] = trade['date'].isoformat()
                            
                json.dump(results_serializable, f, ensure_ascii=False, indent=2)
            print(f"✅ 结果已保存到: {args.output}")
            
    finally:
        provider.cleanup()


def parse_formula(args):
    """解析通达信公式"""
    print(f"\n解析通达信公式: {args.formula_file}")
    
    try:
        with open(args.formula_file, 'r', encoding='utf-8') as f:
            formula_text = f.read()
            
        parser = TDXFormulaParser()
        result = parser.parse_formula(formula_text)
        
        print(f"✅ 公式解析完成: {result['formula_info']['name']}")
        print(f"   描述: {result['formula_info']['description']}")
        print(f"   参数: {result['formula_info']['params']}")
        
        # 生成策略代码
        strategy_code = parser.generate_strategy_class(formula_text)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(strategy_code)
            print(f"✅ 策略代码已保存到: {args.output}")
        else:
            print("\n生成的策略代码:")
            print("="*60)
            print(strategy_code)
            
    except Exception as e:
        print(f"❌ 公式解析失败: {e}")


def show_help(args):
    """显示帮助信息"""
    print("""
可用命令:
    
  1. 测试数据源
     tdxtools test --data-source akshare
    
  2. 运行回测
     tdxtools backtest --symbols 000001.SZ,000002.SZ --strategy ma_crossover
     
  3. 解析通达信公式
     tdxtools parse --formula-file my_formula.txt
     
  4. 查看帮助
     tdxtools --help
     
示例:
  
  # 测试AkShare数据源
  tdxtools test --data-source akshare
  
  # 运行移动平均线策略回测
  tdxtools backtest --symbols 000001.SZ --start-date 2024-01-01 --end-date 2024-03-31
  
  # 解析通达信公式
  tdxtools parse --formula-file formula.txt --output strategy.py
""")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="通达信选股成功率测试工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 测试数据源命令
    test_parser = subparsers.add_parser("test", help="测试数据源连接")
    test_parser.add_argument("--data-source", default="akshare", 
                           choices=["tushare", "akshare", "baostock"],
                           help="数据源类型")
    
    # 回测命令
    backtest_parser = subparsers.add_parser("backtest", help="运行策略回测")
    backtest_parser.add_argument("--symbols", required=True,
                               help="股票代码，多个用逗号分隔，如 000001.SZ,000002.SZ")
    backtest_parser.add_argument("--strategy", default="ma_crossover",
                               choices=["ma_crossover"],
                               help="策略类型")
    backtest_parser.add_argument("--start-date", default="2024-01-01",
                               help="开始日期")
    backtest_parser.add_argument("--end-date", default="2024-03-31",
                               help="结束日期")
    backtest_parser.add_argument("--data-source", default="akshare",
                               choices=["tushare", "akshare", "baostock"],
                               help="数据源类型")
    backtest_parser.add_argument("--adjust", default="qfq",
                               choices=["qfq", "hfq", "None"],
                               help="复权类型")
    backtest_parser.add_argument("--capital", type=float, default=100000.0,
                               help="初始资金")
    backtest_parser.add_argument("--commission", type=float, default=0.0003,
                               help="佣金率")
    backtest_parser.add_argument("--slippage", type=float, default=0.001,
                               help="滑点")
    backtest_parser.add_argument("--short-window", type=int, default=5,
                               help="短期移动平均窗口（仅MA策略）")
    backtest_parser.add_argument("--long-window", type=int, default=20,
                               help="长期移动平均窗口（仅MA策略）")
    backtest_parser.add_argument("--output", help="结果输出文件")
    
    # 解析公式命令
    parse_parser = subparsers.add_parser("parse", help="解析通达信公式")
    parse_parser.add_argument("--formula-file", required=True,
                            help="通达信公式文件路径")
    parse_parser.add_argument("--output", help="输出文件路径")
    
    # 帮助命令
    help_parser = subparsers.add_parser("help", help="显示帮助信息")
    
    args = parser.parse_args()
    
    setup_environment()
    
    if args.command == "test":
        test_data_source(args)
    elif args.command == "backtest":
        # 转换symbols字符串为列表
        args.symbols = [s.strip() for s in args.symbols.split(',')]
        run_backtest(args)
    elif args.command == "parse":
        parse_formula(args)
    elif args.command == "help":
        show_help(args)
    else:
        # 如果没有指定命令，显示帮助
        parser.print_help()


if __name__ == "__main__":
    main()