#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理脚本 - 批量管理浏览器下载的文件
功能：
1. 扫描浏览器下载目录
2. 按文件类型分类（视频、PDF、文档等）
3. 批量移动到指定目录
4. 生成网盘导入辅助信息
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class FileManager:
    def __init__(self):
        # ==================== 配置区域 - 请根据你的实际情况修改 ====================

        # 浏览器默认下载路径（请修改为你的浏览器下载路径）
        # Windows常见路径示例：
        # Chrome: C:\\Users\\你的用户名\\Downloads
        # Edge: C:\\Users\\你的用户名\\Downloads
        # Firefox: C:\\Users\\你的用户名\\Downloads
        self.browser_download_path = r"D:\EdgeDownloads"

        # 本地存储根目录（文件会移动到这里进行分类存储）
        self.local_storage_root = r"B:\Downloads_Organized"

        # 网盘同步目录（如果你有网盘客户端，可以设置对应的同步目录）
        # WPS云盘同步目录示例
        self.wps_sync_path = r"C:\Users\Nobody\WPSDrive\1756487604_1\WPS企业云盘\合肥工业大学\我的企业文档"

        # 百度网盘同步目录示例
        self.baidu_sync_path = r"D:\BaiduSyncdisk"

        # 文件类型分类配置
        # key: 分类名称
        # value: 该分类对应的文件扩展名列表
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
            "其他": []  # 未匹配的文件会归入此类
        }

        # 网盘存储策略配置
        # WPS云盘存储的文件分类
        self.wps_categories = ["PDF文档", "Word文档", "Excel表格", "PPT演示", "电子书"]

        # 百度网盘存储的文件分类
        self.baidu_categories = ["视频", "压缩包", "图片", "音频", "代码文件", "其他"]

        # 文件大小阈值配置（单位：MB）
        # 大于这个值的文件会被标记为"大文件"，方便你决定是否上传到网盘
        self.large_file_threshold = 100  # 100MB

        # 是否在移动文件前进行确认（True=需要确认，False=自动移动）
        self.confirm_before_move = True

        # ==================== 配置区域结束 ====================

    def scan_download_directory(self) -> List[Dict]:
        """
        扫描浏览器下载目录，获取所有文件信息
        返回: 文件信息列表
        """
        files_info = []

        if not os.path.exists(self.browser_download_path):
            print(f"❌ 错误：下载路径不存在: {self.browser_download_path}")
            print("请在脚本中修改 'browser_download_path' 为你的实际下载路径")
            return files_info

        print(f"📁 正在扫描目录: {self.browser_download_path}")

        for item in os.listdir(self.browser_download_path):
            item_path = os.path.join(self.browser_download_path, item)

            # 只处理文件，跳过文件夹
            if os.path.isfile(item_path):
                file_stat = os.stat(item_path)
                file_size_mb = file_stat.st_size / (1024 * 1024)

                file_info = {
                    "name": item,
                    "path": item_path,
                    "size_mb": round(file_size_mb, 2),
                    "size_human": self._format_file_size(file_stat.st_size),
                    "extension": Path(item).suffix.lower(),
                    "modified_time": datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "is_large": file_size_mb > self.large_file_threshold
                }

                # 确定文件分类
                file_info["category"] = self._get_file_category(file_info["extension"])

                files_info.append(file_info)

        return files_info

    def _format_file_size(self, size_bytes: int) -> str:
        """将字节转换为人类可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def _get_file_category(self, extension: str) -> str:
        """根据文件扩展名获取分类"""
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        return "其他"

    def display_files_summary(self, files_info: List[Dict]):
        """显示文件统计摘要"""
        if not files_info:
            print("📭 没有找到任何文件")
            return

        print("\n" + "="*80)
        print("📊 文件统计摘要")
        print("="*80)

        # 按分类统计
        category_stats = {}
        total_size = 0
        large_files_count = 0

        for file_info in files_info:
            category = file_info["category"]
            if category not in category_stats:
                category_stats[category] = {"count": 0, "size": 0}

            category_stats[category]["count"] += 1
            category_stats[category]["size"] += file_info["size_mb"]
            total_size += file_info["size_mb"]

            if file_info["is_large"]:
                large_files_count += 1

        print(f"\n总文件数: {len(files_info)} 个")
        print(f"总大小: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
        print(f"大文件数: {large_files_count} 个 (>{self.large_file_threshold}MB)")

        print("\n按分类统计:")
        print("-" * 60)
        for category, stats in sorted(category_stats.items(), key=lambda x: x[1]["size"], reverse=True):
            print(f"  {category:12s}: {stats['count']:3d} 个文件, 共 {stats['size']:.2f} MB")

        print("\n" + "="*80)

    def display_files_list(self, files_info: List[Dict], show_large_only: bool = False):
        """显示文件详细列表"""
        if not files_info:
            print("📭 没有找到任何文件")
            return

        display_files = [f for f in files_info if not show_large_only or f["is_large"]]

        if not display_files:
            print("📭 没有符合条件的大文件")
            return

        print("\n" + "="*100)
        title = "大文件列表" if show_large_only else "文件列表"
        print(f"📋 {title}")
        print("="*100)
        print(f"{'序号':<6} {'文件名':<40} {'大小':<15} {'分类':<12} {'修改时间'}")
        print("-"*100)

        for idx, file_info in enumerate(display_files, 1):
            large_flag = "🔥 " if file_info["is_large"] else "   "
            name_display = file_info["name"][:38] + ".." if len(file_info["name"]) > 40 else file_info["name"]
            print(f"{large_flag}{idx:<4} {name_display:<40} {file_info['size_human']:<15} {file_info['category']:<12} {file_info['modified_time']}")

        print("="*100 + "\n")

    def organize_files(self, files_info: List[Dict], target_category: str = None):
        """
        整理文件到本地存储目录
        target_category: 只整理指定分类的文件，None表示整理所有文件
        """
        if not files_info:
            print("📭 没有文件需要整理")
            return

        # 创建本地存储目录
        os.makedirs(self.local_storage_root, exist_ok=True)

        # 筛选要处理的文件
        files_to_process = files_info if target_category is None else \
                          [f for f in files_info if f["category"] == target_category]

        if not files_to_process:
            print(f"📭 没有找到分类为 '{target_category}' 的文件")
            return

        print(f"\n🔄 准备整理 {len(files_to_process)} 个文件...")

        if self.confirm_before_move:
            response = input("是否继续？(y/n): ").strip().lower()
            if response != 'y':
                print("❌ 操作已取消")
                return

        # 按分类创建目录并移动文件
        moved_count = 0
        failed_count = 0
        move_report = []

        for file_info in files_to_process:
            category = file_info["category"]
            target_dir = os.path.join(self.local_storage_root, category)

            try:
                # 创建分类目录
                os.makedirs(target_dir, exist_ok=True)

                # 移动文件
                target_path = os.path.join(target_dir, file_info["name"])

                # 如果目标文件已存在，添加时间戳
                if os.path.exists(target_path):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    name_parts = os.path.splitext(file_info["name"])
                    new_name = f"{name_parts[0]}_{timestamp}{name_parts[1]}"
                    target_path = os.path.join(target_dir, new_name)

                shutil.move(file_info["path"], target_path)

                move_report.append({
                    "original_path": file_info["path"],
                    "new_path": target_path,
                    "category": category,
                    "size_mb": file_info["size_mb"],
                    "status": "success"
                })

                moved_count += 1
                print(f"✅ {file_info['name']} -> {category}/")

            except Exception as e:
                failed_count += 1
                move_report.append({
                    "original_path": file_info["path"],
                    "category": category,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"❌ 移动失败: {file_info['name']} - {e}")

        print(f"\n✨ 整理完成！成功: {moved_count} 个，失败: {failed_count} 个")

        # 保存移动报告
        self._save_move_report(move_report)

    def generate_cloud_upload_guide(self, files_info: List[Dict]):
        """生成网盘上传指导信息"""
        if not files_info:
            return

        print("\n" + "="*80)
        print("☁️  网盘上传建议")
        print("="*80)

        # WPS云盘存储的文件类型
        wps_files = [f for f in files_info if f["category"] in self.wps_categories]
        if wps_files:
            # 按分类统计
            wps_stats = {}
            for f in wps_files:
                cat = f["category"]
                if cat not in wps_stats:
                    wps_stats[cat] = {"count": 0, "size": 0}
                wps_stats[cat]["count"] += 1
                wps_stats[cat]["size"] += f["size_mb"]

            print(f"\n📄 WPS云盘文件 ({len(wps_files)} 个文件):")
            print("   文件类型: PDF、Word、Excel、PPT、EPUB")
            print(f"   WPS同步目录: {self.wps_sync_path}")
            print("   详细分类:")
            for cat, stats in wps_stats.items():
                print(f"     - {cat}: {stats['count']} 个文件, {stats['size']:.2f} MB")
            print("   操作方法: 将这些文件移动到WPS同步目录，会自动上传到云端")

        # 百度网盘存储的文件类型
        baidu_files = [f for f in files_info if f["category"] in self.baidu_categories]
        if baidu_files:
            # 按分类统计
            baidu_stats = {}
            for f in baidu_files:
                cat = f["category"]
                if cat not in baidu_stats:
                    baidu_stats[cat] = {"count": 0, "size": 0}
                baidu_stats[cat]["count"] += 1
                baidu_stats[cat]["size"] += f["size_mb"]

            print(f"\n☁️  百度网盘文件 ({len(baidu_files)} 个文件):")
            print("   文件类型: 视频、压缩包、图片、音频、代码文件、其他")
            print(f"   百度网盘同步目录: {self.baidu_sync_path}")
            print("   详细分类:")
            for cat, stats in baidu_stats.items():
                print(f"     - {cat}: {stats['count']} 个文件, {stats['size']:.2f} MB")
            print("   操作方法: 将这些文件移动到百度网盘同步目录")

        # 大文件提醒
        large_files = [f for f in files_info if f["is_large"]]
        if large_files:
            print(f"\n🔥 大文件提醒 ({len(large_files)} 个文件，>{self.large_file_threshold}MB):")
            print("   注意: 大文件建议上传到百度网盘，百度网盘存储空间更大")

        print("\n" + "="*80)

    def _save_move_report(self, move_report: List[Dict]):
        """保存文件移动报告"""
        report_path = os.path.join(self.local_storage_root, f"move_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(move_report, f, ensure_ascii=False, indent=2)

        print(f"\n📝 移动报告已保存: {report_path}")

    def create_cloud_sync_script(self):
        """创建网盘同步辅助脚本"""
        # 构建WPS云盘同步命令
        wps_sync_commands = []
        for category in self.wps_categories:
            source_dir = f"{self.local_storage_root}\\{category}"
            wps_sync_commands.append(f'''
echo 正在同步 {category} 到WPS云盘...
if exist "{source_dir}" (
    xcopy "{source_dir}\\*" "{self.wps_sync_path}\\{category}\\" /Y /I /E
    echo {category} 同步完成
) else (
    echo 没有找到 {category} 目录
)
''')

        # 构建百度网盘同步命令
        baidu_sync_commands = []
        for category in self.baidu_categories:
            source_dir = f"{self.local_storage_root}\\{category}"
            baidu_sync_commands.append(f'''
echo 正在同步 {category} 到百度网盘...
if exist "{source_dir}" (
    xcopy "{source_dir}\\*" "{self.baidu_sync_path}\\{category}\\" /Y /I /E
    echo {category} 同步完成
) else (
    echo 没有找到 {category} 目录
)
''')

        script_content = f'''@echo off
chcp 65001 >nul
echo ========================================
echo    网盘文件同步脚本
echo ========================================
echo.

echo [1] 同步文档类文件到WPS云盘...
echo ----------------------------------------
{''.join(wps_sync_commands)}

echo.
echo [2] 同步杂项文件到百度网盘...
echo ----------------------------------------
{''.join(baidu_sync_commands)}

echo.
echo ========================================
echo    同步完成！
echo ========================================
echo.
echo WPS云盘目录: {self.wps_sync_path}
echo 百度网盘目录: {self.baidu_sync_path}
echo ========================================
pause
'''

        script_path = os.path.join(self.local_storage_root, "sync_to_cloud.bat")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        print(f"✅ 网盘同步脚本已创建: {script_path}")
        print(f"\n📋 脚本功能说明:")
        print(f"   WPS云盘将同步: {', '.join(self.wps_categories)}")
        print(f"   百度网盘将同步: {', '.join(self.baidu_categories)}")


def main():
    """主函数"""
    print("🚀 文件管理脚本启动...")
    print("="*80)

    # 创建文件管理器实例
    manager = FileManager()

    # 扫描下载目录
    files_info = manager.scan_download_directory()

    if not files_info:
        print("\n💡 提示：")
        print("1. 请检查 'browser_download_path' 配置是否正确")
        print("2. 确保浏览器下载目录中有文件")
        return

    # 显示统计信息
    manager.display_files_summary(files_info)

    # 显示文件列表
    manager.display_files_list(files_info)

    # 显示大文件
    large_files = [f for f in files_info if f["is_large"]]
    if large_files:
        print(f"\n⚠️  发现 {len(large_files)} 个大文件:")
        manager.display_files_list(files_info, show_large_only=True)

    # 生成网盘上传建议
    manager.generate_cloud_upload_guide(files_info)

    # 交互式操作菜单
    while True:
        print("\n" + "="*80)
        print("📋 操作菜单")
        print("="*80)
        print("1. 整理所有文件到本地存储目录")
        print("2. 只整理WPS云盘文件 (PDF/Word/Excel/PPT/EPUB)")
        print("3. 只整理百度网盘文件 (视频/压缩包/图片/音频/代码/其他)")
        print("4. 按文件类型整理")
        print("5. 只整理大文件")
        print("6. 创建网盘同步脚本")
        print("7. 重新扫描下载目录")
        print("0. 退出")
        print("-"*80)

        choice = input("请选择操作 (0-7): ").strip()

        if choice == "1":
            manager.organize_files(files_info)
            # 重新扫描
            files_info = manager.scan_download_directory()
        elif choice == "2":
            # 整理WPS云盘文件
            wps_files = [f for f in files_info if f["category"] in manager.wps_categories]
            if wps_files:
                print(f"\n找到 {len(wps_files)} 个WPS云盘文件:")
                for cat in manager.wps_categories:
                    cat_files = [f for f in wps_files if f["category"] == cat]
                    if cat_files:
                        print(f"  - {cat}: {len(cat_files)} 个")
                manager.organize_files(wps_files)
                files_info = manager.scan_download_directory()
            else:
                print("没有找到WPS云盘类型的文件")
        elif choice == "3":
            # 整理百度网盘文件
            baidu_files = [f for f in files_info if f["category"] in manager.baidu_categories]
            if baidu_files:
                print(f"\n找到 {len(baidu_files)} 个百度网盘文件:")
                for cat in manager.baidu_categories:
                    cat_files = [f for f in baidu_files if f["category"] == cat]
                    if cat_files:
                        print(f"  - {cat}: {len(cat_files)} 个")
                manager.organize_files(baidu_files)
                files_info = manager.scan_download_directory()
            else:
                print("没有找到百度网盘类型的文件")
        elif choice == "4":
            # 按文件类型整理
            print("\n可用的文件类型:")
            all_categories = list(manager.file_categories.keys())
            for idx, cat in enumerate(all_categories, 1):
                count = len([f for f in files_info if f["category"] == cat])
                print(f"  {idx}. {cat} ({count} 个文件)")

            cat_choice = input("\n选择要整理的文件类型编号: ").strip()
            try:
                cat_idx = int(cat_choice) - 1
                if 0 <= cat_idx < len(all_categories):
                    selected_category = all_categories[cat_idx]
                    manager.organize_files(files_info, selected_category)
                    files_info = manager.scan_download_directory()
                else:
                    print("❌ 无效的编号")
            except ValueError:
                print("❌ 请输入有效的数字")
        elif choice == "5":
            large_file_list = [f for f in files_info if f["is_large"]]
            if large_file_list:
                print("\n大文件列表:")
                for idx, f in enumerate(large_file_list, 1):
                    print(f"  {idx}. {f['name']} ({f['size_human']}) - {f['category']}")

                # 提供选择整理特定分类的大文件
                category = input("\n输入要整理的大文件分类（直接回车整理所有大文件）: ").strip()
                if category:
                    files_to_organize = [f for f in large_file_list if f["category"] == category]
                else:
                    files_to_organize = large_file_list

                manager.organize_files(files_to_organize)
                files_info = manager.scan_download_directory()
            else:
                print("没有大文件需要整理")
        elif choice == "6":
            manager.create_cloud_sync_script()
        elif choice == "7":
            files_info = manager.scan_download_directory()
            manager.display_files_summary(files_info)
            manager.display_files_list(files_info)
        elif choice == "0":
            print("\n👋 感谢使用，再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()
