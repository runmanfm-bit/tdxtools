"""
股票数据提供器模块
支持多种数据源获取股票历史数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class DataProvider:
    """基础数据提供器类"""
    
    def __init__(self, data_source: str = "tushare"):
        """
        初始化数据提供器
        
        Args:
            data_source: 数据源类型，可选 "tushare", "akshare", "baostock"
        """
        self.data_source = data_source
        self._init_data_source()
        
    def _init_data_source(self):
        """初始化数据源"""
        try:
            if self.data_source == "tushare":
                import tushare as ts
                self.ts = ts
                # 这里需要配置token，实际使用时从环境变量读取
                self.pro = ts.pro_api()
                logger.info("Tushare数据源初始化成功")
                
            elif self.data_source == "akshare":
                import akshare as ak
                self.ak = ak
                logger.info("AkShare数据源初始化成功")
                
            elif self.data_source == "baostock":
                import baostock as bs
                self.bs = bs
                # 登录baostock
                lg = bs.login()
                if lg.error_code == '0':
                    logger.info("Baostock数据源初始化成功")
                else:
                    logger.error(f"Baostock登录失败: {lg.error_msg}")
                    
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
            symbol: 股票代码，如 "000001.SZ"
            start_date: 开始日期，格式 "YYYY-MM-DD"
            end_date: 结束日期，格式 "YYYY-MM-DD"
            adjust: 复权类型，"qfq"前复权，"hfq"后复权，"None"不复权
            
        Returns:
            pandas DataFrame 包含日线数据
        """
        logger.info(f"获取{symbol}日线数据: {start_date} 到 {end_date}")
        
        try:
            if self.data_source == "tushare":
                return self._get_tushare_daily(symbol, start_date, end_date, adjust)
            elif self.data_source == "akshare":
                return self._get_akshare_daily(symbol, start_date, end_date, adjust)
            elif self.data_source == "baostock":
                return self._get_baostock_daily(symbol, start_date, end_date, adjust)
        except Exception as e:
            logger.error(f"获取日线数据失败: {e}")
            raise
    
    def _get_tushare_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用Tushare获取日线数据"""
        df = self.pro.daily(
            ts_code=symbol,
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
        )
        
        if df.empty:
            return pd.DataFrame()
        
        # 重命名列以统一格式
        df = df.rename(columns={
            'trade_date': 'date',
            'ts_code': 'symbol',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'pre_close': 'pre_close',
            'change': 'change',
            'pct_chg': 'pct_change',
            'vol': 'volume',
            'amount': 'amount'
        })
        
        # 转换日期格式
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df = df.set_index('date').sort_index()
        
        # 如果需要复权数据
        if adjust != "None":
            df = self._adjust_price(df, adjust)
            
        return df
    
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
    
    def _get_baostock_daily(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str,
        adjust: str
    ) -> pd.DataFrame:
        """使用Baostock获取日线数据"""
        # 转换股票代码格式
        if symbol.endswith('.SZ'):
            code = f"sz.{symbol[:6]}"
        elif symbol.endswith('.SH'):
            code = f"sh.{symbol[:6]}"
        else:
            code = symbol
            
        # 获取数据
        fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"
        rs = self.bs.query_history_k_data_plus(
            code,
            fields,
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3" if adjust == "qfq" else "2" if adjust == "hfq" else "1"
        )
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
            
        df = pd.DataFrame(data_list, columns=rs.fields)
        
        if df.empty:
            return pd.DataFrame()
        
        # 转换数据类型
        numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'pctChg', 'turn']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'code': 'symbol', 'pctChg': 'pct_change'})
        df = df.set_index('date').sort_index()
        
        return df
    
    def _adjust_price(self, df: pd.DataFrame, adjust_type: str) -> pd.DataFrame:
        """
        价格复权处理（简化版）
        
        Args:
            df: 原始数据
            adjust_type: 复权类型
            
        Returns:
            复权后的数据
        """
        # 这里实现复权逻辑
        # 实际使用时需要获取复权因子进行计算
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
    
    def get_index_data(
        self, 
        index_code: str, 
        start_date: str, 
        end_date: str
    ) -> pd.DataFrame:
        """
        获取指数数据
        
        Args:
            index_code: 指数代码，如 "000001.SH" (上证指数)
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            指数数据DataFrame
        """
        # 实现指数数据获取
        return self.get_daily_data(index_code, start_date, end_date, "None")
    
    def cleanup(self):
        """清理资源"""
        if self.data_source == "baostock":
            self.bs.logout()
            logger.info("Baostock已登出")


# 工厂函数，便于使用
def create_data_provider(data_source: str = "tushare") -> DataProvider:
    """
    创建数据提供器实例
    
    Args:
        data_source: 数据源类型
        
    Returns:
        DataProvider实例
    """
    return DataProvider(data_source)


if __name__ == "__main__":
    # 测试代码
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 测试获取数据
    provider = create_data_provider("akshare")
    
    try:
        # 获取平安银行数据
        df = provider.get_daily_data(
            symbol="000001.SZ",
            start_date="2024-01-01",
            end_date="2024-01-31",
            adjust="qfq"
        )
        
        if not df.empty:
            print(f"获取到 {len(df)} 条数据")
            print(df.head())
            print(f"数据列: {df.columns.tolist()}")
        else:
            print("未获取到数据")
            
    finally:
        provider.cleanup()