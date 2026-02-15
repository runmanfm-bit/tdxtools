"""
基础测试
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data.data_provider import DataProvider
from src.backtest.backtest_engine import BacktestEngine, MovingAverageCrossover, TradeAction
from src.strategy.tdx_formula_parser import TDXFormulaParser


class TestDataProvider(unittest.TestCase):
    """测试数据提供器"""
    
    def test_provider_creation(self):
        """测试创建数据提供器"""
        # 注意：这里不实际连接数据源，只测试类创建
        # 实际使用时需要网络连接
        pass
    
    def test_mock_data(self):
        """测试模拟数据"""
        # 创建模拟数据
        dates = pd.date_range('2024-01-01', '2024-01-10', freq='B')
        data = pd.DataFrame({
            'open': np.random.randn(len(dates)) * 10 + 100,
            'high': np.random.randn(len(dates)) * 10 + 105,
            'low': np.random.randn(len(dates)) * 10 + 95,
            'close': np.random.randn(len(dates)) * 10 + 100,
            'volume': np.random.randint(100000, 1000000, len(dates))
        }, index=dates)
        
        self.assertEqual(len(data), len(dates))
        self.assertIn('close', data.columns)
        self.assertIn('volume', data.columns)


class TestBacktestEngine(unittest.TestCase):
    """测试回测引擎"""
    
    def setUp(self):
        """设置测试数据"""
        # 创建模拟股价数据
        dates = pd.date_range('2024-01-01', '2024-01-31', freq='B')
        np.random.seed(42)
        
        # 生成有趋势的股价
        trend = np.linspace(0, 10, len(dates))
        noise = np.random.randn(len(dates)) * 2
        price = 100 + trend + noise
        
        self.data = pd.DataFrame({
            'open': price * 0.99,
            'high': price * 1.01,
            'low': price * 0.98,
            'close': price,
            'volume': np.random.randint(100000, 1000000, len(dates))
        }, index=dates)
        
        self.engine = BacktestEngine(initial_capital=100000.0)
        self.strategy = MovingAverageCrossover(short_window=5, long_window=10)
    
    def test_engine_creation(self):
        """测试引擎创建"""
        self.assertEqual(self.engine.initial_capital, 100000.0)
        self.assertEqual(self.engine.portfolio.initial_capital, 100000.0)
    
    def test_strategy_signals(self):
        """测试策略信号生成"""
        signals = self.strategy.generate_signals(self.data)
        
        self.assertIn('signal', signals.columns)
        self.assertIn('positions', signals.columns)
        
        # 信号应为1（买入）、-1（卖出）或0（持有）
        self.assertTrue(signals['signal'].isin([-1, 0, 1]).all())
    
    def test_portfolio_buy_sell(self):
        """测试投资组合买卖"""
        portfolio = self.engine.portfolio
        
        # 初始状态
        self.assertEqual(portfolio.cash, 100000.0)
        self.assertEqual(len(portfolio.positions), 0)
        
        # 测试买入
        success = portfolio.buy("TEST", 100.0, 100)
        self.assertTrue(success)
        self.assertEqual(portfolio.cash, 100000.0 - 100*100 - 100*100*0.0003)
        self.assertEqual(portfolio.positions["TEST"], 100)
        
        # 测试卖出
        success = portfolio.sell("TEST", 110.0, 50)
        self.assertTrue(success)
        self.assertEqual(portfolio.positions["TEST"], 50)
        
        # 测试卖出全部
        success = portfolio.sell("TEST", 120.0, 50)
        self.assertTrue(success)
        self.assertNotIn("TEST", portfolio.positions)
    
    def test_trade_records(self):
        """测试交易记录"""
        portfolio = self.engine.portfolio
        
        # 执行一些交易
        portfolio.buy("TEST1", 100.0, 100)
        portfolio.buy("TEST2", 50.0, 200)
        portfolio.sell("TEST1", 110.0, 50)
        
        self.assertEqual(len(portfolio.trades), 3)
        
        # 检查交易类型
        trade_actions = [t.action for t in portfolio.trades]
        self.assertEqual(trade_actions[0], TradeAction.BUY)
        self.assertEqual(trade_actions[1], TradeAction.BUY)
        self.assertEqual(trade_actions[2], TradeAction.SELL)


class TestTDXFormulaParser(unittest.TestCase):
    """测试通达信公式解析器"""
    
    def setUp(self):
        self.parser = TDXFormulaParser()
        
        # 示例公式
        self.example_formula = """
公式名称: 测试公式
公式描述: 这是一个测试公式

参数: N1(5,1,100), N2(10,5,200)

MA5:=MA(CLOSE,N1);
MA10:=MA(CLOSE,N2);

金叉:=CROSS(MA5,MA10);

选股:金叉;
"""
    
    def test_parser_creation(self):
        """测试解析器创建"""
        self.assertIsInstance(self.parser, TDXFormulaParser)
        self.assertIsInstance(self.parser.FUNCTION_MAP, dict)
        self.assertIn('MA', self.parser.FUNCTION_MAP)
        self.assertIn('CROSS', self.parser.FUNCTION_MAP)
    
    def test_formula_parsing(self):
        """测试公式解析"""
        result = self.parser.parse_formula(self.example_formula)
        
        self.assertIn('formula_info', result)
        self.assertIn('variables', result)
        self.assertIn('output_conditions', result)
        self.assertIn('python_code', result)
        
        # 检查公式信息
        self.assertEqual(result['formula_info']['name'], '测试公式')
        self.assertEqual(result['formula_info']['description'], '这是一个测试公式')
        
        # 检查参数
        params = result['formula_info']['params']
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]['name'], 'N1')
        self.assertEqual(params[0]['default'], 5.0)
        
        # 检查变量
        self.assertIn('MA5', result['variables'])
        self.assertIn('MA10', result['variables'])
        self.assertIn('金叉', result['variables'])
        
        # 检查输出条件
        self.assertEqual(len(result['output_conditions']), 1)
        self.assertEqual(result['output_conditions'][0]['type'], 'selection')
    
    def test_expression_conversion(self):
        """测试表达式转换"""
        # 测试基本表达式
        expr1 = "MA(CLOSE,5)"
        converted1 = self.parser._convert_expression(expr1)
        self.assertIn('ta.MA', converted1)
        
        # 测试逻辑表达式
        expr2 = "CLOSE > MA(CLOSE,10) AND VOLUME > MA(VOLUME,20)"
        converted2 = self.parser._convert_expression(expr2)
        self.assertIn('&', converted2)
        
        # 测试交叉函数
        expr3 = "CROSS(MA5,MA10)"
        converted3 = self.parser._convert_expression(expr3)
        self.assertIn('ta.CROSS', converted3)
    
    def test_strategy_generation(self):
        """测试策略生成"""
        strategy_code = self.parser.generate_strategy_class(self.example_formula)
        
        self.assertIn('class', strategy_code)
        self.assertIn('def __init__', strategy_code)
        self.assertIn('def generate_signals', strategy_code)
        self.assertIn('测试公式', strategy_code)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end_simulation(self):
        """测试端到端模拟"""
        # 创建模拟数据
        dates = pd.date_range('2024-01-01', '2024-02-01', freq='B')
        np.random.seed(123)
        
        # 生成两只股票的模拟数据
        stock1_price = 100 + np.cumsum(np.random.randn(len(dates)) * 1.5)
        stock2_price = 50 + np.cumsum(np.random.randn(len(dates)) * 1.0)
        
        data = {
            "000001.SZ": pd.DataFrame({
                'open': stock1_price * 0.99,
                'high': stock1_price * 1.01,
                'low': stock1_price * 0.98,
                'close': stock1_price,
                'volume': np.random.randint(1000000, 5000000, len(dates))
            }, index=dates),
            "000002.SZ": pd.DataFrame({
                'open': stock2_price * 0.99,
                'high': stock2_price * 1.01,
                'low': stock2_price * 0.98,
                'close': stock2_price,
                'volume': np.random.randint(500000, 3000000, len(dates))
            }, index=dates)
        }
        
        # 创建策略和引擎
        strategy = MovingAverageCrossover(short_window=5, long_window=20)
        engine = BacktestEngine(initial_capital=100000.0)
        
        # 运行回测
        results = engine.run(data, strategy)
        
        # 验证结果
        self.assertIn('total_return', results)
        self.assertIn('max_drawdown', results)
        self.assertIn('sharpe_ratio', results)
        self.assertIn('total_trades', results)
        
        # 总收益率应在合理范围内
        self.assertGreater(results['total_return'], -0.5)  # 不应亏损超过50%
        self.assertLess(results['total_return'], 2.0)  # 不应盈利超过200%
        
        # 最大回撤应在合理范围内
        self.assertGreaterEqual(results['max_drawdown'], -1.0)  # 不应超过-100%
        self.assertLessEqual(results['max_drawdown'], 0)  # 应为负数或0


if __name__ == '__main__':
    unittest.main()