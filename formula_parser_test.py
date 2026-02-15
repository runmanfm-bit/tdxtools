#!/usr/bin/env python3
"""
测试通达信公式解析器
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("通达信公式解析器测试")
print("="*60)

try:
    from src.strategy.tdx_formula_parser import TDXFormulaParser, EXAMPLE_FORMULA
    
    # 创建解析器
    parser = TDXFormulaParser()
    print("✅ 通达信公式解析器创建成功")
    
    # 测试示例公式
    print("\n1. 解析示例公式:")
    print("-"*40)
    print(EXAMPLE_FORMULA)
    
    result = parser.parse_formula(EXAMPLE_FORMULA)
    
    print(f"\n✅ 公式解析完成:")
    print(f"   公式名称: {result['formula_info']['name']}")
    print(f"   公式描述: {result['formula_info']['description']}")
    
    # 显示参数
    if result['formula_info']['params']:
        print(f"\n   参数列表:")
        for param in result['formula_info']['params']:
            print(f"     • {param['name']}: 默认值={param['default']}, "
                  f"范围=[{param['min']}, {param['max']}]")
    
    # 显示变量
    if result['variables']:
        print(f"\n   中间变量:")
        for var_name, var_expr in result['variables'].items():
            print(f"     • {var_name} := {var_expr}")
    
    # 显示输出条件
    if result['output_conditions']:
        print(f"\n   输出条件:")
        for condition in result['output_conditions']:
            print(f"     • {condition['type']}: {condition['expression']}")
    
    # 生成Python代码
    print(f"\n2. 生成的Python代码预览:")
    print("-"*40)
    python_code = result['python_code']
    
    # 显示前20行代码
    lines = python_code.split('\n')
    for i, line in enumerate(lines[:25]):
        print(f"{i+1:3d}: {line}")
    
    if len(lines) > 25:
        print(f"      ... 还有{len(lines)-25}行代码")
    
    # 生成策略类
    print(f"\n3. 生成的策略类:")
    print("-"*40)
    strategy_code = parser.generate_strategy_class(EXAMPLE_FORMULA)
    
    # 显示策略类代码
    lines = strategy_code.split('\n')
    for i, line in enumerate(lines[:30]):
        print(f"{i+1:3d}: {line}")
    
    if len(lines) > 30:
        print(f"      ... 还有{len(lines)-30}行代码")
    
    # 测试自定义公式
    print(f"\n4. 测试自定义公式:")
    print("-"*40)
    
    custom_formula = """
公式名称: RSI超买超卖策略
公式描述: RSI指标超买超卖策略

参数: N(14,6,30), OVERBOUGHT(70,50,90), OVERSOLD(30,10,50)

RSI:=RSI(CLOSE,N);

超买:=RSI>OVERBOUGHT;
超卖:=RSI<OVERSOLD;

买入信号:超卖;
卖出信号:超买;
"""
    
    print(custom_formula)
    
    custom_result = parser.parse_formula(custom_formula)
    
    print(f"\n✅ 自定义公式解析完成:")
    print(f"   公式名称: {custom_result['formula_info']['name']}")
    print(f"   参数数量: {len(custom_result['formula_info']['params'])}")
    print(f"   输出条件: {len(custom_result['output_conditions'])}")
    
    # 显示函数映射
    print(f"\n5. 函数映射表（部分）:")
    print("-"*40)
    
    function_samples = {
        'MA': '移动平均线',
        'EMA': '指数移动平均',
        'RSI': '相对强弱指数',
        'MACD': '指数平滑异同平均线',
        'CROSS': '交叉函数',
        'HHV': '最高值',
        'LLV': '最低值',
        'REF': '引用前N周期'
    }
    
    for tdx_func, description in function_samples.items():
        if tdx_func in parser.FUNCTION_MAP:
            py_func = parser.FUNCTION_MAP[tdx_func]
            print(f"   {tdx_func:10s} → {py_func:15s} # {description}")
    
    # 测试表达式转换
    print(f"\n6. 表达式转换测试:")
    print("-"*40)
    
    test_expressions = [
        "MA(CLOSE,5)",
        "CROSS(MA5,MA20)",
        "CLOSE>MA(CLOSE,10) AND VOLUME>MA(VOLUME,20)",
        "RSI(CLOSE,14)>70",
        "REF(CLOSE,1)>CLOSE"
    ]
    
    for expr in test_expressions:
        converted = parser._convert_expression(expr)
        print(f"   通达信: {expr}")
        print(f"   Python: {converted}")
        print()
    
    # 保存生成的代码
    output_file = "generated_strategy.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(strategy_code)
    
    print(f"\n✅ 策略代码已保存到: {output_file}")
    
    # 创建测试用的通达信公式文件
    formula_file = "tdx_formula_example.txt"
    with open(formula_file, "w", encoding="utf-8") as f:
        f.write(EXAMPLE_FORMULA)
    
    print(f"✅ 示例公式已保存到: {formula_file}")
    
    print(f"\n📋 使用说明:")
    print(f"1. 编辑 {formula_file} 文件添加你的通达信公式")
    print(f"2. 运行解析器: python -m tdxtools.cli parse --formula-file {formula_file}")
    print(f"3. 生成的策略代码可以在回测中使用")
    
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所有依赖")

except Exception as e:
    print(f"❌ 测试过程中出错: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("公式解析器测试完成！")
print("="*60)