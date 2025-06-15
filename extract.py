import json
import sys
import os

def extract_invoice_data(input_file, target):
    """
    从导出的JSON文件中提取发票分组信息
    
    参数:
    input_file: 输入的JSON文件路径
    target: 目标标识符字符串
    
    返回:
    重组后的分组数据列表
    """
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 初始化结果列表
    result = []
    
    # 处理每个分组
    for idx, group in enumerate(data.get('groups', []), start=1):
        # 创建当前分组的字典
        group_dict = {}
        
        # 为分组中的每张发票创建条目
        for invoice in group.get('invoices', []):
            invoice_number = invoice.get('invoice_number', '')
            if invoice_number:  # 确保发票号不为空
                # 使用格式 f"{target}_{分组序号}"
                group_dict[invoice_number] = f"{target}_{idx}"
        
        # 将当前分组字典添加到结果列表
        if group_dict:  # 只添加非空分组
            result.append(group_dict)
    
    return result

def main():
    # 检查命令行参数
    if len(sys.argv) != 3:
        print("使用方法: python func.py <输入文件> <目标标识符>")
        print("示例: python func.py ./invoice_data.json ABC")
        sys.exit(1)
    
    # 获取参数
    input_file = sys.argv[1]
    target = sys.argv[2]
    
    # 验证输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)
    
    # 提取数据
    try:
        extracted_data = extract_invoice_data(input_file, target)
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        sys.exit(1)
    
    # 生成输出文件名
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_extract.json"
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已成功提取并保存到: {output_file}")
    print(f"提取了 {len(extracted_data)} 个分组")

if __name__ == "__main__":
    main()