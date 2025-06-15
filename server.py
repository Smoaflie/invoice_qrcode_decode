import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
from datetime import datetime
from flask import Flask, request, jsonify
import re
import os

# 发票数据结构类
class Invoice:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.invoice_number = parse_invoice_data(raw_data)
        self.timestamp = datetime.now()
        self.status = "未处理"
    
    def __str__(self):
        return f"{self.invoice_number} ({self.timestamp.strftime('%H:%M:%S')})"

    def to_dict(self):
        """将发票数据转换为字典格式"""
        return {
            "raw_data": self.raw_data,
            "invoice_number": self.invoice_number,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }

# 发票数据分组类
class InvoiceGroup:
    def __init__(self):
        self.invoices = []
        self.created_at = datetime.now()
        self.status = "当前组"
    
    def add_invoice(self, invoice):
        self.invoices.append(invoice)
    
    def count(self):
        return len(self.invoices)
    
    def get_invoice_numbers(self):
        return [inv.invoice_number for inv in self.invoices]
    
    def __str__(self):
        return f"组 ({self.count()}张发票) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def to_dict(self):
        """将分组数据转换为字典格式"""
        return {
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "invoice_count": self.count(),
            "invoices": [inv.to_dict() for inv in self.invoices]
        }

# 解析发票数据 - 这是一个示例实现，您可以根据实际需求修改
def parse_invoice_data(data):
    """从原始数据中解析出发票号码"""
    try:
        # 定义正则表达式模式
        # 01,31,,24312000000358032546,633.00,20241118,,16C0
        patterns = [
            r'^(?:01|04|10|08),\d*,\d*,(\d*),\S*$',  # 增值税电子普通发票和增值税专用发票
            r'^(\d{12}),\S*$',  # 全面数字化的电子发票（全电发票）
            r'^(?:https://)\S+bill_num=(\d*)'  # 深圳电子发票
        ]
        for pattern in patterns:
            match = re.search(pattern, data)
            if match:
                return match.group(1)
        
        # 如果都没有找到，返回None
        return None
    
    except Exception as e:
        print(f"解析发票数据出错: {e}")
        return None

# 主应用类
class InvoiceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("发票管理系统")
        self.root.geometry("800x600")
        
        # 初始化数据
        self.processed_invoices = set()  # 已处理的发票号码集合
        self.current_group = InvoiceGroup()  # 当前组
        self.result_groups = []  # 历史分组列表
        self.current_view_index = -1  # 当前查看的分组索引(-1表示当前组)
        
        # 创建UI
        self.create_widgets()
        
        # 启动Flask服务器
        self.start_flask_server()
        
        # 设置键盘绑定
        self.root.bind("<space>", self.commit_current_group)
        self.root.bind("<Left>", self.show_prev_group)
        self.root.bind("<Right>", self.show_next_group)
        self.root.bind("<a>", self.show_prev_group)
        self.root.bind("<d>", self.show_next_group)
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 分组信息面板
        group_frame = ttk.LabelFrame(main_frame, text="当前分组信息")
        group_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.group_label = ttk.Label(
            group_frame, 
            text="当前组 (0张发票)", 
            font=("Arial", 12, "bold")
        )
        self.group_label.pack(pady=5)
        
        # 分组列表
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 发票列表
        self.invoice_list = tk.Listbox(
            list_frame, 
            selectmode=tk.SINGLE,
            font=("Arial", 10)
        )
        self.invoice_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, command=self.invoice_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.invoice_list.config(yscrollcommand=scrollbar.set)
        
        # 按钮面板
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 左侧按钮组
        left_btn_frame = ttk.Frame(button_frame)
        left_btn_frame.pack(side=tk.LEFT)

        # 提交按钮
        commit_btn = ttk.Button(
            left_btn_frame, 
            text="提交当前组 (空格键)", 
            command=self.commit_current_group
        )
        commit_btn.pack(side=tk.LEFT, padx=5)
        
        # 导出按钮
        export_btn = ttk.Button(
            left_btn_frame, 
            text="导出数据 (E键)", 
            command=self.export_data
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        # 历史分组导航
        nav_frame = ttk.Frame(button_frame)
        nav_frame.pack(side=tk.RIGHT, padx=5)
        
        prev_btn = ttk.Button(
            nav_frame, 
            text="← 上一个 (A/←)", 
            command=lambda: self.show_prev_group()
        )
        prev_btn.pack(side=tk.LEFT, padx=2)
        
        next_btn = ttk.Button(
            nav_frame, 
            text="下一个 → (D/→)", 
            command=lambda: self.show_next_group()
        )
        next_btn.pack(side=tk.LEFT, padx=2)
        
        # 状态栏
        self.status_bar = ttk.Label(
            self.root, 
            text="就绪 | 0张发票已处理 | 按空格键提交当前组",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_flask_server(self, port=5000):
        """启动Flask服务器接收数据"""
        self.data_queue = []
        
        app = Flask(__name__)
        
        @app.route('/')
        def handle_qr_data():
            data = request.args.get('data')
            # 深圳电子普票的二维码数据会引发BUG，进行特殊处理："https://bcfp.shenzhen.chinatax.gov.cn/verify/scan?hash=**&bill_num=000000&total_amount=0"
            bill_num = request.args.get('bill_num')
            if bill_num:
                print(bill_num)
                data = f"https://bcfp.shenzhen.chinatax.gov.cn/verify/scan?hash=**&bill_num={bill_num}"
            
            if data:
                # 将数据添加到队列，UI线程会处理
                self.data_queue.append(data)
                return jsonify({"status": "success", "message": "数据已接收"})
            return jsonify({"status": "error", "message": "无效数据"}), 400
        
        # 在后台线程中运行Flask
        def run_server():
            app.run(host='0.0.0.0', port=port)
        
        threading.Thread(target=run_server, daemon=True).start()
        
        # 定期检查数据队列
        self.check_data_queue()
    
    def check_data_queue(self):
        """定期检查并处理接收到的数据"""
        while self.data_queue:
            data = self.data_queue.pop(0)
            self.process_invoice_data(data)
        
        # 每100毫秒检查一次
        self.root.after(100, self.check_data_queue)
    
    def process_invoice_data(self, data):
        """处理接收到的发票数据"""
        # 创建发票对象
        invoice = Invoice(data)
        
        # 检查是否存在
        if not invoice.invoice_number:
            self.update_status(f"无法正常识别该发票，qrcode:{data}，跳过")
            return

        # 检查是否已处理过
        if invoice.invoice_number in self.processed_invoices:
            self.update_status(f"发票 {invoice.invoice_number} 已处理过，跳过")
            return
        
        # 添加到当前组
        self.current_group.add_invoice(invoice)
        self.processed_invoices.add(invoice.invoice_number)
        
        # 更新UI
        self.update_group_display()
        
        self.update_status(f"已添加发票: {invoice.invoice_number}")
    
    def commit_current_group(self, event=None):
        """提交当前组到历史记录"""
        if self.current_group.count() == 0:
            self.update_status("当前组为空，无需提交")
            return
        
        # 标记当前组为已完成
        self.current_group.status = "已完成"
        
        # 添加到历史组
        self.result_groups.append(self.current_group)
        
        # 创建新组
        self.current_group = InvoiceGroup()
        
        # 更新UI
        self.update_group_display()
        
        # 显示成功消息
        messagebox.showinfo(
            "分组提交成功", 
            f"已提交包含 {self.result_groups[-1].count()} 张发票的分组"
        )
    
    def show_prev_group(self, event=None):
        """显示上一个分组"""
        if not self.result_groups:
            return
        
        if self.current_view_index <= 0:
            # 如果已经在第一个，则跳转到最后一个
            self.current_view_index = len(self.result_groups) - 1
        else:
            self.current_view_index -= 1
        
        self.update_group_display()
    
    def show_next_group(self, event=None):
        """显示下一个分组"""
        if not self.result_groups:
            return
        
        if self.current_view_index >= len(self.result_groups) - 1:
            # 如果已经在最后一个，则跳转到第一个
            self.current_view_index = 0
        else:
            self.current_view_index += 1
        
        self.update_group_display()
    
    def export_data(self, event=None):
        """导出结果数据为JSON文件"""
        if not self.result_groups:
            messagebox.showwarning("导出失败", "没有可导出的数据！")
            return
        
        # 创建导出数据结构
        export_data = {
            "metadata": {
                "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_groups": len(self.result_groups),
                "total_invoices": sum(group.count() for group in self.result_groups)
            },
            "groups": [group.to_dict() for group in self.result_groups]
        }
        
        # 生成默认文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"invoice_export_{timestamp}.json"
        
        # 打开文件选择对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            initialfile=default_filename
        )
        
        if not file_path:
            return  # 用户取消了保存
        
        try:
            # 写入JSON文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            # 显示成功消息
            messagebox.showinfo(
                "导出成功", 
                f"数据已成功导出到:\n{file_path}\n\n"
                f"包含 {len(self.result_groups)} 个分组，"
                f"共 {export_data['metadata']['total_invoices']} 张发票"
            )
            
            # 更新状态栏
            self.update_status(f"数据已导出到: {os.path.basename(file_path)}")
        
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时出错:\n{str(e)}")
            self.update_status(f"导出失败: {str(e)}")

    def update_group_display(self):
        """更新分组显示"""
        # 更新分组标签
        if self.current_view_index == -1:
            group = self.current_group
            group_label_text = f"当前组 ({group.count()}张发票)"
        else:
            group = self.result_groups[self.current_view_index]
            group_label_text = f"历史组 {self.current_view_index + 1}/{len(self.result_groups)} ({group.count()}张发票)"
        
        self.group_label.config(text=group_label_text)
        
        # 更新发票列表
        self.invoice_list.delete(0, tk.END)
        for invoice in group.invoices:
            self.invoice_list.insert(tk.END, str(invoice))
        
        # 更新状态栏
        total_processed = len(self.processed_invoices)
        self.update_status(f"就绪 | {total_processed}张发票已处理 | 按空格键提交当前组")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=message)

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceManagerApp(root)
    root.mainloop()