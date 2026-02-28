# 文件管理脚本使用说明

## 功能介绍

这个脚本帮助你管理浏览器下载的文件，主要功能包括：

1. **扫描下载目录** - 自动扫描浏览器下载的所有文件
2. **智能分类** - 按文件类型自动分类，并根据网盘存储策略分组
3. **批量整理** - 将文件移动到本地分类目录
4. **网盘同步** - 自动生成网盘上传建议和同步脚本

## 网盘存储策略

### WPS云盘存储（文档类）
- **PDF文档** (.pdf)
- **Word文档** (.doc, .docx)
- **Excel表格** (.xls, .xlsx)
- **PPT演示** (.ppt, .pptx)
- **电子书** (.epub)

### 百度网盘存储（杂项类）
- **视频文件** (.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v)
- **压缩包** (.zip, .rar, .7z, .tar, .gz)
- **图片** (.jpg, .jpeg, .png, .gif, .bmp, .svg, .webp)
- **音频** (.mp3, .wav, .flac, .aac, .m4a)
- **代码文件** (.py, .js, .java, .cpp, .c, .h, .html, .css)
- **其他** (未匹配的文件类型)

## 快速开始

### 第一步：修改配置

打开 `file_manager.py`，找到 `FileManager.__init__` 方法中的配置区域，修改以下路径：

```python
# 1. 浏览器下载路径（必须修改）
self.browser_download_path = r"C:\Users\你的用户名\Downloads"

# 2. 本地存储根目录（可选修改）
self.local_storage_root = r"B:\Downloads_Organized"

# 3. WPS云盘同步目录（如果使用WPS）
self.wps_sync_path = r"C:\Users\你的用户名\WPS Cloud"

# 4. 百度网盘同步目录（如果使用百度网盘）
self.baidu_sync_path = r"C:\Users\你的用户名\BaiduNetdisk"
```

### 第二步：运行脚本

```bash
python file_manager.py
```

### 第三步：选择操作

脚本会显示交互式菜单，你可以选择：
1. **整理所有文件** - 将所有文件整理到本地存储目录
2. **只整理WPS云盘文件** - 只整理PDF、Word、Excel、PPT、EPUB文件
3. **只整理百度网盘文件** - 只整理视频、压缩包、图片、音频、代码等文件
4. **按文件类型整理** - 选择特定文件类型进行整理
5. **只整理大文件** - 只整理超过阈值的大文件
6. **创建网盘同步脚本** - 生成自动同步到网盘的批处理脚本
7. **重新扫描下载目录** - 刷新文件列表

## 配置详解

### 1. 浏览器下载路径

**Windows系统常见路径：**

```
Chrome/Edge/Firefox: C:\Users\<你的用户名>\Downloads
```

**如何找到你的下载路径：**
1. 打开浏览器
2. 按 `Ctrl + J` 打开下载管理
3. 点击"在文件夹中显示"或查看下载设置
4. 复制完整路径

**示例：**
```python
self.browser_download_path = r"C:\Users\张三\Downloads"
```

### 2. 本地存储目录

这是文件整理后的存储位置，建议选择一个空间充足的磁盘：

```python
self.local_storage_root = r"D:\我的文件\下载整理"
```

脚本会自动创建以下子目录：
- 视频/
- PDF文档/
- Word文档/
- Excel表格/
- PPT演示/
- 压缩包/
- 图片/
- 音频/
- 代码文件/
- 其他/

### 3. 网盘同步目录

#### WPS云盘

如果你安装了WPS并开启了云同步，WPS会在本地创建一个同步文件夹。

**查找方法：**
1. 打开WPS
2. 点击"云文档"或"我的云盘"
3. 查看本地同步目录位置

**常见位置：**
```python
self.wps_sync_path = r"C:\Users\<用户名>\WPS Cloud"
# 或
self.wps_sync_path = r"C:\Users\<用户名>\Documents\WPS Cloud"
```

#### 百度网盘

如果你安装了百度网盘客户端，可以设置自动同步目录。

**查找方法：**
1. 打开百度网盘客户端
2. 进入设置 -> 基本设置
3. 查看"同步空间"或"自动备份"设置

**常见位置：**
```python
self.baidu_sync_path = r"C:\Users\<用户名>\BaiduNetdisk"
# 或
self.baidu_sync_path = r"D:\百度网盘下载"
```

### 4. 文件分类配置

你可以自定义文件分类规则：

```python
self.file_categories = {
    # WPS云盘存储的文件类型（文档类）
    "PDF文档": [".pdf"],
    "Word文档": [".doc", ".docx"],
    "Excel表格": [".xls", ".xlsx"],
    "PPT演示": [".ppt", ".pptx"],
    "电子书": [".epub"],
    # 百度网盘存储的文件类型（杂项类）
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "代码文件": [".py", ".js", ".java", ".cpp", ".c", ".h", ".html", ".css"],
    "其他": []
}
```

**网盘存储策略配置：**
```python
# WPS云盘存储的文件分类
self.wps_categories = ["PDF文档", "Word文档", "Excel表格", "PPT演示", "电子书"]

# 百度网盘存储的文件分类
self.baidu_categories = ["视频", "压缩包", "图片", "音频", "代码文件", "其他"]
```

**添加新分类示例：**
```python
# 在 file_categories 中添加
"电子书": [".epub", ".mobi", ".azw3"],

# 如果要添加到WPS云盘，在 wps_categories 中添加
self.wps_categories = ["PDF文档", "Word文档", "Excel表格", "PPT演示", "电子书"]

# 如果要添加到百度网盘，在 baidu_categories 中添加
self.baidu_categories = ["视频", "压缩包", "图片", "音频", "代码文件", "其他", "电子书"]
```

### 5. 大文件阈值

设置大文件的判定标准（单位：MB）：

```python
self.large_file_threshold = 100  # 100MB以上的文件会被标记为大文件
```

### 6. 移动确认

控制是否在移动文件前进行确认：

```python
self.confirm_before_move = True   # 每次移动前询问确认
self.confirm_before_move = False  # 自动移动，不询问
```

## 使用场景

### 场景1：按网盘类型整理文件

1. 运行脚本
2. 选择"只整理WPS云盘文件"或"只整理百度网盘文件"
3. 文件会自动分类到本地存储目录
4. 使用生成的同步脚本上传到对应网盘

### 场景2：只整理PDF文档到WPS云盘

1. 运行脚本
2. 选择"只整理WPS云盘文件"
3. PDF、Word、Excel、PPT、EPUB文件会移动到本地存储目录
4. 运行同步脚本或手动复制到WPS同步目录
5. WPS会自动上传到云端

### 场景3：处理大文件

1. 运行脚本
2. 查看大文件列表
3. 选择"只整理大文件"
4. 将整理后的大文件上传到百度网盘（推荐）

### 场景4：批量同步到网盘

1. 运行脚本
2. 选择"创建网盘同步脚本"
3. 运行生成的 `sync_to_cloud.bat`
4. 脚本会自动将文件复制到对应的网盘同步目录：
   - WPS云盘：PDF、Word、Excel、PPT、EPUB
   - 百度网盘：视频、压缩包、图片、音频、代码文件、其他

## 注意事项

1. **首次使用前一定要修改配置路径**
2. 确保目标磁盘有足够的空间
3. 建议先使用"确认模式"（`confirm_before_move = True`）
4. 重要文件建议先备份再整理
5. 网盘同步需要安装对应的客户端并登录

## 常见问题

**Q: 提示"下载路径不存在"？**
A: 检查 `browser_download_path` 配置是否正确，注意使用原始字符串（r"路径"）

**Q: 文件移动失败？**
A: 可能原因：
- 文件正在被使用（关闭相关程序）
- 目标磁盘空间不足
- 权限不足（以管理员身份运行）

**Q: 如何添加新的文件类型？**
A: 在 `file_categories` 配置中添加新的分类和对应的扩展名

**Q: 可以同时管理多个下载目录吗？**
A: 当前版本只支持单个目录，你可以多次运行脚本处理不同目录

## 高级用法

### 自定义处理逻辑

你可以在 `organize_files` 方法中添加自定义逻辑，例如：

```python
# 只处理最近7天的文件
from datetime import datetime, timedelta

seven_days_ago = datetime.now() - timedelta(days=7)
recent_files = [f for f in files_info 
                if datetime.strptime(f["modified_time"], "%Y-%m-%d %H:%M:%S") > seven_days_ago]
```

### 添加文件重命名规则

在移动文件时，你可以添加重命名逻辑：

```python
# 在 organize_files 方法中修改
new_name = f"{datetime.now().strftime('%Y%m%d')}_{file_info['name']}"
target_path = os.path.join(target_dir, new_name)
```

## 更新日志

- v1.0 - 初始版本
  - 支持文件扫描和分类
  - 支持批量移动
  - 支持网盘同步建议
