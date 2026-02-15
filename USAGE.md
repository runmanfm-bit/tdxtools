# 使用指南

## 快速开始

### 1. 运行示例回测

```bash
# 进入项目目录
cd tdxtools

# 运行基础示例
python examples/basic_backtest.py

# 选择模式1（完整示例）
```

### 2. 使用命令行工具

```bash
# 测试数据源
python -m tdxtools.cli test --data-source akshare

# 运行回测
python -m tdxtools.cli backtest \
  --symbols 000001.SZ,000002.SZ \
  --start-date 2024-01-01 \
  --end-date 2024-03-31 \
  --strategy ma_crossover

# 查看帮助
python -m tdxtools.cli --help
```

## 核心功能

### 1. 数据获取

#### 获取单只股票数据

```python
from src.data.data_provider import create_data_provider

# 创建数据提供器
provider = create_data_provider("akshare")  # 或 "tushare", "baostock"

# 获取平安银行数据
df = provider.get_daily_data(
    symbol="000001.SZ",
    start_date="2024-01-01",
    end_date="2024-03-31",
    adjust="qfq"  # 前复权
)

print(f"获取到 {len(df)} 条数据")
print(df.head())

# 清理资源
provider.cleanup()
```

#### 批量获取多只股票

```python
symbols = ["000001.SZ", "000002.SZ", "000858.SZ"]
data = provider.get_multiple_stocks(
    symbols=symbols,
    start_date="2024-01-01",
    end_date="2024-03-31",
    adjust="qfq"
)

for symbol, df in data.items():
    print(f"{symbol}: {len(df)} 条记录")
```

### 2. 策略回测

#### 使用内置策略

```python
from src.backtest.backtest_engine import create_backtest_engine, MovingAverageCrossover

# 创建策略
strategy = MovingAverageCrossover(short_window=5, long_window=20)

# 创建回测引擎
engine = create_backtest_engine(
    initial_capital=100000.0,  # 10万元
    commission_rate=0.0003,    # 佣金率0.03%
    slippage=0.001             # 滑点0.1%
)

# 运行回测
results = engine.run(data, strategy)

# 查看结果
engine.print_summary()

# 获取详细结果
detailed_results = engine.get_results()
print(f"总收益率: {detailed_results['total_return']:.2%}")
print(f"最大回撤: {detailed_results['max_drawdown']:.2%}")
print(f"夏普比率: {detailed_results['sharpe_ratio']:.2f}")
```

#### 自定义策略

```python
from src.backtest.backtest_engine import Strategy
import pandas as pd

class MyCustomStrategy(Strategy):
    def __init__(self, param1=10, param2=30):
        super().__init__("MyCustomStrategy")
        self.param1 = param1
        self.param2 = param2
        
    def calculate_indicators(self, data):
        data = data.copy()
        # 计算自定义指标
        data['my_indicator'] = data['close'].rolling(self.param1).mean()
        return data
        
    def generate_signals(self, data):
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # 生成信号逻辑
        data.loc[data['close'] > data['my_indicator'], 'signal'] = 1
        data.loc[data['close'] < data['my_indicator'], 'signal'] = -1
        
        data['positions'] = data['signal'].diff()
        return data
```

### 3. 通达信公式解析

#### 解析通达信公式文件

```python
from src.strategy.tdx_formula_parser import TDXFormulaParser

# 创建解析器
parser = TDXFormulaParser()

# 读取公式文件
with open("my_formula.txt", "r", encoding="utf-8") as f:
    formula_text = f.read()

# 解析公式
result = parser.parse_formula(formula_text)

print(f"公式名称: {result['formula_info']['name']}")
print(f"参数: {result['formula_info']['params']}")

# 生成策略代码
strategy_code = parser.generate_strategy_class(formula_text)

# 保存策略代码
with open("generated_strategy.py", "w", encoding="utf-8") as f:
    f.write(strategy_code)
```

#### 示例通达信公式

创建文件 `ma_cross.txt`：

```
公式名称: 双均线金叉选股
公式描述: 5日均线上穿20日均线选股公式

参数: N1(5,1,100), N2(20,5,200)

MA5:=MA(CLOSE,N1);
MA20:=MA(CLOSE,N2);

金叉:=CROSS(MA5,MA20);

选股:金叉;
```

然后解析：
```bash
python -m tdxtools.cli parse --formula-file ma_cross.txt --output ma_strategy.py
```

### 4. 结果分析

#### 基本分析

```python
results = engine.get_results()

# 收益率曲线
import matplotlib.pyplot as plt

dates = results['dates']
portfolio_values = results['portfolio_values']

plt.figure(figsize=(12, 6))
plt.plot(dates, portfolio_values)
plt.title("投资组合价值曲线")
plt.xlabel("日期")
plt.ylabel("组合价值")
plt.grid(True)
plt.show()

# 交易统计
trades = results['trade_details']
buy_trades = [t for t in trades if t['action'] == 'BUY']
sell_trades = [t for t in trades if t['action'] == 'SELL']

print(f"买入交易: {len(buy_trades)} 次")
print(f"卖出交易: {len(sell_trades)} 次")
```

#### 性能指标计算

```python
import numpy as np

# 计算日收益率
daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]

print(f"平均日收益率: {daily_returns.mean():.4%}")
print(f"日收益率标准差: {daily_returns.std():.4%}")
print(f"最大单日涨幅: {daily_returns.max():.4%}")
print(f"最大单日跌幅: {daily_returns.min():.4%}")

# 计算年化波动率
annual_volatility = daily_returns.std() * np.sqrt(252)
print(f"年化波动率: {annual_volatility:.2%}")
```

## 高级用法

### 1. 参数优化

```python
from itertools import product

# 定义参数网格
short_windows = [5, 10, 20]
long_windows = [20, 30, 60]

best_result = None
best_params = None

for short_win, long_win in product(short_windows, long_windows):
    if short_win >= long_win:
        continue
        
    strategy = MovingAverageCrossover(short_win, long_win)
    engine = create_backtest_engine(100000.0)
    results = engine.run(data, strategy)
    
    if best_result is None or results['total_return'] > best_result['total_return']:
        best_result = results
        best_params = (short_win, long_win)

print(f"最佳参数: 短期={best_params[0]}, 长期={best_params[1]}")
print(f"最佳收益率: {best_result['total_return']:.2%}")
```

### 2. 多策略组合

```python
from src.backtest.backtest_engine import Strategy
import numpy as np

class CombinedStrategy(Strategy):
    def __init__(self, strategies):
        super().__init__("CombinedStrategy")
        self.strategies = strategies
        
    def generate_signals(self, data):
        all_signals = []
        
        for strategy in self.strategies:
            signals = strategy.generate_signals(data)
            all_signals.append(signals['signal'])
            
        # 组合信号（简单平均）
        combined_signal = np.mean(all_signals, axis=0)
        
        result = data.copy()
        result['signal'] = np.where(combined_signal > 0.5, 1, 
                                   np.where(combined_signal < -0.5, -1, 0))
        result['positions'] = result['signal'].diff()
        
        return result
```

### 3. 风险控制

```python
class RiskManagedStrategy(Strategy):
    def __init__(self, base_strategy, max_position_size=0.2, stop_loss=0.1):
        super().__init__(f"RiskManaged_{base_strategy.name}")
        self.base_strategy = base_strategy
        self.max_position_size = max_position_size  # 单只股票最大仓位
        self.stop_loss = stop_loss  # 止损比例
        
    def generate_signals(self, data):
        base_signals = self.base_strategy.generate_signals(data)
        
        # 这里添加风险控制逻辑
        # 例如：限制仓位大小、添加止损等
        
        return base_signals
```

## 配置文件

项目使用YAML配置文件，位于 `config/data_sources.yaml`：

```yaml
# 数据源配置
data_sources:
  default: "akshare"
  
# 股票池配置  
stock_pools:
  csi300:
    name: "沪深300"
    symbols:
      - "000001.SZ"
      - "000002.SZ"
      # ... 更多股票

# 回测默认参数
backtest_defaults:
  initial_capital: 100000.0
  commission_rate: 0.0003
  slippage: 0.001
```

## 最佳实践

1. **数据验证**：始终检查获取的数据是否完整
2. **参数测试**：在实盘前进行充分的参数优化和回测
3. **风险管理**：添加适当的风险控制措施
4. **结果分析**：不仅看收益率，还要关注最大回撤、夏普比率等风险指标
5. **持续优化**：定期更新策略和参数

## 故障排除

### 常见问题

1. **数据获取失败**：
   - 检查网络连接
   - 确认数据源API可用
   - 检查股票代码格式（如 "000001.SZ"）

2. **回测结果异常**：
   - 检查数据质量
   - 验证策略逻辑
   - 调整佣金和滑点设置

3. **性能问题**：
   - 减少回测时间范围
   - 减少股票数量
   - 使用更高效的数据结构

### 获取帮助

- 查看示例代码：`examples/` 目录
- 运行测试：`python -m pytest tests/`
- 查看日志：设置 `logging.basicConfig(level=logging.DEBUG)`

## 下一步

- 查看[API文档](API.md)了解详细接口
- 学习如何[贡献代码](CONTRIBUTING.md)
- 查看[更新日志](CHANGELOG.md)了解最新功能