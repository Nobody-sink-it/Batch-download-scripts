import requests
from bs4 import BeautifulSoup


def simple_crawler():
    # ================= 配置区域 =================

    # 1. 目标网址 (这里填写你想要爬取的网页链接)
    target_url = "https://www.baidu.com"

    # 2. 请求头 (Headers)
    # 很多网站会检查 User-Agent 来判断访问者是浏览器还是爬虫脚本。
    # 如果不加这一行，可能会被网站拒绝访问 (返回 403 Forbidden)。
    # 你可以在这里修改成你自己的浏览器 User-Agent。
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # ===========================================

    try:
        # 1. 发送 HTTP GET 请求（修正1：添加timeout参数）
        print(f"正在请求: {target_url} ...")
        response = requests.get(url=target_url, headers=headers, timeout=10)

        # 2. 设置响应编码（修正2：避免中文乱码）
        response.encoding = response.apparent_encoding

        # 3. 检查请求是否成功 (状态码 200 表示成功)
        if response.status_code == 200:
            print("请求成功！正在解析内容...\n")

            # 4. 使用 BeautifulSoup 解析网页文本内容
            # 'html.parser' 是 Python 内置的解析器，不需要额外安装
            soup = BeautifulSoup(response.text, 'html.parser')

            # 5. 提取并处理文字
            # soup.get_text() 会获取网页中所有的可见文字，包括标签之间的换行和空格
            raw_text = soup.get_text()

            # 简单的清洗：将连续的空白字符（换行、空格、制表符）替换为一个空格
            clean_text = ' '.join(raw_text.split())

            # 6. 打印结果 (或者你可以写入文件)
            print("=== 爬取到的文字内容 ===")
            print(clean_text)
            print("======================")

            # 如果你想保存到文件，可以取消下面几行的注释：
            # with open("baidu_text.txt", "w", encoding="utf-8") as f:
            #     f.write(clean_text)
            # print("内容已保存到 baidu_text.txt")

        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("错误：请求超时，请检查网络连接或增加超时时间")

    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请检查网址或网络连接")

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")

    except Exception as e:
        print(f"发生未知错误: {e}")

    finally:
        # 确保响应对象被正确关闭，释放连接资源
        if 'response' in locals():
            response.close()
            print("\n连接已关闭")


if __name__ == "__main__":
    simple_crawler()
