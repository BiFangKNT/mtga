# _run_wrapper.py
import subprocess
import os
import sys

def get_script_dir():
    """获取包含可执行件或脚本的目录。"""
    if getattr(sys, 'frozen', False):
        # 如果应用程序是作为打包/冻结的可执行文件运行
        return os.path.dirname(sys.executable)
    else:
        # 如果作为标准 Python 脚本运行
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    script_dir = get_script_dir()
    # 注意：这里的 bat 文件名需要和您实际的文件名一致
    bat_file = os.path.join(script_dir, "run_mtga_gui.bat") 

    if not os.path.exists(bat_file):
        print(f"错误: 启动脚本未找到: {bat_file}")
        # 在Python中使用input实现暂停效果
        input("按 Enter 键退出...") 
        sys.exit(1)

    # 执行批处理脚本
    # 在Windows上执行 .bat 文件通常需要 shell=True
    # cwd确保批处理脚本在其预期的目录中运行
    try:
        # 直接运行，允许在当前控制台查看输出（如果存在）
        # check=True 会在批处理脚本返回非零退出码时抛出异常
        process = subprocess.run([bat_file], shell=True, check=True, cwd=script_dir)
        # 正常退出时，使用批处理脚本的退出码
        sys.exit(process.returncode)
    except subprocess.CalledProcessError as e:
        # 如果批处理脚本出错退出（非零退出码），打印错误信息
        # 原始批处理脚本在出错时有自己的 pause 机制，这里不再添加 input
        print(f"启动脚本执行失败，错误代码: {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        # 捕获其他可能的异常
        print(f"执行启动脚本时发生意外错误: {e}")
        input("按 Enter 键退出...")
        sys.exit(1)
