# 安装指南

## 系统要求

- Python 3.8 或更高版本
- pip (Python包管理器)
- 网络连接（用于获取股票数据）

## 快速安装

### 1. 克隆或下载项目

```bash
git clone <项目地址>
cd tdxtools
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 安装TA-Lib（可选但推荐）

TA-Lib是技术分析库，提供许多技术指标计算：

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install build-essential
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

#### macOS:
```bash
brew install ta-lib
pip install TA-Lib
```

#### Windows:
下载预编译的TA-Lib：https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
然后安装：
```bash
pip install TA_Lib‑0.4.26‑cp38‑cp38‑win_amd64.whl
```

### 4. 配置数据源（可选）

如果需要使用Tushare数据源，需要获取token：

1. 访问 https://tushare.pro/ 注册账号
2. 获取token
3. 设置环境变量：
```bash
export TUSHARE_TOKEN="你的token"
```

## 验证安装

运行测试确保一切正常：

```bash
# 运行单元测试
python -m pytest tests/test_basic.py -v

# 运行示例
python examples/basic_backtest.py
```

## Docker安装（可选）

如果你使用Docker，可以使用以下方式：

```bash
# 构建镜像
docker build -t tdxtools .

# 运行容器
docker run -it --rm tdxtools python examples/basic_backtest.py
```

## 开发环境设置

如果你要参与开发，安装开发依赖：

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

安装开发工具：
```bash
# 代码格式化
pip install black

# 代码检查
pip install flake8

# 类型检查
pip install mypy

# 测试框架
pip install pytest
```

## 常见问题

### 1. TA-Lib安装失败
如果TA-Lib安装失败，可以跳过或使用纯Python实现：
```bash
pip install ta  # 纯Python的TA库
```

然后修改代码中的`import talib as ta`为`import ta`

### 2. 数据获取失败
- 检查网络连接
- 确认数据源API可用
- 对于Tushare，检查token是否正确

### 3. 内存不足
处理大量股票数据时可能需要较多内存，建议：
- 减少回测时间范围
- 减少股票数量
- 增加系统内存

### 4. 依赖冲突
如果遇到依赖冲突，可以创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 下一步

安装完成后，查看[使用指南](USAGE.md)开始使用通达信选股工具。