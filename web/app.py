#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通达信选股工具 - Web界面主应用
支持免费数据源和策略回测的现代化Web界面
"""

import streamlit as st
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 页面配置
st.set_page_config(
    page_title="通达信选股工具",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/tdxtools',
        'Report a bug': 'https://github.com/yourusername/tdxtools/issues',
        'About': """
        ## 通达信选股工具 Web版
        
        一个基于免费数据源的股票策略回测和分析工具。
        
        **主要功能**：
        - 📊 多数据源股票数据获取
        - 🧪 策略回测和优化
        - 📝 通达信公式解析
        - 📈 交互式结果分析
        
        **版本**: 1.0.0
        """
    }
)

# 导入自定义CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "css", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 加载CSS
load_css()

# 应用标题和描述
def show_header():
    st.title("📈 通达信选股工具")
    st.markdown("""
<div class="subtitle">
    基于免费数据源的股票策略回测和分析平台
</div>
""", unsafe_allow_html=True)


# 侧边栏导航
def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🔧 导航菜单</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 导航选项
        page = st.radio(
            "选择功能",
            ["🏠 首页", "📥 数据获取", "🧪 策略回测", "📝 公式解析", "📊 结果分析", "⚙️ 设置"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 快速操作
        st.markdown("""
        <div class="sidebar-section">
            <h4>🚀 快速操作</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 刷新数据", use_container_width=True):
            st.rerun()
            
        if st.button("📊 查看示例", use_container_width=True):
            st.session_state.show_example = True
            
        if st.button("💾 导出配置", use_container_width=True):
            st.toast("配置已导出到本地", icon="✅")
        
        st.markdown("---")
        
        # 系统状态
        st.markdown("""
        <div class="sidebar-section">
            <h4>📊 系统状态</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("数据源", "4个", "正常")
        with col2:
            st.metric("策略库", "12个", "+3")
            
        # 主题切换
        st.markdown("---")
        theme = st.selectbox("🎨 主题", ["自动", "亮色", "暗色"])
        
        # 关于信息
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-footer">
            <small>版本: 1.0.0</small><br>
            <small>© 2024 通达信选股工具</small>
        </div>
        """, unsafe_allow_html=True)
        
    return page

# 首页内容
def show_home():
    st.markdown("""
    <div class="welcome-card">
        <h2>🎯 欢迎使用通达信选股工具</h2>
        <p>一个功能强大的股票策略回测和分析平台，基于免费数据源构建。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📥</div>
            <h3>数据获取</h3>
            <p>支持多个免费数据源，包括Yahoo Finance、AkShare、东方财富、新浪财经等。</p>
            <ul>
                <li>实时行情数据</li>
                <li>历史数据下载</li>
                <li>批量数据获取</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧪</div>
            <h3>策略回测</h3>
            <p>基于通达信公式的策略回测引擎，支持参数优化和结果分析。</p>
            <ul>
                <li>可视化回测配置</li>
                <li>多策略对比</li>
                <li>参数优化网格</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3>公式解析</h3>
            <p>将通达信公式转换为Python代码，支持在线编辑和测试。</p>
            <ul>
                <li>语法高亮编辑器</li>
                <li>实时代码预览</li>
                <li>一键测试功能</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 快速开始
    st.markdown("""
    <div class="quick-start">
        <h3>🚀 快速开始</h3>
        <ol>
            <li>在<strong>数据获取</strong>页面选择数据源并下载股票数据</li>
            <li>在<strong>策略回测</strong>页面配置策略参数并运行回测</li>
            <li>在<strong>结果分析</strong>页面查看回测结果和图表</li>
            <li>在<strong>公式解析</strong>页面编辑和测试通达信公式</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据源支持
    st.markdown("""
    <div class="data-sources">
        <h3>📊 支持的数据源</h3>
        <div class="sources-grid">
            <div class="source-item">
                <div class="source-logo">Y</div>
                <div class="source-info">
                    <strong>Yahoo Finance</strong>
                    <small>全球股票数据</small>
                </div>
            </div>
            <div class="source-item">
                <div class="source-logo">A</div>
                <div class="source-info">
                    <strong>AkShare</strong>
                    <small>全面的A股数据</small>
                </div>
            </div>
            <div class="source-item">
                <div class="source-logo">东</div>
                <div class="source-info">
                    <strong>东方财富</strong>
                    <small>实时行情数据</small>
                </div>
            </div>
            <div class="source-item">
                <div class="source-logo">新</div>
                <div class="source-info">
                    <strong>新浪财经</strong>
                    <small>历史数据</small>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 数据获取功能
def show_data_acquisition():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    import plotly.express as px
    
    st.title("📥 数据获取")
    
    # 页面描述
    st.markdown("""
    <div class="page-description">
        从多个免费数据源下载股票数据，支持实时行情和历史数据。
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'data_source' not in st.session_state:
        st.session_state.data_source = "akshare"
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
        
        # 数据源选择 - 只保留akshare
        data_source = st.selectbox(
            "选择数据源",
            ["akshare"],
            index=0,
            help="选择要使用的数据源"
        )
        st.session_state.data_source = data_source
        
        # 数据源描述
        source_descriptions = {
            "akshare": "AkShare - 全面的A股数据，包括日线、指数、港股、美股等"
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
            ["日线", "周线", "月线"],
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
            "akshare": {"status": "正常", "latency": "中", "limit": "无限制"}
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
            "数据源": ["akshare"],
            "股票数量": ["A股全面"],
            "更新频率": ["日更"]
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
                
                codes = [code.strip() for code in stock_codes.split(",") if code.strip()]
                
                # 创建真实数据
                all_data = []
                success_count = 0
                
                # 使用AkShare下载数据
                try:
                    import akshare as ak
                    for code in codes[:5]:  # 限制最多5只股票
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
                
                time.sleep(1)  # 模拟处理时间
                
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


# 策略回测功能
def show_backtest():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    import plotly.express as px
    import akshare as ak
    import sys
    import os
    
    # 添加项目根目录到Python路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    st.title("🧪 策略回测")
    
    # 页面描述
    st.markdown("""
    <div class="page-description">
        基于历史数据进行策略回测，评估策略收益率和风险。
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = None
    if 'backtest_config' not in st.session_state:
        st.session_state.backtest_config = {}
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 回测配置卡片
        st.markdown("""
        <div class="config-card">
            <h3>🔧 回测配置</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 策略选择
        strategy_type = st.selectbox(
            "选择策略",
            ["双均线交叉", "RSI策略", "布林带策略", "MACD策略"],
            help="选择要回测的交易策略"
        )
        
        # 策略参数配置
        if strategy_type == "双均线交叉":
            col_ma1, col_ma2 = st.columns(2)
            with col_ma1:
                short_window = st.number_input("短期均线周期", min_value=2, max_value=50, value=5)
            with col_ma2:
                long_window = st.number_input("长期均线周期", min_value=5, max_value=200, value=20)
            strategy_params = {"short_window": short_window, "long_window": long_window}
            
        elif strategy_type == "RSI策略":
            col_rsi1, col_rsi2 = st.columns(2)
            with col_rsi1:
                rsi_period = st.number_input("RSI周期", min_value=5, max_value=30, value=14)
            with col_rsi2:
                rsi_oversold = st.number_input("RSI超卖阈值", min_value=10, max_value=40, value=30)
            rsi_overbought = st.number_input("RSI超买阈值", min_value=60, max_value=90, value=70)
            strategy_params = {"rsi_period": rsi_period, "rsi_oversold": rsi_oversold, "rsi_overbought": rsi_overbought}
            
        elif strategy_type == "布林带策略":
            col_bb1, col_bb2 = st.columns(2)
            with col_bb1:
                bb_period = st.number_input("布林带周期", min_value=10, max_value=50, value=20)
            with col_bb2:
                bb_std = st.number_input("标准差倍数", min_value=1.0, max_value=3.0, value=2.0, step=0.5)
            strategy_params = {"bb_period": bb_period, "bb_std": bb_std}
            
        else:  # MACD策略
            col_macd1, col_macd2, col_macd3 = st.columns(3)
            with col_macd1:
                macd_fast = st.number_input("MACD快线", min_value=5, max_value=20, value=12)
            with col_macd2:
                macd_slow = st.number_input("MACD慢线", min_value=15, max_value=40, value=26)
            with col_macd3:
                macd_signal = st.number_input("信号线", min_value=5, max_value=15, value=9)
            strategy_params = {"macd_fast": macd_fast, "macd_slow": macd_slow, "macd_signal": macd_signal}
        
        # 回测参数
        st.markdown("---")
        st.markdown("#### 💰 回测参数")
        
        col_cap1, col_cap2 = st.columns(2)
        with col_cap1:
            initial_capital = st.number_input("初始资金(¥)", min_value=10000, value=100000, step=10000)
        with col_cap2:
            commission_rate = st.number_input("佣金费率(%)", min_value=0.01, max_value=0.5, value=0.03, step=0.01)
        
        slippage = st.number_input("滑点(%)", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
        
        # 股票选择
        st.markdown("---")
        st.markdown("#### 📈 股票选择")
        
        stock_code = st.text_input(
            "股票代码",
            value="000001.SZ",
            help="输入股票代码，例如：000001.SZ（平安银行）"
        )
        
        # 时间范围
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            backtest_start = st.date_input(
                "开始日期",
                value=datetime.now() - timedelta(days=365),
                max_value=datetime.now()
            )
        with col_date2:
            backtest_end = st.date_input(
                "结束日期",
                value=datetime.now(),
                max_value=datetime.now()
            )

    with col2:
        # 策略说明卡片
        st.markdown("""
        <div class="status-card">
            <h3>📋 策略说明</h3>
        </div>
        """, unsafe_allow_html=True)
        
        strategy_descriptions = {
            "双均线交叉": "当短期均线上穿长期均线时买入，下穿时卖出。适用于趋势明显的行情。",
            "RSI策略": "RSI低于超卖阈值时买入，高于超买阈值时卖出。适用于震荡行情。",
            "布林带策略": "价格突破布林带上轨时卖出，跌破下轨时买入。",
            "MACD策略": "MACD线从下向上穿越信号线时买入，从上向下穿越时卖出。"
        }
        
        st.info(strategy_descriptions[strategy_type])
        
        # 回测统计
        st.markdown("---")
        st.markdown("#### 📊 回测统计")
        st.write("运行回测后显示统计信息")

    # 运行回测按钮
    st.markdown("---")
    run_col1, run_col2, run_col3 = st.columns([1, 2, 1])

    with run_col2:
        if st.button("🚀 运行回测", type="primary", use_container_width=True):
            with st.spinner("正在获取数据并运行回测..."):
                try:
                    # 1. 获取股票数据
                    # 标准化股票代码格式
                    # 处理A股代码 - AkShare使用纯数字代码
                    ak_code = stock_code
                    if '.' in stock_code:
                        ak_code = stock_code.split('.')[0]
                    
                    # 使用AkShare下载数据
                    data = ak.stock_zh_a_hist(
                        symbol=ak_code,
                        period="daily",
                        start_date=backtest_start.strftime("%Y%m%d"),
                        end_date=backtest_end.strftime("%Y%m%d"),
                        adjust="qfq"
                    )
                    
                    if data.empty:
                        st.error(f"❌ 无法获取 {stock_code} 的数据，请检查股票代码是否正确")
                        return
                    
                    # 转换为DataFrame
                    df = pd.DataFrame({
                        'open': data['开盘'],
                        'high': data['最高'],
                        'low': data['最低'],
                        'close': data['收盘'],
                        'volume': data['成交量']
                    })
                    
                    st.info(f"✅ 成功获取 {stock_code} 的 {len(df)} 条数据")
                    
                    # 2. 根据策略类型计算信号
                    if strategy_type == "双均线交叉":
                        df = calculate_ma_crossover(df, short_window, long_window)
                    elif strategy_type == "RSI策略":
                        df = calculate_rsi_strategy(df, rsi_period, rsi_oversold, rsi_overbought)
                    elif strategy_type == "布林带策略":
                        df = calculate_bollinger_strategy(df, bb_period, bb_std)
                    else:  # MACD策略
                        df = calculate_macd_strategy(df, macd_fast, macd_slow, macd_signal)
                    
                    # 3. 运行回测
                    results = run_backtest_simulation(
                        df, 
                        initial_capital, 
                        commission_rate / 100, 
                        slippage / 100
                    )
                    
                    # 保存结果
                    st.session_state.backtest_results = results
                    st.session_state.backtest_config = {
                        'strategy': strategy_type,
                        'params': strategy_params,
                        'stock': stock_code,
                        'start': backtest_start,
                        'end': backtest_end
                    }
                    
                    st.success("✅ 回测完成！")
                    
                except Exception as e:
                    st.error(f"❌ 回测失败: {str(e)}")
                    import traceback
                    st.text(traceback.format_exc())

    # 显示回测结果
    if st.session_state.backtest_results is not None:
        results = st.session_state.backtest_results
        config = st.session_state.backtest_config
        
        st.markdown("---")
        st.subheader("📊 回测结果")
        
        # 关键指标
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.metric("总收益率", f"{results['total_return']:.2%}", 
                     delta=f"¥{results['final_value'] - results['initial_capital']:,.0f}")
        with col_res2:
            st.metric("年化收益率", f"{results['annual_return']:.2%}")
        with col_res3:
            st.metric("最大回撤", f"{results['max_drawdown']:.2%}")
        with col_res4:
            st.metric("夏普比率", f"{results['sharpe_ratio']:.2f}")
        
        # 更多指标
        col_res5, col_res6, col_res7, col_res8 = st.columns(4)
        
        with col_res5:
            st.metric("初始资金", f"¥{results['initial_capital']:,.0f}")
        with col_res6:
            st.metric("最终价值", f"¥{results['final_value']:,.0f}")
        with col_res7:
            st.metric("交易次数", results['total_trades'])
        with col_res8:
            st.metric("胜率", f"{results['win_rate']:.1%}")
        
        # 可视化
        st.markdown("---")
        
        # 创建标签页
        tab1, tab2, tab3 = st.tabs(["📈 收益曲线", "📉 交易信号", "📋 交易记录"])
        
        with tab1:
            # 收益曲线图
            fig = go.Figure()
            
            # 添加资产曲线
            fig.add_trace(go.Scatter(
                x=results['portfolio_history']['date'],
                y=results['portfolio_history']['value'],
                mode='lines',
                name='资产价值',
                line=dict(color='#3b82f6', width=2)
            ))
            
            # 添加买入标记
            if len(results['buy_signals']) > 0:
                buy_df = pd.DataFrame(results['buy_signals'])
                fig.add_trace(go.Scatter(
                    x=buy_df['date'],
                    y=buy_df['price'],
                    mode='markers',
                    name='买入',
                    marker=dict(color='green', symbol='triangle-up', size=10)
                ))
            
            # 添加卖出标记
            if len(results['sell_signals']) > 0:
                sell_df = pd.DataFrame(results['sell_signals'])
                fig.add_trace(go.Scatter(
                    x=sell_df['date'],
                    y=sell_df['price'],
                    mode='markers',
                    name='卖出',
                    marker=dict(color='red', symbol='triangle-down', size=10)
                ))
            
            fig.update_layout(
                title=f"{config['stock']} - {config['strategy']} 策略资产曲线",
                xaxis_title="日期",
                yaxis_title="资产价值 (¥)",
                template="plotly_white",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # 价格与信号图
            fig2 = go.Figure()
            
            # 添加价格线
            price_df = results['price_history']
            # 找到日期列
            date_col = None
            for col in price_df.columns:
                if '日期' in col or 'date' in col.lower() or col == 'index':
                    date_col = col
                    break
            
            x_data = price_df[date_col] if date_col else price_df.index
            close_col = 'close' if 'close' in price_df.columns else '收盘'
            
            fig2.add_trace(go.Scatter(
                x=x_data,
                y=price_df[close_col],
                mode='lines',
                name='收盘价',
                line=dict(color='#1f77b4', width=1.5)
            ))
            
            # 添加均线（如果有）
            if 'ma_short' in price_df.columns:
                fig2.add_trace(go.Scatter(
                    x=x_data,
                    y=price_df['ma_short'],
                    mode='lines',
                    name='短期均线',
                    line=dict(color='orange', width=1)
                ))
            
            if 'ma_long' in price_df.columns:
                fig2.add_trace(go.Scatter(
                    x=x_data,
                    y=price_df['ma_long'],
                    mode='lines',
                    name='长期均线',
                    line=dict(color='purple', width=1)
                ))
            
            # 添加买入/卖出标记
            if len(results['buy_signals']) > 0:
                buy_df = pd.DataFrame(results['buy_signals'])
                fig2.add_trace(go.Scatter(
                    x=buy_df['date'],
                    y=buy_df['price'],
                    mode='markers',
                    name='买入信号',
                    marker=dict(color='green', symbol='triangle-up', size=12)
                ))
            
            if len(results['sell_signals']) > 0:
                sell_df = pd.DataFrame(results['sell_signals'])
                fig2.add_trace(go.Scatter(
                    x=sell_df['date'],
                    y=sell_df['price'],
                    mode='markers',
                    name='卖出信号',
                    marker=dict(color='red', symbol='triangle-down', size=12)
                ))
            
            fig2.update_layout(
                title=f"{config['stock']} 价格与交易信号",
                xaxis_title="日期",
                yaxis_title="价格 (¥)",
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            # 交易记录
            if results['trades']:
                trades_df = pd.DataFrame(results['trades'])
                st.dataframe(trades_df, use_container_width=True)
                
                # 导出交易记录
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    label="📥 导出交易记录",
                    data=csv,
                    file_name=f"trades_{config['stock']}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("暂无交易记录")

    # 使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ### 策略回测使用指南
        
        #### 1. 选择策略
        - **双均线交叉**: 短期均线上穿长期均线买入，下穿卖出
        - **RSI策略**: RSI超卖买入，超买卖出
        - **布林带策略**: 价格跌破下轨买入，突破上轨卖出
        - **MACD策略**: MACD金叉买入，死叉卖出
        
        #### 2. 配置参数
        - 根据所选策略调整相应参数
        - 参数会影响交易频率和风险
        
        #### 3. 设置回测参数
        - 初始资金: 回测用的起始资金
        - 佣金费率: 每次交易的手续费
        - 滑点: 价格滑动的比例
        
        #### 4. 查看结果
        - 收益率: 总收益和年化收益
        - 风险指标: 最大回撤、夏普比率
        - 交易记录: 每次买入卖出的详细信息
        
        #### 注意事项
        - 历史回测不代表未来收益
        - 请综合考虑多种指标评估策略
        - 建议使用多个时间段进行测试
        """)

# 策略计算函数
def calculate_ma_crossover(df, short_window, long_window):
    """计算双均线交叉信号"""
    df = df.copy()
    df['ma_short'] = df['close'].rolling(short_window).mean()
    df['ma_long'] = df['close'].rolling(long_window).mean()
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1
    df.loc[df['ma_short'] <= df['ma_long'], 'signal'] = -1
    
    # 交易信号
    df['position'] = df['signal'].diff()
    
    return df

def calculate_rsi_strategy(df, period, oversold, overbought):
    """计算RSI策略信号"""
    import numpy as np
    df = df.copy()
    
    # 计算RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['rsi'] < oversold, 'signal'] = 1  # 超卖买入
    df.loc[df['rsi'] > overbought, 'signal'] = -1  # 超买卖出
    
    # 保持仓位
    df['signal'] = df['signal'].replace(0, np.nan)
    df['signal'] = df['signal'].ffill().fillna(0)
    
    # 交易信号
    df['position'] = df['signal'].diff()
    
    return df

def calculate_bollinger_strategy(df, period, std_dev):
    """计算布林带策略信号"""
    import numpy as np
    df = df.copy()
    
    # 计算布林带
    df['bb_middle'] = df['close'].rolling(period).mean()
    df['bb_std'] = df['close'].rolling(period).std()
    df['bb_upper'] = df['bb_middle'] + std_dev * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - std_dev * df['bb_std']
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['close'] < df['bb_lower'], 'signal'] = 1  # 跌破下轨买入
    df.loc[df['close'] > df['bb_upper'], 'signal'] = -1  # 突破上轨卖出
    
    # 保持仓位
    df['signal'] = df['signal'].replace(0, np.nan)
    df['signal'] = df['signal'].ffill().fillna(0)
    
    # 交易信号
    df['position'] = df['signal'].diff()
    
    return df

def calculate_macd_strategy(df, fast, slow, signal):
    """计算MACD策略信号"""
    df = df.copy()
    
    # 计算MACD
    exp1 = df['close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['signal_line'] = df['macd'].ewm(span=signal, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['signal_line']
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # 金叉买入
    df.loc[df['macd'] <= df['signal_line'], 'signal'] = -1  # 死叉卖出
    
    # 交易信号
    df['position'] = df['signal'].diff()
    
    return df

def run_backtest_simulation(df, initial_capital, commission_rate, slippage):
    """运行回测模拟"""
    import numpy as np
    import pandas as pd
    from datetime import datetime
    
    cash = initial_capital
    position = 0  # 持股数量
    shares = 0
    
    trades = []
    buy_signals = []
    sell_signals = []
    portfolio_history = []
    wins = 0
    losses = 0
    
    # 处理日期格式 - 更健壮的处理
    try:
        # 首先检查索引的第一个元素
        first_idx = df.index[0]
        
        if df.index.dtype == 'datetime64[ns]':
            # 已经是datetime格式
            pass
        elif isinstance(first_idx, (int, np.integer)) and first_idx > 10000000:
            # 看起来像YYYYMMDD格式的整数
            df.index = pd.to_datetime(df.index, format='%Y%m%d')
        elif isinstance(first_idx, str):
            # 字符串格式，尝试自动解析
            df.index = pd.to_datetime(df.index, errors='coerce')
        elif hasattr(first_idx, 'year'):
            # 已经是日期对象
            df.index = pd.to_datetime(df.index)
    except Exception as e:
        # 如果处理失败，直接重置索引
        pass
    
    # 转换为列表进行回测
    df = df.reset_index()
    # 处理列名 - AkShare返回的是中文列名
    df.columns = df.columns.str.lower()
    
    # 找到日期列
    date_col = None
    for col in df.columns:
        if '日期' in col or 'date' in col.lower() or 'day' in col.lower():
            date_col = col
            break
    
    for i, row in df.iterrows():
        # 获取日期
        if date_col:
            date = row[date_col]
        else:
            date = df.index[i]  # 使用索引作为日期
        
        # 确保日期是datetime对象
        if not isinstance(date, (pd.Timestamp, datetime)):
            try:
                date = pd.to_datetime(date)
            except:
                continue
        
        price = row['close']
        position_signal = row.get('position', 0)
        
        # 买入信号
        if position_signal > 0 and cash > 0:
            # 考虑滑点
            buy_price = price * (1 + slippage)
            # 买入最大可用资金
            max_shares = int(cash / (buy_price * (1 + commission_rate)))
            if max_shares > 0:
                cost = max_shares * buy_price * (1 + commission_rate)
                cash -= cost
                shares = max_shares
                
                trades.append({
                    '日期': date.strftime('%Y-%m-%d'),
                    '操作': '买入',
                    '价格': round(buy_price, 2),
                    '数量': shares,
                    '金额': round(cost, 2)
                })
                buy_signals.append({'date': date, 'price': buy_price})
        
        # 卖出信号
        elif position_signal < 0 and shares > 0:
            # 考虑滑点
            sell_price = price * (1 - slippage)
            revenue = shares * sell_price * (1 - commission_rate)
            
            # 记录胜负
            if len(trades) > 0:
                last_buy = trades[-1]
                if sell_price > last_buy['价格']:
                    wins += 1
                else:
                    losses += 1
            
            trades.append({
                '日期': date.strftime('%Y-%m-%d'),
                '操作': '卖出',
                '价格': round(sell_price, 2),
                '数量': shares,
                '金额': round(revenue, 2)
            })
            sell_signals.append({'date': date, 'price': sell_price})
            
            cash += revenue
            shares = 0
        
        # 计算当前资产价值
        total_value = cash + shares * price
        portfolio_history.append({
            'date': date,
            'cash': cash,
            'shares': shares,
            'value': total_value,
            'price': price
        })
    
    # 最终价值
    if shares > 0:
        final_price = df.iloc[-1]['close']
        final_value = cash + shares * final_price
    else:
        final_value = cash
    
    # 计算指标
    total_return = (final_value - initial_capital) / initial_capital
    days = len(portfolio_history)
    years = days / 252
    annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
    
    # 计算最大回撤
    portfolio_values = [p['value'] for p in portfolio_history]
    max_value = 0
    max_drawdown = 0
    for value in portfolio_values:
        if value > max_value:
            max_value = value
        drawdown = (max_value - value) / max_value if max_value > 0 else 0
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # 计算夏普比率
    returns = []
    for i in range(1, len(portfolio_history)):
        ret = (portfolio_history[i]['value'] - portfolio_history[i-1]['value']) / portfolio_history[i-1]['value']
        returns.append(ret)
    
    if returns:
        avg_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe_ratio = (avg_return * 252) / (std_return * np.sqrt(252)) if std_return > 0 else 0
    else:
        sharpe_ratio = 0
    
    # 胜率
    total_trades = wins + losses
    win_rate = wins / total_trades if total_trades > 0 else 0
    
    # 准备价格历史 - 标准化列名
    price_history = df.copy()
    price_history = price_history.reset_index()
    price_history.columns = price_history.columns.str.lower()
    
    return {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'total_trades': total_trades,
        'win_rate': win_rate,
        'trades': trades,
        'buy_signals': buy_signals,
        'sell_signals': sell_signals,
        'portfolio_history': pd.DataFrame(portfolio_history),
        'price_history': price_history
    }


# 主函数
def main():
    # 显示标题
    show_header()
    
    # 显示侧边栏并获取当前页面
    current_page = show_sidebar()
    
    # 根据选择显示页面内容
    if current_page == "🏠 首页":
        show_home()
    elif current_page == "📥 数据获取":
        # 直接显示数据获取功能
        show_data_acquisition()
    elif current_page == "🧪 策略回测":
        # 直接显示策略回测功能
        show_backtest()
    elif current_page == "📝 公式解析":
        # 直接显示公式解析功能
        show_formula_parser()
    elif current_page == "📊 结果分析":
        # 导入结果分析页面
        try:
            from pages import 结果分析
            结果分析.show()
        except ImportError:
            st.warning("结果分析页面正在开发中...")
            st.info("功能即将上线，敬请期待！")
    elif current_page == "⚙️ 设置":
        # 直接显示系统设置功能
        show_settings()


# 系统设置功能
def show_settings():
    import pandas as pd
    import numpy as np
    from datetime import datetime
    
    st.title("⚙️ 系统设置")
    
    # 页面描述
    st.markdown("""
    <div class="page-description">
        配置系统参数，管理数据源和个性化选项。
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化设置session state
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'theme': '自动',
            'language': '中文',
            'default_capital': 100000,
            'default_commission': 0.03,
            'default_slippage': 0.1,
            'data_refresh_interval': 60,
            'auto_save': True,
            'chart_theme': 'plotly_white'
        }
    
    settings = st.session_state.settings
    
    # 确保theme值正确
    if settings.get('theme') == 'auto':
        settings['theme'] = '自动'
    
    # 创建设置标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 外观", "💰 回测参数", "📡 数据源", "🔧 高级"])
    
    with tab1:
        st.subheader("🎨 外观设置")
        
        # 主题选择
        theme = st.selectbox(
            "主题模式",
            ["自动", "亮色", "暗色"],
            index=["自动", "亮色", "暗色"].index(settings.get('theme', '自动')),
            help="选择应用的主题模式"
        )
        settings['theme'] = theme
        
        # 语言选择
        language = st.selectbox(
            "界面语言",
            ["中文", "English"],
            index=0,
            help="选择界面显示语言"
        )
        settings['language'] = language
        
        # 图表主题
        chart_theme = st.selectbox(
            "图表主题",
            ["plotly_white", "plotly_dark", "ggplot2", "seaborn"],
            index=0,
            help="选择图表的默认主题"
        )
        settings['chart_theme'] = chart_theme
        
        # 显示设置
        st.markdown("#### 显示选项")
        show_indicators = st.checkbox("显示技术指标", value=True)
        show_volume = st.checkbox("显示成交量", value=True)
        show_grid = st.checkbox("显示网格", value=True)
        
    with tab2:
        st.subheader("💰 回测参数默认值")
        
        # 默认初始资金
        default_capital = st.number_input(
            "默认初始资金 (¥)",
            min_value=10000,
            value=settings.get('default_capital', 100000),
            step=10000,
            help="设置回测时的默认初始资金"
        )
        settings['default_capital'] = default_capital
        
        # 默认佣金
        default_commission = st.number_input(
            "默认佣金费率 (%)",
            min_value=0.01,
            max_value=0.5,
            value=settings.get('default_commission', 0.03),
            step=0.01,
            help="设置默认佣金费率"
        )
        settings['default_commission'] = default_commission
        
        # 默认滑点
        default_slippage = st.number_input(
            "默认滑点 (%)",
            min_value=0.0,
            max_value=1.0,
            value=settings.get('default_slippage', 0.1),
            step=0.05,
            help="设置默认滑点比例"
        )
        settings['default_slippage'] = default_slippage
        
        # 复权类型
        adjust_type = st.selectbox(
            "默认复权类型",
            ["前复权 (qfq)", "后复权 (hfq)", "不复权"],
            index=0,
            help="设置默认的复权类型"
        )
        
        # 显示当前设置
        st.markdown("---")
        st.markdown("#### 当前设置预览")
        
        col_prev1, col_prev2 = st.columns(2)
        with col_prev1:
            st.metric("默认初始资金", f"¥{default_capital:,.0f}")
        with col_prev2:
            st.metric("默认佣金", f"{default_commission}%")
        
    with tab3:
        st.subheader("📡 数据源设置")
        
        # 数据源选择
        st.markdown("#### 数据源配置")
        
        data_source = st.selectbox(
            "默认数据源",
            ["akshare"],
            index=0,
            help="选择默认的数据源"
        )
        
        # 数据刷新间隔
        data_refresh = st.slider(
            "数据刷新间隔 (秒)",
            min_value=30,
            max_value=300,
            value=settings.get('data_refresh_interval', 60),
            step=30,
            help="设置数据自动刷新的间隔"
        )
        settings['data_refresh_interval'] = data_refresh
        
        # 数据缓存
        st.markdown("#### 数据缓存")
        enable_cache = st.checkbox("启用数据缓存", value=settings.get('auto_save', True))
        cache_size = st.slider(
            "缓存大小 (MB)",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
            help="设置数据缓存的最大大小"
        )
        
        # 数据保存
        st.markdown("#### 数据保存")
        auto_save = st.checkbox("自动保存回测结果", value=settings.get('auto_save', True))
        settings['auto_save'] = auto_save
        
        # 导出路径
        export_path = st.text_input(
            "默认导出路径",
            value="./data/exports",
            help="设置默认的数据导出目录"
        )
        
    with tab4:
        st.subheader("🔧 高级设置")
        
        # 并行计算
        st.markdown("#### 计算设置")
        enable_parallel = st.checkbox("启用并行计算", value=True, help="启用多核CPU加速回测")
        
        # 线程数
        max_workers = st.slider(
            "最大工作线程数",
            min_value=1,
            max_value=8,
            value=4,
            help="设置并行计算的最大线程数"
        )
        
        # 日志级别
        log_level = st.selectbox(
            "日志级别",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,
            help="设置日志输出级别"
        )
        
        # 性能监控
        st.markdown("#### 性能监控")
        enable_profiling = st.checkbox("启用性能分析", value=False, help="启用后会在回测时记录性能数据")
        show_warnings = st.checkbox("显示警告信息", value=True)
        
        # 重置设置
        st.markdown("---")
        st.markdown("#### 危险操作")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            if st.button("🔄 重置为默认", use_container_width=True):
                st.session_state.settings = {
                    'theme': '自动',
                    'language': '中文',
                    'default_capital': 100000,
                    'default_commission': 0.03,
                    'default_slippage': 0.1,
                    'data_refresh_interval': 60,
                    'auto_save': True,
                    'chart_theme': 'plotly_white'
                }
                st.success("✅ 已重置为默认设置")
                st.rerun()
        
        with col_d2:
            if st.button("🗑️ 清除缓存", use_container_width=True):
                # 清除缓存
                st.cache_data.clear()
                st.success("✅ 缓存已清除")
    
    # 保存设置按钮
    st.markdown("---")
    save_col1, save_col2, save_col3 = st.columns([1, 2, 1])
    
    with save_col2:
        if st.button("💾 保存设置", type="primary", use_container_width=True):
            # 保存设置到session state
            st.session_state.settings = settings
            st.success("✅ 设置已保存！")
            st.balloons()
    
    # 显示当前版本信息
    st.markdown("---")
    st.markdown("""
    <div class="page-footer">
        <small>💡 提示：部分设置需要刷新页面后生效</small>
    </div>
    """, unsafe_allow_html=True)
    
    # 版本信息
    st.markdown("---")
    st.markdown("#### ℹ️ 关于")
    
    col_about1, col_about2, col_about3 = st.columns(3)
    
    with col_about1:
        st.info("**版本**: 1.0.0")
    with col_about2:
        st.info("**构建日期**: 2024-02-15")
    with col_about3:
        st.info("**数据源**: AkShare")
    
    # 技术栈信息
    with st.expander("ℹ️ 技术栈信息"):
        st.markdown("""
        - **后端**: Python 3.12
        - **Web框架**: Streamlit 1.54
        - **数据处理**: Pandas, NumPy
        - **数据可视化**: Plotly
        - **数据源**: AkShare (A股数据)
        """)


# 主函数
def main():
    # 显示标题
    show_header()
    
    # 显示侧边栏并获取当前页面
    current_page = show_sidebar()
    
    # 根据选择显示页面内容
    if current_page == "🏠 首页":
        show_home()
    elif current_page == "📥 数据获取":
        # 直接显示数据获取功能
        show_data_acquisition()
    elif current_page == "🧪 策略回测":
        # 直接显示策略回测功能
        show_backtest()
    elif current_page == "📝 公式解析":
        # 直接显示公式解析功能
        show_formula_parser()
    elif current_page == "📊 结果分析":
        # 直接显示结果分析功能
        show_result_analysis()
    elif current_page == "⚙️ 设置":
        # 直接显示系统设置功能
        show_settings()


# 结果分析功能
def show_result_analysis():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    import plotly.express as px
    
    st.title("📊 结果分析")
    
    # 页面描述
    st.markdown("""
    <div class="page-description">
        对回测结果进行深入分析，包括收益分析、风险评估和交易统计。
    </div>
    """, unsafe_allow_html=True)
    
    # 检查是否有回测结果
    if 'backtest_results' not in st.session_state or st.session_state.backtest_results is None:
        st.warning("暂无回测结果，请先运行策略回测！")
        
        # 引导用户进行回测
        st.markdown("""
        ### 如何进行回测：
        1. 在左侧菜单选择 **🧪 策略回测**
        2. 选择策略类型和参数
        3. 输入股票代码和时间范围
        4. 点击 **运行回测** 按钮
        5. 回测完成后返回结果分析页面
        """)
        return
    
    results = st.session_state.backtest_results
    config = st.session_state.get('backtest_config', {})
    
    # 策略选择和分析配置
    col_sel1, col_sel2 = st.columns([2, 1])
    
    with col_sel1:
        st.markdown("""
        <div class="config-card">
            <h3>🔧 策略选择</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 策略类型选择
        strategy_type = st.selectbox(
            "选择策略类型",
            ["双均线交叉", "RSI策略", "布林带策略", "MACD策略"],
            index=0,
            key="analysis_strategy",
            help="选择要分析的策略类型"
        )
    
    # 策略参数配置
    if strategy_type == "双均线交叉":
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            short_window = st.number_input("短期均线周期", min_value=2, max_value=50, value=5, key="ma_short_analysis")
        with col_p2:
            long_window = st.number_input("长期均线周期", min_value=5, max_value=200, value=20, key="ma_long_analysis")
        strategy_params = {"short_window": short_window, "long_window": long_window}
        strategy_params_str = f"MA({short_window}, {long_window})"
        
    elif strategy_type == "RSI策略":
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            rsi_period = st.number_input("RSI周期", min_value=5, max_value=30, value=14, key="rsi_period_analysis")
        with col_p2:
            rsi_oversold = st.number_input("RSI超卖阈值", min_value=10, max_value=40, value=30, key="rsi_oversold_analysis")
            rsi_overbought = st.number_input("RSI超买阈值", min_value=60, max_value=90, value=70, key="rsi_overbought_analysis")
        strategy_params = {"rsi_period": rsi_period, "rsi_oversold": rsi_oversold, "rsi_overbought": rsi_overbought}
        strategy_params_str = f"RSI({rsi_period}, 超卖{rsi_oversold}, 超买{rsi_overbought})"
        
    elif strategy_type == "布林带策略":
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            bb_period = st.number_input("布林带周期", min_value=10, max_value=50, value=20, key="bb_period_analysis")
        with col_p2:
            bb_std = st.number_input("标准差倍数", min_value=1.0, max_value=3.0, value=2.0, step=0.5, key="bb_std_analysis")
        strategy_params = {"bb_period": bb_period, "bb_std": bb_std}
        strategy_params_str = f"BOLL({bb_period}, {bb_std})"
        
    else:  # MACD策略
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            macd_fast = st.number_input("MACD快线", min_value=5, max_value=20, value=12, key="macd_fast_analysis")
        with col_p2:
            macd_slow = st.number_input("MACD慢线", min_value=15, max_value=40, value=26, key="macd_slow_analysis")
        with col_p3:
            macd_signal = st.number_input("信号线", min_value=5, max_value=15, value=9, key="macd_signal_analysis")
        strategy_params = {"macd_fast": macd_fast, "macd_slow": macd_slow, "macd_signal": macd_signal}
        strategy_params_str = f"MACD({macd_fast}, {macd_slow}, {macd_signal})"
    
    # 显示策略信息
    with col_sel2:
        st.markdown("""
        <div class="status-card">
            <h3>📋 当前策略信息</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"**策略类型**: {strategy_type}")
        st.info(f"**策略参数**: {strategy_params_str}")
    
    # 运行回测按钮
    st.markdown("---")
    run_col1, run_col2, run_col3 = st.columns([1, 2, 1])
    
    with run_col2:
        if st.button("🚀 运行回测并分析", type="primary", use_container_width=True):
            # 需要先有股票数据
            if 'downloaded_data' in st.session_state and st.session_state.downloaded_data is not None:
                with st.spinner("正在运行回测..."):
                    try:
                        # 获取数据
                        df = st.session_state.downloaded_data.copy()
                        
                        # 根据选择的策略计算信号
                        if strategy_type == "双均线交叉":
                            df = calculate_ma_crossover(df, short_window, long_window)
                        elif strategy_type == "RSI策略":
                            df = calculate_rsi_strategy(df, rsi_period, rsi_oversold, rsi_overbought)
                        elif strategy_type == "布林带策略":
                            df = calculate_bollinger_strategy(df, bb_period, bb_std)
                        else:  # MACD策略
                            df = calculate_macd_strategy(df, macd_fast, macd_slow, macd_signal)
                        
                        # 获取回测参数
                        initial_capital = config.get('initial_capital', 100000) if config else 100000
                        commission_rate = 0.0003
                        slippage = 0.001
                        
                        # 运行回测
                        results = run_backtest_simulation(df, initial_capital, commission_rate, slippage)
                        
                        # 保存结果
                        st.session_state.backtest_results = results
                        st.session_state.backtest_config = {
                            'strategy': strategy_type,
                            'params': strategy_params,
                            'stock': config.get('stock', 'N/A') if config else 'N/A',
                            'start': config.get('start', 'N/A') if config else 'N/A',
                            'end': config.get('end', 'N/A') if config else 'N/A',
                            'initial_capital': initial_capital
                        }
                        
                        st.success("✅ 回测完成！")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ 回测失败: {str(e)}")
            else:
                st.warning("请先在「数据获取」页面下载股票数据！")
    
    # 如果没有回测结果，显示提示
    if 'backtest_results' not in st.session_state or st.session_state.backtest_results is None:
        st.warning("请点击上方「运行回测并分析」按钮进行分析")
        st.markdown("""
        ### 如何使用：
        1. 先在「数据获取」页面下载股票数据
        2. 在上方选择策略类型和参数
        3. 点击「运行回测并分析」按钮
        4. 查看收益分析、风险分析等结果
        """)
        return
    
    results = st.session_state.backtest_results
    config = st.session_state.get('backtest_config', {})
    
    # 创建分析标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📈 收益分析", "⚠️ 风险分析", "📋 交易统计", "📊 综合报告"])
    
    with tab1:
        st.subheader("📈 收益分析")
        
        # 收益概览
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总收益率", f"{results.get('total_return', 0)*100:.2f}%")
        with col2:
            st.metric("年化收益率", f"{results.get('annual_return', 0)*100:.2f}%")
        with col3:
            st.metric("绝对收益", f"¥{results.get('final_value', 0) - results.get('initial_capital', 0):,.0f}")
        with col4:
            st.metric("夏普比率", f"{results.get('sharpe_ratio', 0):.2f}")
        
        # 收益率曲线
        if 'portfolio_history' in results and len(results['portfolio_history']) > 0:
            pf_df = pd.DataFrame(results['portfolio_history'])
            
            # 计算收益率
            if 'value' in pf_df.columns:
                pf_df['return'] = pf_df['value'].pct_change() * 100
                pf_df['cumulative_return'] = (pf_df['value'] / pf_df['value'].iloc[0] - 1) * 100
                
                # 收益率曲线图
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=pf_df.index if 'date' not in pf_df.columns else pf_df['date'],
                    y=pf_df['cumulative_return'],
                    mode='lines',
                    name='累计收益率',
                    fill='tozeroy',
                    line=dict(color='#3b82f6', width=2)
                ))
                
                fig.update_layout(
                    title='累计收益率曲线',
                    xaxis_title='时间',
                    yaxis_title='收益率 (%)',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 月度收益统计
                if 'date' in pf_df.columns:
                    try:
                        pf_df['month'] = pd.to_datetime(pf_df['date']).dt.to_period('M')
                        monthly_returns = pf_df.groupby('month')['return'].sum()
                        
                        fig_monthly = px.bar(
                            x=[str(x) for x in monthly_returns.index],
                            y=monthly_returns.values,
                            color=monthly_returns.values,
                            color_continuous_scale='RdYlGn',
                            title='月度收益率',
                            labels={'x': '月份', 'y': '收益率 (%)'}
                        )
                        fig_monthly.update_layout(height=300)
                        st.plotly_chart(fig_monthly, use_container_width=True)
                    except:
                        pass
    
    with tab2:
        st.subheader("⚠️ 风险分析")
        
        # 风险指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            max_dd = results.get('max_drawdown', 0) * 100
            st.metric("最大回撤", f"{max_dd:.2f}%", delta_color="inverse")
        with col2:
            volatility = results.get('volatility', 0) * 100
            st.metric("波动率", f"{volatility:.2f}%")
        with col3:
            calmar = results.get('calmar_ratio', 0)
            st.metric("卡尔玛比率", f"{calmar:.2f}")
        with col4:
            sortino = results.get('sortino_ratio', 0)
            st.metric("索提诺比率", f"{sortino:.2f}")
        
        # 回撤曲线
        if 'portfolio_history' in results and len(results['portfolio_history']) > 0:
            pf_df = pd.DataFrame(results['portfolio_history'])
            
            if 'value' in pf_df.columns:
                # 计算回撤
                pf_df['peak'] = pf_df['value'].cummax()
                pf_df['drawdown'] = (pf_df['value'] - pf_df['peak']) / pf_df['peak'] * 100
                
                fig_dd = go.Figure()
                
                fig_dd.add_trace(go.Scatter(
                    x=pf_df.index if 'date' not in pf_df.columns else pf_df['date'],
                    y=pf_df['drawdown'],
                    mode='lines',
                    name='回撤',
                    fill='tozeroy',
                    line=dict(color='#ef4444', width=2)
                ))
                
                fig_dd.update_layout(
                    title='回撤曲线',
                    xaxis_title='时间',
                    yaxis_title='回撤 (%)',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig_dd, use_container_width=True)
                
                # 回撤统计
                st.markdown("#### 回撤统计")
                dd_stats = {
                    "平均回撤": f"{pf_df['drawdown'].mean():.2f}%",
                    "最大回撤": f"{pf_df['drawdown'].min():.2f}%",
                    "回撤持续天数": (pf_df['drawdown'] < 0).sum()
                }
                
                col_dd1, col_dd2, col_dd3 = st.columns(3)
                with col_dd1:
                    st.metric("平均回撤", dd_stats["平均回撤"])
                with col_dd2:
                    st.metric("最大回撤", dd_stats["最大回撤"], delta_color="inverse")
                with col_dd3:
                    st.metric("回撤天数", dd_stats["回撤持续天数"])
    
    with tab3:
        st.subheader("📋 交易统计")
        
        # 基本统计
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总交易次数", results.get('total_trades', 0))
        with col2:
            st.metric("盈利次数", results.get('winning_trades', 0))
        with col3:
            st.metric("亏损次数", results.get('losing_trades', 0))
        with col4:
            st.metric("胜率", f"{results.get('win_rate', 0)*100:.1f}%")
        
        # 交易详情表格
        if results.get('trades') and len(results['trades']) > 0:
            st.markdown("#### 交易记录")
            
            trades_df = pd.DataFrame(results['trades'])
            
            # 格式化显示
            if '日期' in trades_df.columns:
                st.dataframe(trades_df, use_container_width=True)
                
                # 交易统计
                if '操作' in trades_df.columns:
                    buy_count = len(trades_df[trades_df['操作'] == '买入'])
                    sell_count = len(trades_df[trades_df['操作'] == '卖出'])
                    
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.metric("买入次数", buy_count)
                    with col_t2:
                        st.metric("卖出次数", sell_count)
        else:
            st.info("暂无交易记录")
        
        # 交易信号可视化
        if 'buy_signals' in results and 'sell_signals' in results:
            if len(results['buy_signals']) > 0 or len(results['sell_signals']) > 0:
                st.markdown("#### 交易信号分布")
                
                signal_data = {
                    '类型': ['买入'] * len(results['buy_signals']) + ['卖出'] * len(results['sell_signals']),
                    '数量': [1] * (len(results['buy_signals']) + len(results['sell_signals']))
                }
                
                fig_signals = px.histogram(
                    pd.DataFrame(signal_data),
                    x='类型',
                    title='买卖信号分布',
                    color='类型',
                    color_discrete_map={'买入': 'green', '卖出': 'red'}
                )
                fig_signals.update_layout(height=300)
                st.plotly_chart(fig_signals, use_container_width=True)
    
    with tab4:
        st.subheader("📊 综合报告")
        
        # 策略信息
        st.markdown("#### 策略信息")
        
        strategy_info = {
            "策略类型": strategy_type,
            "策略参数": strategy_params,
            "股票代码": config.get('stock', 'N/A') if config else 'N/A',
            "回测时间": f"{config.get('start', 'N/A')} ~ {config.get('end', 'N/A')}" if config else 'N/A',
            "初始资金": f"¥{results.get('initial_capital', 0):,.0f}"
        }
        
        for key, value in strategy_info.items():
            st.write(f"**{key}**: {value}")
        
        # 核心指标汇总
        st.markdown("#### 核心指标汇总")
        
        metrics_data = {
            '指标': ['总收益率', '年化收益率', '夏普比率', '最大回撤', '胜率', '交易次数'],
            '数值': [
                f"{results.get('total_return', 0)*100:.2f}%",
                f"{results.get('annual_return', 0)*100:.2f}%",
                f"{results.get('sharpe_ratio', 0):.2f}",
                f"{results.get('max_drawdown', 0)*100:.2f}%",
                f"{results.get('win_rate', 0)*100:.1f}%",
                f"{results.get('total_trades', 0)}"
            ],
            '评价': ['越高越好', '越高越好', '越高越好', '越低越好', '越高越好', '适中最好']
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.table(metrics_df)
        
        # 导出报告
        st.markdown("---")
        
        # 生成报告文本
        report_text = f"""
# 策略回测分析报告

## 策略信息
- 策略类型: {config.get('strategy', '未知')}
- 股票代码: {config.get('stock', '未知')}
- 回测时间: {config.get('start', 'N/A')} ~ {config.get('end', 'N/A')}
- 初始资金: ¥{results.get('initial_capital', 0):,.0f}

## 收益指标
- 总收益率: {results.get('total_return', 0)*100:.2f}%
- 年化收益率: {results.get('annual_return', 0)*100:.2f}%
- 最终价值: ¥{results.get('final_value', 0):,.0f}

## 风险指标
- 最大回撤: {results.get('max_drawdown', 0)*100:.2f}%
- 夏普比率: {results.get('sharpe_ratio', 0):.2f}

## 交易统计
- 总交易次数: {results.get('total_trades', 0)}
- 胜率: {results.get('win_rate', 0)*100:.1f}%

---
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.download_button(
                label="📥 导出报告(Markdown)",
                data=report_text,
                file_name=f"backtest_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        
        with col_exp2:
            if results.get('trades') and len(results['trades']) > 0:
                trades_df = pd.DataFrame(results['trades'])
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    label="📥 导出交易记录",
                    data=csv,
                    file_name=f"trades_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    # 使用说明
    with st.expander("📖 指标说明"):
        st.markdown("""
        ### 收益指标
        
        - **总收益率**: 回测期间的总收益百分比
        - **年化收益率**: 折算为年度的收益率
        - **夏普比率**: 风险调整后收益，越高越好
        - **卡尔玛比率**: 年化收益/最大回撤，越高越好
        - **索提诺比率**: 只考虑下行风险的夏普比率
        
        ### 风险指标
        
        - **最大回撤**: 从最高点到最低点的最大跌幅
        - **波动率**: 收益率的标准差，年化处理
        - **回撤持续天数**: 策略处于亏损状态的天数
        
        ### 交易统计
        
        - **胜率**: 盈利交易数/总交易数
        - **盈亏比**: 平均盈利金额/平均亏损金额
        """)


# 公式解析功能
def show_formula_parser():
    import sys
    import os
    import re
    
    # 添加项目根目录到Python路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    st.title("📝 公式解析")
    
    # 页面描述
    st.markdown("""
    <div class="page-description">
        将通达信公式转换为Python代码，支持在线编辑和测试。
    </div>
    """, unsafe_allow_html=True)
    
    # 示例公式
    example_formulas = {
        "双均线金叉": """公式名称: 双均线金叉选股
公式描述: 5日均线上穿20日均线选股公式

参数: N1(5,1,100), N2(20,5,200)

MA5:=MA(CLOSE,N1);
MA20:=MA(CLOSE,N2);

金叉:=CROSS(MA5,MA20);

选股:金叉;""",
        "RSI超卖": """公式名称: RSI超卖选股
公式描述: RSI低于30时选股

参数: N(14,5,30)

RSI值:=RSI(C,N);

选股:RSI值<30;""",
        "成交量突破": """公式名称: 成交量突破
公式描述: 成交量突破20日均量的1.5倍

参数: N(20,5,60)

VOLMA:=MA(VOL,N);

选股:VOL>VOLMA*1.5;""",
        "MACD金叉": """公式名称: MACD金叉选股
公式描述: MACD指标金叉时选股

参数: FAST(12,5,30), SLOW(26,9,50), SIGNAL(9,5,20)

DIF:=EMA(CLOSE,FAST)-EMA(CLOSE,SLOW);
DEA:=EMA(DIF,SIGNAL);
MACD:=(DIF-DEA)*2;

金叉:=CROSS(DIF,DEA);

选股:金叉 AND DIF>DEA;"""
    }
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 公式输入区域
        st.markdown("""
        <div class="config-card">
            <h3>📝 公式输入</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 示例选择
        selected_example = st.selectbox(
            "选择示例公式",
            list(example_formulas.keys()) + ["自定义"],
            help="选择一个示例公式或输入自定义公式"
        )
        
        if selected_example != "自定义":
            default_formula = example_formulas[selected_example]
        else:
            default_formula = ""
        
        # 公式编辑器
        formula_text = st.text_area(
            "通达信公式",
            value=default_formula,
            height=300,
            help="输入通达信公式，支持MA、EMA、RSI、MACD等技术指标"
        )
        
        # 解析按钮
        if st.button("🔄 解析公式", type="primary", use_container_width=True):
            if formula_text.strip():
                try:
                    # 简单解析公式
                    result = parse_tdx_formula(formula_text)
                    st.session_state.formula_result = result
                    st.success("✅ 公式解析成功！")
                except Exception as e:
                    st.error(f"❌ 公式解析失败: {str(e)}")
            else:
                st.warning("请输入公式内容")

    with col2:
        # 解析结果区域
        st.markdown("""
        <div class="status-card">
            <h3>📋 解析结果</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if 'formula_result' in st.session_state and st.session_state.formula_result:
            result = st.session_state.formula_result
            
            # 显示公式信息
            st.markdown("#### 公式信息")
            st.info(f"**名称**: {result.get('name', '未命名')}")
            st.info(f"**描述**: {result.get('description', '无')}")
            
            # 显示参数
            if result.get('params'):
                st.markdown("#### 参数")
                for param in result['params']:
                    st.write(f"• {param['name']}: 默认值={param['default']}, 范围=[{param['min']}, {param['max']}]")
            
            # 显示变量
            if result.get('variables'):
                st.markdown("#### 变量")
                for var_name, var_expr in result['variables'].items():
                    st.code(f"{var_name} = {var_expr}", language=None)
        else:
            st.info("解析公式后显示结果")

    # 显示生成的Python代码
    if 'formula_result' in st.session_state and st.session_state.formula_result:
        result = st.session_state.formula_result
        
        st.markdown("---")
        st.subheader("🐍 生成的Python代码")
        
        # 生成Python代码
        python_code = generate_python_code(result)
        
        # 代码显示
        st.code(python_code, language="python")
        
        # 复制按钮
        col_copy1, col_copy2 = st.columns([1, 4])
        with col_copy1:
            st.button("📋 复制代码", use_container_width=True)
        
        # 保存按钮
        with col_copy2:
            st.download_button(
                label="💾 下载代码",
                data=python_code,
                file_name="strategy.py",
                mime="text/x-python"
            )

    # 使用说明
    with st.expander("📖 公式语法说明"):
        st.markdown("""
        ### 通达信公式语法
        
        #### 基本格式
        ```
        公式名称: xxx
        公式描述: xxx
        
        参数: N1(默认值,最小值,最大值), N2(默认值,最小值,最大值)
        
        变量1:=表达式;
        变量2:=表达式;
        
        输出:表达式;
        ```
        
        #### 支持的函数
        - **MA(CLOSE, N)**: 简单移动平均
        - **EMA(CLOSE, N)**: 指数移动平均
        - **RSI(CLOSE, N)**: RSI指标
        - **MACD**: MACD指标
        - **CROSS(A, B)**: A上穿B
        - **REF(X, N)**: N周期前的X值
        - **HHV(X, N)**: N周期内X的最大值
        - **LLV(X, N)**: N周期内X的最小值
        
        #### 示例
        ```
        公式名称: 双均线金叉
        
        MA5:=MA(CLOSE,5);
        MA20:=MA(CLOSE,20);
        
        金叉:=CROSS(MA5,MA20);
        
        选股:金叉;
        ```
        """)


def parse_tdx_formula(formula_text: str) -> dict:
    """简单解析通达信公式"""
    import re
    
    result = {
        'name': '未命名',
        'description': '',
        'params': [],
        'variables': {},
        'outputs': []
    }
    
    lines = formula_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 解析公式名称
        if line.startswith('公式名称:'):
            result['name'] = line.replace('公式名称:', '').strip()
        
        # 解析公式描述
        elif line.startswith('公式描述:'):
            result['description'] = line.replace('公式描述:', '').strip()
        
        # 解析参数
        elif line.startswith('参数:'):
            params_str = line.replace('参数:', '').strip()
            # 匹配参数格式: N1(5,1,100), N2(20,5,200)
            param_pattern = r'(\w+)\((\d+\.?\d*),(\d+\.?\d*),(\d+\.?\d*)\)'
            matches = re.findall(param_pattern, params_str)
            for match in matches:
                result['params'].append({
                    'name': match[0],
                    'default': float(match[1]),
                    'min': float(match[2]),
                    'max': float(match[3])
                })
        
        # 解析变量定义
        elif ':=' in line:
            var_part = line.split(':=')
            if len(var_part) == 2:
                var_name = var_part[0].strip()
                var_expr = var_part[1].rstrip(';').strip()
                result['variables'][var_name] = var_expr
        
        # 解析输出条件
        elif ':' in line and not line.startswith('参数'):
            out_part = line.split(':')
            if len(out_part) == 2:
                out_name = out_part[0].strip()
                out_expr = out_part[1].rstrip(';').strip()
                result['outputs'].append({
                    'name': out_name,
                    'expression': out_expr
                })
    
    return result


def generate_python_code(result: dict) -> str:
    """生成Python代码"""
    name = result.get('name', 'Strategy')
    description = result.get('description', '')
    params = result.get('params', [])
    variables = result.get('variables', {})
    outputs = result.get('outputs', [])
    
    # 生成参数默认值
    param_strs = []
    for p in params:
        param_strs.append(f"{p['name']}: float = {p['default']}")
    
    # 生成代码
    code = f'''"""
{name}
{description}
自动生成的策略代码
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class {name.replace(' ', '').replace('选股', '')}Strategy:
    """{name}策略"""
    
    def __init__(self{', ' + ', '.join(param_strs) if param_strs else ''}):
        """初始化策略参数"""
{chr(10).join([f'        self.{p["name"]} = {p["name"]}' for p in params]) if params else '        pass'}
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        data = data.copy()
        close = data['close']
        
        # 计算中间变量
{chr(10).join([f'        # {var_name}: {var_expr}' for var_name, var_expr in variables.items()])}
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        data = self.calculate_indicators(data)
        
        # 生成信号
{chr(10).join([f'        # {out["name"]}: {out["expression"]}' for out in outputs])}
        
        data['signal'] = 0
        data['position'] = data['signal'].diff()
        
        return data


# 使用示例
if __name__ == "__main__":
    # 创建策略实例
    strategy = {name.replace(' ', '').replace('选股', '')}Strategy()
    
    # 假设已有数据 data
    # signals = strategy.generate_signals(data)
'''
    
    return code


# 运行应用
if __name__ == "__main__":
    main()