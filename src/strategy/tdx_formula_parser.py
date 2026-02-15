"""
通达信公式解析器
解析通达信选股公式并转换为Python可执行的策略
"""

import re
import ast
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class TDXFunction:
    """通达信函数定义"""
    
    def __init__(self, name: str, params: List[str], body: str):
        self.name = name
        self.params = params
        self.body = body
        
    def __repr__(self):
        return f"TDXFunction({self.name}, params={self.params})"


class TDXFormulaParser:
    """通达信公式解析器"""
    
    # 通达信内置函数映射到Python
    FUNCTION_MAP = {
        # 数学函数
        'ABS': 'abs',
        'MAX': 'max',
        'MIN': 'min',
        'POW': 'pow',
        'SQRT': 'sqrt',
        'LN': 'np.log',
        'LOG': 'np.log10',
        'EXP': 'np.exp',
        
        # 统计函数
        'MA': 'ta.MA',  # 移动平均
        'EMA': 'ta.EMA',  # 指数移动平均
        'SMA': 'ta.SMA',  # 简单移动平均
        'HHV': 'ta.MAX',  # 最高值
        'LLV': 'ta.MIN',  # 最低值
        'SUM': 'ta.SUM',  # 求和
        'COUNT': 'ta.COUNT',  # 计数
        'REF': 'ta.REF',  # 引用前N周期
        'CROSS': 'ta.CROSS',  # 交叉函数
        
        # 技术指标
        'MACD': 'ta.MACD',
        'KDJ': 'ta.STOCH',
        'RSI': 'ta.RSI',
        'BOLL': 'ta.BBANDS',
        'CCI': 'ta.CCI',
        'WR': 'ta.WILLR',
        
        # 逻辑函数
        'IF': 'np.where',
        'AND': 'np.logical_and',
        'OR': 'np.logical_or',
        'NOT': 'np.logical_not',
        
        # 价格数据
        'CLOSE': 'close',
        'OPEN': 'open',
        'HIGH': 'high',
        'LOW': 'low',
        'VOLUME': 'volume',
        'AMOUNT': 'amount',
        
        # 其他
        'BARSLAST': 'ta.BARSLAST',  # 上一次条件成立到当前的周期数
        'BARSCOUNT': 'ta.BARSCOUNT',  # 有效数据周期数
    }
    
    def __init__(self):
        self.functions: Dict[str, TDXFunction] = {}
        self.variables: Dict[str, Any] = {}
        
    def parse_formula(self, formula_text: str) -> Dict:
        """
        解析通达信公式文本
        
        Args:
            formula_text: 通达信公式文本
            
        Returns:
            解析后的公式结构
        """
        logger.info("开始解析通达信公式")
        
        # 清理公式文本
        cleaned_text = self._clean_formula_text(formula_text)
        
        # 提取公式信息
        formula_info = self._extract_formula_info(cleaned_text)
        
        # 解析变量定义
        variables = self._parse_variables(cleaned_text)
        
        # 解析输出条件
        output_conditions = self._parse_output_conditions(cleaned_text)
        
        # 转换为Python代码
        python_code = self._convert_to_python(cleaned_text, formula_info, variables, output_conditions)
        
        result = {
            'formula_info': formula_info,
            'variables': variables,
            'output_conditions': output_conditions,
            'python_code': python_code,
            'original_text': formula_text,
            'cleaned_text': cleaned_text
        }
        
        logger.info(f"公式解析完成: {formula_info.get('name', '未命名')}")
        return result
    
    def _clean_formula_text(self, text: str) -> str:
        """清理公式文本"""
        # 移除注释
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 移除行尾注释
            line = line.split('//')[0].strip()
            if line:
                cleaned_lines.append(line)
                
        # 合并为单行（简化处理）
        cleaned_text = ' '.join(cleaned_lines)
        
        # 移除多余空格
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        return cleaned_text
    
    def _extract_formula_info(self, text: str) -> Dict:
        """提取公式基本信息"""
        info = {
            'name': '未命名公式',
            'description': '',
            'params': []
        }
        
        # 尝试提取公式名称（通达信公式通常以特定格式开始）
        name_match = re.search(r'公式名称[:：]\s*([^\s;]+)', text)
        if name_match:
            info['name'] = name_match.group(1)
            
        # 提取描述
        desc_match = re.search(r'公式描述[:：]\s*([^;]+)', text)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
            
        # 提取参数（简化处理）
        param_matches = re.finditer(r'参数[:：]\s*([^;]+)', text)
        for match in param_matches:
            params_text = match.group(1)
            # 解析参数定义，如 "N1(5,1,100)" 表示参数N1，默认值5，最小值1，最大值100
            param_defs = re.finditer(r'(\w+)\(([^)]+)\)', params_text)
            for param_match in param_defs:
                param_name = param_match.group(1)
                param_values = param_match.group(2).split(',')
                
                param_info = {
                    'name': param_name,
                    'default': float(param_values[0]) if param_values[0].replace('.', '').isdigit() else param_values[0],
                    'min': float(param_values[1]) if len(param_values) > 1 and param_values[1].replace('.', '').isdigit() else None,
                    'max': float(param_values[2]) if len(param_values) > 2 and param_values[2].replace('.', '').isdigit() else None
                }
                info['params'].append(param_info)
                
        return info
    
    def _parse_variables(self, text: str) -> Dict[str, str]:
        """解析变量定义"""
        variables = {}
        
        # 查找变量赋值语句，如 "MA5:=MA(CLOSE,5);"
        var_pattern = r'(\w+)\s*:=\s*([^;]+);'
        matches = re.finditer(var_pattern, text)
        
        for match in matches:
            var_name = match.group(1)
            var_expr = match.group(2).strip()
            variables[var_name] = var_expr
            
        return variables
    
    def _parse_output_conditions(self, text: str) -> List[Dict]:
        """解析输出条件"""
        conditions = []
        
        # 查找输出语句，如 "选股:条件表达式;"
        output_pattern = r'选股\s*[:：]\s*([^;]+);'
        matches = re.finditer(output_pattern, text)
        
        for match in matches:
            condition_expr = match.group(1).strip()
            conditions.append({
                'expression': condition_expr,
                'type': 'selection'  # 选股条件
            })
            
        # 查找买入卖出条件
        buy_pattern = r'买入\s*[:：]\s*([^;]+);'
        sell_pattern = r'卖出\s*[:：]\s*([^;]+);'
        
        for match in re.finditer(buy_pattern, text):
            conditions.append({
                'expression': match.group(1).strip(),
                'type': 'buy'
            })
            
        for match in re.finditer(sell_pattern, text):
            conditions.append({
                'expression': match.group(1).strip(),
                'type': 'sell'
            })
            
        return conditions
    
    def _convert_to_python(self, text: str, formula_info: Dict, variables: Dict, conditions: List[Dict]) -> str:
        """转换为Python代码"""
        python_lines = []
        
        # 添加导入语句
        python_lines.append("import numpy as np")
        python_lines.append("import pandas as pd")
        python_lines.append("import talib as ta")
        python_lines.append("")
        
        # 添加函数定义
        func_name = formula_info['name'].replace(' ', '_').replace('-', '_')
        python_lines.append(f"def {func_name}(data, **params):")
        python_lines.append('    """')
        python_lines.append(f'    {formula_info.get("description", "通达信公式转换")}')
        python_lines.append('    """')
        python_lines.append('    ')
        python_lines.append('    # 提取价格数据')
        python_lines.append('    close = data["close"].values')
        python_lines.append('    open = data["open"].values')
        python_lines.append('    high = data["high"].values')
        python_lines.append('    low = data["low"].values')
        python_lines.append('    volume = data["volume"].values')
        python_lines.append('    ')
        
        # 设置参数默认值
        if formula_info['params']:
            python_lines.append('    # 设置参数')
            for param in formula_info['params']:
                default = param['default']
                python_lines.append(f'    {param["name"]} = params.get("{param["name"]}", {default})')
            python_lines.append('    ')
        
        # 转换变量定义
        if variables:
            python_lines.append('    # 计算中间变量')
            for var_name, var_expr in variables.items():
                py_expr = self._convert_expression(var_expr)
                python_lines.append(f'    {var_name} = {py_expr}')
            python_lines.append('    ')
        
        # 转换输出条件
        if conditions:
            python_lines.append('    # 计算信号')
            for i, condition in enumerate(conditions):
                py_expr = self._convert_expression(condition['expression'])
                signal_name = f'signal_{condition["type"]}_{i}'
                python_lines.append(f'    {signal_name} = {py_expr}')
            python_lines.append('    ')
            
            # 合并信号
            python_lines.append('    # 合并所有信号')
            python_lines.append('    signals = pd.DataFrame(index=data.index)')
            for i, condition in enumerate(conditions):
                signal_name = f'signal_{condition["type"]}_{i}'
                python_lines.append(f'    signals["{condition["type"]}_{i}"] = {signal_name}')
            python_lines.append('    ')
            
            # 生成最终信号
            python_lines.append('    # 生成最终选股信号（简化处理）')
            python_lines.append('    if "selection" in signals.columns:')
            python_lines.append('        final_signal = signals["selection_0"]')
            python_lines.append('    else:')
            python_lines.append('        final_signal = np.zeros(len(data))')
            python_lines.append('    ')
            python_lines.append('    return final_signal, signals')
        else:
            python_lines.append('    # 没有输出条件，返回空信号')
            python_lines.append('    signals = pd.DataFrame(index=data.index)')
            python_lines.append('    final_signal = np.zeros(len(data))')
            python_lines.append('    return final_signal, signals')
        
        return '\n'.join(python_lines)
    
    def _convert_expression(self, expr: str) -> str:
        """转换表达式为Python语法"""
        # 替换通达信函数为Python函数
        converted = expr
        
        # 首先替换内置变量
        for tdx_func, py_func in self.FUNCTION_MAP.items():
            # 使用正则表达式确保只替换函数调用，不替换变量名的一部分
            pattern = r'\b' + re.escape(tdx_func) + r'\b'
            converted = re.sub(pattern, py_func, converted)
        
        # 替换逻辑运算符
        converted = converted.replace('AND', '&').replace('OR', '|').replace('NOT', '~')
        
        # 替换比较运算符
        converted = converted.replace('>', '>').replace('<', '<')
        converted = converted.replace('>=', '>=').replace('<=', '<=')
        converted = converted.replace('=', '==').replace('<>', '!=')
        
        # 处理通达信特有的语法
        # 例如：CROSS(A,B) 表示A上穿B
        # 这里简化处理，实际需要更复杂的转换
        
        return converted
    
    def generate_strategy_class(self, formula_text: str) -> str:
        """
        生成策略类代码
        
        Args:
            formula_text: 通达信公式文本
            
        Returns:
            策略类Python代码
        """
        parsed = self.parse_formula(formula_text)
        
        # 生成策略类
        class_name = parsed['formula_info']['name'].replace(' ', '_').replace('-', '_') + 'Strategy'
        
        code = f'''"""
{parsed['formula_info']['name']}策略
{parsed['formula_info'].get('description', '')}
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

from src.backtest.backtest_engine import Strategy


class {class_name}(Strategy):
    """{parsed['formula_info']['name']}策略"""
    
    def __init__(self{self._generate_init_params(parsed)}):
        """初始化策略"""
        super().__init__("{parsed['formula_info']['name']}")
        {self._generate_init_assignments(parsed)}
        
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        data = data.copy()
        
        # 这里添加指标计算逻辑
        # 基于解析的公式实现
        
        return data
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        data = self.calculate_indicators(data)
        
        # 初始化信号列
        data['signal'] = 0
        
        # 这里添加信号生成逻辑
        # 基于解析的输出条件实现
        
        # 信号变化点
        data['positions'] = data['signal'].diff()
        
        return data
'''
        return code
    
    def _generate_init_params(self, parsed: Dict) -> str:
        """生成初始化参数"""
        params = parsed['formula_info']['params']
        if not params:
            return ''
            
        param_strs = []
        for param in params:
            default = param['default']
            param_strs.append(f"{param['name']}: float = {default}")
            
        return ', ' + ', '.join(param_strs)
    
    def _generate_init_assignments(self, parsed: Dict) -> str:
        """生成初始化赋值语句"""
        params = parsed['formula_info']['params']
        if not params:
            return 'pass'
            
        assignments = []
        for param in params:
            assignments.append(f"self.{param['name']} = {param['name']}")
            
        return '\n        '.join(assignments)


# 示例通达信公式
EXAMPLE_FORMULA = """
公式名称: 双均线金叉选股
公式描述: 5日均线上穿20日均线选股公式

参数: N1(5,1,100), N2(20,5,200)

MA5:=MA(CLOSE,N1);
MA20:=MA(CLOSE,N2);

金叉:=CROSS(MA5,MA20);

选股:金叉;
"""


if __name__ == "__main__":
    # 测试解析器
    parser = TDXFormulaParser()
    
    print("测试通达信公式解析器")
    print("="*60)
    
    # 解析示例公式
    result = parser.parse_formula(EXAMPLE_FORMULA)
    
    print(f"公式名称: {result['formula_info']['name']}")
    print(f"公式描述: {result['formula_info']['description']}")
    print(f"参数: {result['formula_info']['params']}")
    print(f"变量数量: {len(result['variables'])}")
    print(f"输出条件: {len(result['output_conditions'])}")
    
    print("\n生成的Python代码:")
    print("="*60)
    print(result['python_code'])
    
    print("\n生成的策略类:")
    print("="*60)
    strategy_code = parser.generate_strategy_class(EXAMPLE_FORMULA)
    print(strategy_code)