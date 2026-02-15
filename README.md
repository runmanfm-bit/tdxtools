# 通达信选股成功率测试工具 (TDXStockTools)

## 项目概述
基于通达信选股策略的回测和成功率测试工具，帮助投资者量化验证选股策略的有效性。

## 功能特性
- ✅ 通达信公式解析与转换
- ✅ 股票历史数据获取与管理
- ✅ 策略回测引擎
- ✅ 成功率分析与风险评估
- ✅ 可视化报告生成

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据源
编辑 `config/data_sources.yaml`，配置股票数据源

### 3. 运行示例
```python
python examples/basic_backtest.py
```

## 项目结构
```
tdxtools/
├── src/                    # 源代码
│   ├── data/              # 数据获取模块
│   ├── strategy/          # 策略解析模块
│   ├── backtest/          # 回测引擎
│   ├── analysis/          # 分析模块
│   └── utils/             # 工具函数
├── tests/                 # 测试代码
├── data/                  # 数据存储
├── docs/                  # 文档
├── examples/              # 使用示例
└── config/                # 配置文件
```

## 数据源支持
- Tushare (免费)
- AkShare (免费)
- Baostock (免费)
- 自定义数据源

## 开发计划
- [ ] Phase 1: 基础数据获取和回测引擎
- [ ] Phase 2: 通达信公式解析器
- [ ] Phase 3: 可视化界面
- [ ] Phase 4: 高级分析和优化

## 许可证
MIT License