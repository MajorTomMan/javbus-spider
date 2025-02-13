
import subprocess

# 执行 bat 文件
bat_file = "./spiders.bat"

try:
    # 运行 .bat 文件，并等待其完成
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
