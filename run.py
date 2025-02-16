'''
Date: 2025-02-14 20:07:34
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-16 19:19:33
FilePath: \spider\run.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
import subprocess
import platform

# 检查操作系统
current_platform = platform.system()

if current_platform == "Windows":
    # 在 Windows 上执行 .bat 文件
    bat_file = "./spiders.bat"
    try:
        result = subprocess.run(
            [bat_file],  # 调用 .bat 文件
            shell=True,  # Windows 系统需要设置 shell=True
            capture_output=True,  # 捕获标准输出和标准错误
            text=True,  # 以文本格式输出
            check=True,  # 如果命令失败则引发异常
        )

        # 输出执行结果
        print("BAT 文件执行成功")
        print("输出：", result.stdout)
    except subprocess.CalledProcessError as e:
        print("BAT 文件执行失败")
        print("错误输出：", e.stderr)
else:
    # 在非 Windows 操作系统上执行 Linux 相关命令
    try:
        result = subprocess.run(
            ["bash", "./spiders.sh"],  # 执行 .sh 脚本
            capture_output=True,
            text=True,
            check=True,
        )

        print("Shell 脚本执行成功")
        print("输出：", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Shell 脚本执行失败")
        print("错误输出：", e.stderr)
