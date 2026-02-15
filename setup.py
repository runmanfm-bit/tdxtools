#!/usr/bin/env python3
"""
通达信选股工具安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tdxtools",
    version="0.1.0",
    author="通达信选股工具开发团队",
    author_email="",
    description="通达信选股成功率测试工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "tushare>=1.2.89",
        "akshare>=1.12.0",
        "baostock>=0.8.80",
        "backtrader>=1.9.78.123",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "talib>=0.4.0",  # TA-Lib技术分析库
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "jupyter>=1.0.0",
        ],
        "web": [
            "streamlit>=1.28.0",
            "plotly>=5.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tdxtools=tdxtools.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tdxtools": ["config/*.yaml", "data/*.csv", "examples/*.py"],
    },
)