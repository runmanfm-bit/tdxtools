#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取页面 - 支持多个免费数据源的股票数据下载
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 页面标题
st.title("📥 数据获取")

# 页面描述
st.markdown("""
<div class="page-description">
    从多个免费数据源下载股票数据，支持实时行情和历史数据。
</div>
""", unsafe_allow_html=True)

# 初始化session state
if 'data_source' not in st.session_state:
    st.session_state.data_source = "yfinance"
if 'stock_codes' not in st.session_state:
    st.session_state.stock_codes = "000001.SZ, 000002.SZ"
if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now() - timedelta(days=30)
if 'end_date' not in st.session_state:
    st.session_state.end_date = datetime.now()
if 'downloaded_data' not in st.session_state:
    st.session_state.downloaded_data = None

# 创建两列布局
col1, col2 = st.columns([2, 1])

with col1:
    # 数据源配置卡片
    st.markdown("""
    <div class="config-card">
        <h3>🔧 数据源配置</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据源选择
    data_source = st.selectbox(
        "选择数据源",
        ["yfinance", "akshare", "eastmoney", "sina"],
        index=0,
        help="选择要使用的数据源"
    )
    st.session_state.data_source = data_source
    
    # 数据源描述
    source_descriptions = {
        "yfinance": "Yahoo Finance - 全球股票数据，支持实时和历史数据",
        "akshare": "AkShare - 全面的A股数据，包括日线、指数、港股、美股等",
        "eastmoney": "东方财富 - A股实时数据、资金流向、龙虎榜",
        "sina": "新浪财经 - 实时行情、历史数据、分时数据"
    }
    
    st.info(f"**{data_source}**: {source_descriptions[data_source]}")
    
    # 股票代码输入
    stock_codes = st.text_area(
        "股票代码",
        value=st.session_state.stock_codes,
        help="输入股票代码，多个代码用逗号分隔。例如：000001.SZ, 000002.SZ, AAPL"
    )
    st.session_state.stock_codes = stock_codes
    
    # 时间范围选择
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        start_date = st.date_input(
            "开始日期",
            value=st.session_state.start_date,
            max_value=datetime.now()
        )
        st.session_state.start_date = start_date
        
    with col_date2:
        end_date = st.date_input(
            "结束日期",
            value=st.session_state.end_date,
            max_value=datetime.now()
        )
        st.session_state.end_date = end_date
    
    # 数据频率
    frequency = st.selectbox(
        "数据频率",
        ["日线", "周线", "月线", "60分钟", "30分钟", "15分钟", "5分钟", "1分钟"],
        index=0
    )
    
    # 高级选项
    with st.expander("⚙️ 高级选项"):
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            adjust_price = st.checkbox("复权价格", value=True)
            include_volume = st.checkbox("包含成交量", value=True)
        with col_adv2:
            include_macd = st.checkbox("计算MACD", value=False)
            include_rsi = st.checkbox("计算RSI", value=False)

with col2:
    # 数据源状态卡片
    st.markdown("""
    <div class="status-card">
        <h3>📊 数据源状态</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据源状态
    source_status = {
        "yfinance": {"status": "正常", "latency": "低", "limit": "无限制"},
        "akshare": {"status": "正常", "latency": "中", "limit": "无限制"},
        "eastmoney": {"status": "正常", "latency": "低", "limit": "无限制"},
        "sina": {"status": "正常", "latency": "低", "limit": "无限制"}
    }
    
    status_info = source_status[data_source]
    
    # 状态指标
    st.metric("状态", status_info["status"])
    st.metric("延迟", status_info["latency"])
    st.metric("限制", status_info["limit"])
    
    # 数据源统计
    st.markdown("---")
    st.markdown("#### 📈 数据统计")
    
    stats_data = {
        "数据源": ["yfinance", "akshare", "eastmoney", "sina"],
        "股票数量": ["全球", "A股全面", "A股实时", "A股历史"],
        "更新频率": ["实时", "日更", "实时", "实时"]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

# 下载按钮区域
st.markdown("---")
download_col1, download_col2, download_col3 = st.columns([1, 2, 1])

with download_col2:
    if st.button("🚀 下载数据", type="primary", use_container_width=True):
        with st.spinner("正在下载数据..."):
            # 真实数据下载
            import time
            import yfinance as yf
            
            codes = [code.strip() for code in stock_codes.split(",") if code.strip()]
            
            # 创建真实数据
            all_data = []
            success_count = 0
            
            # 根据数据源选择不同的下载方式
            if data_source == "yfinance":
                # 使用Yahoo Finance
                for code in codes[:5]:  # 限制最多5只股票
                    try:
                        # 标准化股票代码格式
                        if '.' not in code and code.isdigit() and len(code) == 6:
                            # 处理A股代码
                            if code.startswith(('6', '5')):
                                yf_code = f"{code}.SS"  # 上交所
                            else:
                                yf_code = f"{code}.SZ"  # 深交所
                        else:
                            yf_code = code
                        
                        # 下载数据
                        ticker = yf.Ticker(yf_code)
                        hist = ticker.history(start=start_date, end=end_date, interval="1d")
                        
                        if not hist.empty:
                            for date, row in hist.iterrows():
                                all_data.append({
                                    "股票代码": code,
                                    "日期": date,
                                    "开盘价": float(row['Open']),
                                    "最高价": float(row['High']),
                                    "最低价": float(row['Low']),
                                    "收盘价": float(row['Close']),
                                    "成交量": int(row['Volume']),
                                    "成交额": float(row['Close'] * row['Volume'])
                                })
                            success_count += 1
                            st.info(f"✅ {code} 数据下载成功 (Yahoo Finance)")
                        else:
                            st.warning(f"⚠️ {code} 无可用数据")
                            
                    except Exception as e:
                        st.error(f"❌ {code} 下载失败: {str(e)}")
                        continue
                        
            elif data_source == "akshare":
                # 使用AkShare (需要安装: pip install akshare)
                try:
                    import akshare as ak
                    for code in codes[:5]:
                        try:
                            # 处理A股代码
                            if '.' not in code and code.isdigit() and len(code) == 6:
                                # AkShare使用纯数字代码
                                ak_code = code
                            else:
                                ak_code = code.split('.')[0] if '.' in code else code
                            
                            # 获取股票数据
                            df_ak = ak.stock_zh_a_hist(symbol=ak_code, period="daily", 
                                                     start_date=start_date.strftime("%Y%m%d"),
                                                     end_date=end_date.strftime("%Y%m%d"),
                                                     adjust="qfq")  # 前复权
                            
                            if not df_ak.empty:
                                for _, row in df_ak.iterrows():
                                    all_data.append({
                                        "股票代码": code,
                                        "日期": pd.to_datetime(row['日期']),
                                        "开盘价": float(row['开盘']),
                                        "最高价": float(row['最高']),
                                        "最低价": float(row['最低']),
                                        "收盘价": float(row['收盘']),
                                        "成交量": int(row['成交量']),
                                        "成交额": float(row['成交额']) if '成交额' in row else 0
                                    })
                                success_count += 1
                                st.info(f"✅ {code} 数据下载成功 (AkShare)")
                            else:
                                st.warning(f"⚠️ {code} 无可用数据")
                                
                        except Exception as e:
                            st.error(f"❌ {code} 下载失败: {str(e)}")
                            continue
                            
                except ImportError:
                    st.error("❌ 未安装AkShare，请运行: pip install akshare")
                    all_data = []  # 清空数据，避免后续处理
            
            # 其他数据源的占位符
            else:
                st.warning(f"⚠️ 数据源 {data_source} 功能正在开发中...")
                # 可以在这里添加其他数据源的实现
            
            if all_data:
                df = pd.DataFrame(all_data)
                st.session_state.downloaded_data = df
                
                st.success(f"✅ 成功下载 {success_count} 只股票的数据，共 {len(df)} 条记录")
                
                # 显示数据预览
                st.subheader("📋 数据预览")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 显示统计信息
                st.subheader("📊 数据统计")
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric("股票数量", len(codes))
                with col_stat2:
                    st.metric("数据条数", len(df))
                with col_stat3:
                    st.metric("时间范围", f"{(end_date - start_date).days}天")
                with col_stat4:
                    st.metric("数据源", data_source)
            else:
                st.error("❌ 下载失败，请检查股票代码和网络连接")

# 如果已有下载的数据，显示数据分析和可视化
if st.session_state.downloaded_data is not None:
    st.markdown("---")
    st.subheader("📈 数据分析与可视化")
    
    df = st.session_state.downloaded_data
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📊 价格走势", "📈 K线图", "📉 收益率分布", "📋 数据详情"])
    
    with tab1:
        # 价格走势图
        st.markdown("#### 收盘价走势")
        
        # 选择要显示的股票
        unique_codes = df["股票代码"].unique()
        selected_codes = st.multiselect(
            "选择股票",
            unique_codes,
            default=unique_codes[:min(3, len(unique_codes))]
        )
        
        if selected_codes:
            fig = go.Figure()
            
            for code in selected_codes:
                code_data = df[df["股票代码"] == code].sort_values("日期")
                fig.add_trace(go.Scatter(
                    x=code_data["日期"],
                    y=code_data["收盘价"],
                    mode='lines',
                    name=code,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title="股票收盘价走势",
                xaxis_title="日期",
                yaxis_title="价格",
                hovermode='x unified',
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # K线图
        st.markdown("#### K线图")
        
        selected_code = st.selectbox("选择股票", unique_codes, key="kline_select")
        
        if selected_code:
            code_data = df[df["股票代码"] == selected_code].sort_values("日期")
            
            fig = go.Figure(data=[go.Candlestick(
                x=code_data["日期"],
                open=code_data["开盘价"],
                high=code_data["最高价"],
                low=code_data["最低价"],
                close=code_data["收盘价"],
                name=selected_code
            )])
            
            fig.update_layout(
                title=f"{selected_code} K线图",
                xaxis_title="日期",
                yaxis_title="价格",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # 收益率分布
        st.markdown("#### 日收益率分布")
        
        # 计算收益率
        returns_data = []
        for code in unique_codes:
            code_data = df[df["股票代码"] == code].sort_values("日期")
            if len(code_data) > 1:
                code_data["收益率"] = code_data["收盘价"].pct_change()
                returns_data.append(code_data[["股票代码", "收益率"]].dropna())
        
        if returns_data:
            returns_df = pd.concat(returns_data)
            
            fig = px.histogram(
                returns_df,
                x="收益率",
                color="股票代码",
                nbins=50,
                opacity=0.7,
                title="日收益率分布"
            )
            
            fig.update_layout(
                xaxis_title="收益率",
                yaxis_title="频数",
                template="plotly_white",
                height=500,
                barmode='overlay'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # 数据详情
        st.markdown("#### 详细数据")
        
        # 数据筛选
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            filter_code = st.selectbox("按股票筛选", ["全部"] + list(unique_codes))
        with col_filter2:
            date_range = st.date_input(
                "日期范围",
                value=[start_date, end_date],
                key="detail_date_range"
            )
        
        # 应用筛选
        filtered_df = df.copy()
        if filter_code != "全部":
            filtered_df = filtered_df[filtered_df["股票代码"] == filter_code]
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df["日期"] >= pd.Timestamp(date_range[0])) &
                (filtered_df["日期"] <= pd.Timestamp(date_range[1]))
            ]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # 数据导出
        st.markdown("---")
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("📥 导出CSV", use_container_width=True):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="下载CSV文件",
                    data=csv,
                    file_name=f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col_export2:
            if st.button("📊 导出Excel", use_container_width=True):
                # 这里需要pandas的ExcelWriter
                excel_file = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filtered_df.to_excel(excel_file, index=False)
                with open(excel_file, "rb") as f:
                    st.download_button(
                        label="下载Excel文件",
                        data=f,
                        file_name=excel_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        
        with col_export3:
            if st.button("🔄 清除数据", use_container_width=True):
                st.session_state.downloaded_data = None
                st.rerun()

# 使用说明
with st.expander("📖 使用说明"):
    st.markdown("""
    ### 数据获取页面使用指南
    
    #### 1. 选择数据源
    - **Yahoo Finance**: 适合全球股票数据，包括美股、港股等
    - **AkShare**: 适合全面的A股数据，包括日线、指数等
    - **东方财富**: 适合A股实时行情和资金流向数据
    - **新浪财经**: 适合A股历史数据和分时数据
    
    #### 2. 输入股票代码
    - 支持多种格式：`000001.SZ`、`AAPL`、`0700.HK`
    - 多个代码用逗号分隔
    - A股代码需要包含交易所后缀：`.SZ`（深交所）或`.SH`（上交所）
    
    #### 3. 设置时间范围
    - 选择开始和结束日期
    - 最大时间范围取决于数据源
    - 实时数据通常支持最近1-2年的历史数据
    
    #### 4. 高级选项
    - **复权价格**: 自动计算除权除息后的价格
    - **技术指标**: 自动计算MACD、RSI等常用指标
    
    #### 5. 数据导出
    - 支持CSV和Excel格式导出
    - 导出前可以筛选和预览数据
    - 导出的数据包含所有字段
    
    #### 注意事项
    - 免费数据源可能有访问频率限制
    - 实时数据可能有15分钟延迟
    - 建议在工作时间（9:30-15:00）获取A股数据
    - 美股数据在交易时间外可能无法获取
    """)

# 页面底部信息
st.markdown("---")
st.markdown("""
<div class="page-footer">
    <small>💡 提示：数据仅供参考，投资有风险，入市需谨慎。</small>
</div>
""", unsafe_allow_html=True)

def show():
    """显示页面内容（供主应用调用）"""
    # 页面内容已经在上面定义
    pass

if __name__ == "__main__":
    show()