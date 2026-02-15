#!/bin/bash
# 启动通达信选股工具Web应用的脚本

cd /home/runman/pworkspace/tdxtools
source venv/bin/activate

# 跳过Streamlit邮箱输入并启动应用
cd web
echo "" | streamlit run app.py --server.port 8501 --server.address 0.0.0.0