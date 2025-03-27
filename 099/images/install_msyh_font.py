import os
import shutil
import requests
import sys
from subprocess import run
import matplotlib
import zipfile
from io import BytesIO


def download_and_extract_zip(url, extract_to):
    """
    下载 ZIP 文件并解压到指定目录
    :param url: ZIP 文件 URL
    :param extract_to: 解压目录路径
    """
    # 确保目标目录存在
    os.makedirs(extract_to, exist_ok=True)

    try:
        print(f"正在下载: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        zip_data = BytesIO(response.content)

        print(f"正在解压到: {extract_to}")
        with zipfile.ZipFile(zip_data) as zip_ref:
            zip_ref.extractall(extract_to)

        print("下载并解压完成！")
    except Exception as e:
        print(f"下载并解压发生 url={url} 错误: {e}")

def main():
    print("=== 开始安装微软雅黑字体到 Conda 环境 start ===")

    matplotlib_fname = matplotlib.matplotlib_fname()
    print(f'step 1, matplotlib_fname：{matplotlib_fname}')
    matplotlib_fname_dir = os.path.dirname(matplotlib_fname)

    print(f'step 2, 检查字体文件是否存在')
    if os.path.isfile(matplotlib_fname_dir + '/fonts/ttf/chinese.msyh.ttf'):
        print(f'step 3, 字体文件已存在')
    else:
        print(f'step 3, 下载并导入字体文件')
        font_dir = matplotlib_fname_dir + '/fonts/ttf'
        download_and_extract_zip(url='https://image.woodwhales.cn/099/images/microsoft-yahei.zip', extract_to = font_dir)

    print(f'step 4, 清除 Matplotlib 缓存...')
    shutil.rmtree(matplotlib.get_cachedir(), ignore_errors=True)

    print(f'step 5, 启动新进程验证字体...')

    result = run([
        sys.executable, "-c",
        f"import matplotlib.font_manager; "
        f"print([f.name for f in matplotlib.font_manager.fontManager.ttflist if 'Microsoft YaHei' in f.name])"
    ], capture_output=True, text=True)

    # 4. 解析输出结果
    font_list = eval(result.stdout.strip())
    if font_list:
        print(f"字体安装成功: {font_list[0]}")
    else:
        print("字体安装失败，请手动刷新缓存或检查字体路径。")

    print("=== 开始安装微软雅黑字体到 Conda 环境 end ===")

if __name__ == "__main__":
    main()