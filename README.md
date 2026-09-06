浏览器下载目录整理 + 网盘归档助手。扫描下载目录，按文件类型自动分类到本地目录，并按「文档进 WPS 云盘、大文件进百度网盘」的策略生成同步方案。

> 纯 Python 标准库实现，无第三方依赖，Windows 下开箱即用。

## 功能

- **扫描下载目录**：列出所有待整理文件，支持按大小、类型过滤
- **智能分类**：按扩展名分到 10 个类别（视频 / PDF / Word / Excel / PPT / 电子书 / 压缩包 / 图片 / 音频 / 代码）
- **批量移动**：移动前逐个确认，可只整理某一类或超过阈值的大文件
- **网盘归档**：按「文档类 → WPS 云盘、杂项类 → 百度网盘」的策略分组，一键生成 `sync_to_cloud.bat` 同步脚本

## 快速开始

```bash
git clone https://github.com/Nobody-sink-it/Batch-download-scripts.git
cd Batch-download-scripts
python file_manager.py
```

首次使用前，打开 `file_manager.py` 修改 `FileManager.__init__` 里的四个路径：

```python
self.browser_download_path = r"C:\Users\你的用户名\Downloads"   # 浏览器下载目录（必改）
self.local_storage_root   = r"D:\Downloads_Organized"           # 整理后的本地存储根目录
self.wps_sync_path        = r"C:\Users\你的用户名\WPS Cloud"     # WPS 云盘同步目录
self.baidu_sync_path      = r"C:\Users\你的用户名\BaiduNetdisk"  # 百度网盘同步目录
```

路径建议写成原始字符串（`r"..."`），避免反斜杠转义问题。

## 分类与网盘策略

| 去向 | 类别 | 扩展名 |
| --- | --- | --- |
| WPS 云盘 | PDF / Word / Excel / PPT / 电子书 | `.pdf` `.doc(x)` `.xls(x)` `.ppt(x)` `.epub` |
| 百度网盘 | 视频 / 压缩包 / 图片 / 音频 / 代码 / 其他 | `.mp4` `.zip` `.jpg` `.mp3` `.py` 等 |

分类规则、网盘分组和大文件阈值（默认 100 MB）都可以在 `file_categories`、`wps_categories`、`baidu_categories`、`large_file_threshold` 里自定义。

## 交互菜单

运行后提供 7 个操作：整理全部文件、只整理 WPS 云盘类、只整理百度网盘类、按类型整理、只整理大文件、生成网盘同步脚本、重新扫描。

## 注意事项

1. 首次使用务必先改配置路径
2. 建议保持确认模式（`confirm_before_move = True`），重要文件先备份
3. 网盘同步需要已安装并登录对应客户端
4. 文件被占用导致移动失败时，关闭相关程序后重试
