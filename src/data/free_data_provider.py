"""
免费数据源提供器模块
支持多种免费数据源获取股票历史数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging
import yfinance as yf
import requests
import json
from io import StringIO

logger = logging.getLogger(__name__)


class FreeDataProvider:
    """免费数据源提供器类"""
    
    def __init__(self, data_source: str = "yfinance"):
        """
        初始化免费数据提供器
        
        Args:
            data_source: 数据源类型，可选 "yfinance", "eastmoney", "sina", "akshare"
        """
        self.data_source = data_source
        self._init_data_source()
        
    def _init_data_source(self):
        """初始化数据源"""
        try:
            if self.data_source == "yfinance":
                # yfinance不需要特殊初始化
                logger.info("Yahoo Finance数据源初始化成功")
                
            elif self.data_source == "eastmoney":
                # 东方财富数据源
                logger.info("东方财富数据源初始化成功")
                
            elif self.data_source == "sina":
                # 新浪财经数据源
                logger.info("新浪财经数据源初始化成功")
                
            elif self.data_source == "akshare":
                import akshare as ak
                self.ak = ak
                logger.info("AkShare数据源初始化成功")
                
            else:
                raise ValueError(f"不支持的数据源: {self.data_source}")
                
        except ImportError as e:
            logger.error(f"导入数据源模块失败: {e}")
            raise
    
    def get_daily_data(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str = "qfq"
    ) -> pd.DataFrame:
        """
        获取日线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期，格式 "YYYY-MM-DD"
            end_date: 结束日期，格式 "YYYY-MM-DD"
            adjust: 复权类型，"qfq"前复权，"hfq"后复权，"None"不复权
            
        Returns:
            pandas DataFrame 包含日线数据
        """
        logger.info(f"使用{self.data_source}获取{symbol}日线数据: {start_date} 到 {end_date}")
        
        try:
            if self.data_source == "yfinance":
                return self._get_yfinance_daily(symbol, start_date, end_date, adjust)
            elif self.data_source == "eastmoney":
                return self._get_eastmoney_daily(symbol, start_date, end_date, adjust)
            elif self.data_source == "sina":
                return self._get_sina_daily(symbol, start_date, end_date, adjust)
            elif self.data_source == "akshare":
                return self._get_akshare_daily(symbol, start_date, end_date, adjust)
        except Exception as e:
            logger.error(f"获取日线数据失败: {e}")
            raise
    
    def _get_yfinance_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用Yahoo Finance获取日线数据"""
        # 转换股票代码格式
        if symbol.endswith('.SZ'):
            yf_symbol = f"{symbol[:6]}.SZ"
        elif symbol.endswith('.SH'):
            yf_symbol = f"{symbol[:6]}.SS"
        else:
            yf_symbol = symbol
            
        # 获取数据
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            return pd.DataFrame()
        
        # 重命名列以统一格式
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        # 添加其他必要列
        df['symbol'] = symbol
        df['amount'] = df['close'] * df['volume']
        
        # 计算涨跌幅
        df['pct_change'] = df['close'].pct_change() * 100
        
        # 复权处理
        if adjust != "None":
            df = self._adjust_yfinance_price(df, adjust, ticker)
            
        return df
    
    def _adjust_yfinance_price(self, df: pd.DataFrame, adjust_type: str, ticker) -> pd.DataFrame:
        """Yahoo Finance复权处理"""
        try:
            # 获取分红和拆股数据
            dividends = ticker.dividends
            splits = ticker.splits
            
            # 这里实现复权逻辑
            # 简化版：直接返回原始数据
            return df
        except:
            return df
    
    def _get_eastmoney_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用东方财富获取日线数据"""
        # 转换股票代码格式
        if symbol.endswith('.SZ'):
            code = f"sz{symbol[:6]}"
        elif symbol.endswith('.SH'):
            code = f"sh{symbol[:6]}"
        else:
            code = symbol
            
        # 东方财富API
        url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': code,
            'fields1': 'f1,f2,f3,f4,f5',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',  # 日线
            'fqt': '1' if adjust == "qfq" else '2' if adjust == "hfq" else '0',  # 复权类型
            'beg': start_date.replace("-", ""),
            'end': end_date.replace("-", ""),
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('rc') == 0 and 'data' in data:
                klines = data['data']['klines']
                data_list = []
                
                for kline in klines:
                    items = kline.split(',')
                    if len(items) >= 6:
                        data_list.append({
                            'date': items[0],
                            'open': float(items[1]),
                            'close': float(items[2]),
                            'high': float(items[3]),
                            'low': float(items[4]),
                            'volume': float(items[5]),
                            'amount': float(items[6]) if len(items) > 6 else 0,
                            'pct_change': float(items[8]) if len(items) > 8 else 0,
                        })
                
                df = pd.DataFrame(data_list)
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                    df['symbol'] = symbol
                    df = df.set_index('date').sort_index()
                    return df
                    
        except Exception as e:
            logger.error(f"东方财富API请求失败: {e}")
            
        return pd.DataFrame()
    
    def _get_sina_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用新浪财经获取日线数据"""
        # 转换股票代码格式
        if symbol.endswith('.SZ'):
            code = f"sz{symbol[:6]}"
        elif symbol.endswith('.SH'):
            code = f"sh{symbol[:6]}"
        else:
            code = symbol
            
        # 新浪财经API
        url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
        params = {
            'symbol': code,
            'scale': '240',  # 日线
            'ma': 'no',
            'datalen': '1000'  # 数据长度
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                
                # 重命名列
                column_mapping = {
                    'day': 'date',
                    'open': 'open',
                    'high': 'high',
                    'low': 'low',
                    'close': 'close',
                    'volume': 'volume'
                }
                
                df = df.rename(columns=column_mapping)
                
                # 转换数据类型
                numeric_cols = ['open', 'high', 'low', 'close', 'volume']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 过滤日期范围
                df['date'] = pd.to_datetime(df['date'])
                mask = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
                df = df[mask]
                
                if not df.empty:
                    df['symbol'] = symbol
                    df['amount'] = df['close'] * df['volume']
                    df['pct_change'] = df['close'].pct_change() * 100
                    df = df.set_index('date').sort_index()
                    return df
                    
        except Exception as e:
            logger.error(f"新浪财经API请求失败: {e}")
            
        return pd.DataFrame()
    
    def _get_akshare_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用AkShare获取日线数据"""
        # 转换股票代码格式
        if symbol.endswith('.SZ'):
            code = f"sz{symbol[:6]}"
        elif symbol.endswith('.SH'):
            code = f"sh{symbol[:6]}"
        else:
            code = symbol
            
        # 获取数据
        df = self.ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )
        
        if df.empty:
            return pd.DataFrame()
        
        # 重命名列
        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount',
            '振幅': 'amplitude',
            '涨跌幅': 'pct_change',
            '涨跌额': 'change',
            '换手率': 'turnover'
        })
        
        df['date'] = pd.to_datetime(df['date'])
        df['symbol'] = symbol
        df = df.set_index('date').sort_index()
        
        return df
    
    def get_multiple_stocks(
        self, 
        symbols: List[str], 
        start_date: str, 
        end_date: str,
        adjust: str = "qfq"
    ) -> Dict[str, pd.DataFrame]:
        """
        批量获取多只股票数据
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            adjust: 复权类型
            
        Returns:
            字典，key为股票代码，value为DataFrame
        """
        result = {}
        for symbol in symbols:
            try:
                df = self.get_daily_data(symbol, start_date, end_date, adjust)
                if not df.empty:
                    result[symbol] = df
                    logger.info(f"成功获取 {symbol} 数据，共 {len(df)} 条记录")
                else:
                    logger.warning(f"未获取到 {symbol} 数据")
            except Exception as e:
                logger.error(f"获取 {symbol} 数据失败: {e}")
                
        return result
    
    def get_realtime_quote(self, symbol: str) -> Dict:
        """
        获取实时行情
        
        Args:
            symbol: 股票代码
            
        Returns:
            实时行情数据字典
        """
        try:
            if self.data_source == "yfinance":
                ticker = yf.Ticker(self._convert_symbol(symbol))
                info = ticker.info
                return {
                    'symbol': symbol,
                    'price': info.get('regularMarketPrice', 0),
                    'change': info.get('regularMarketChange', 0),
                    'pct_change': info.get('regularMarketChangePercent', 0),
                    'volume': info.get('regularMarketVolume', 0),
                    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            logger.error(f"获取实时行情失败: {e}")
            
        return {}
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码格式"""
        if symbol.endswith('.SZ'):
            return f"{symbol[:6]}.SZ"
        elif symbol.endswith('.SH'):
            return f"{symbol[:6]}.SS"
        return symbol
    
    def get_market_status(self) -> Dict:
        """
        获取市场状态
        
        Returns:
            市场状态信息
        """
        # 这里可以添加获取市场状态的功能
        return {
            'status': 'open',  # open, closed, pre_market, after_hours
            'timestamp': datetime.now().isoformat(),
            'data_source': self.data_source
        }
    
    def cleanup(self):
        """清理资源"""
        # 对于免费数据源，通常不需要特殊清理
        logger.info(f"{self.data_source}数据源清理完成")


# 工厂函数
def create_free_data_provider(data_source: str = "yfinance") -> FreeDataProvider:
    """
    创建免费数据提供器实例
    
    Args:
        data_source: 数据源类型
        
    Returns:
        FreeDataProvider实例
    """
    return FreeDataProvider(data_source)


if __name__ == "__main__":
    # 测试代码
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("免费数据源测试")
    print("=" * 50)
    
    # 测试不同数据源
    data_sources = ["yfinance", "akshare", "eastmoney", "sina"]
    
    for source in data_sources:
        print(f"\n测试 {source} 数据源:")
        try:
            provider = create_free_data_provider(source)
            
            # 获取平安银行数据
            df = provider.get_daily_data(
                symbol="000001.SZ",
                start_date="2024-01-01",
                end_date="2024-01-10",
                adjust="qfq"
            )
            
            if not df.empty:
                print(f"✅ 成功获取 {len(df)} 条数据")
                print(f"   数据列: {df.columns.tolist()}")
                print(f"   日期范围: {df.index[0].date()} 到 {df.index[-1].date()}")
            else:
                print("❌ 未获取到数据")
                
            provider.cleanup()
            
        except Exception as e:
            print(f"❌ {source} 测试失败: {e}")