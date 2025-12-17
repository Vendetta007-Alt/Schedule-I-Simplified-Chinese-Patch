import os
import sys
import UnityPy
import tkinter as tk
from tkinter import filedialog

# --- 配置区 ---
# 要被替换的目标字体名称列表 (固定)
TARGET_FONT_NAMES = [
    "LiberationSans", "OpenSans-Bold", "OpenSans-BoldItalic",
    "OpenSans-ExtraBold", "OpenSans-ExtraBoldItalic", "OpenSans-Italic",
    "OpenSans-Light", "OpenSans-LightItalic", "OpenSans-Medium",
    "OpenSans-MediumItalic", "OpenSans-Regular", "OpenSans-SemiBold",
    "OpenSans-SemiBoldItalic"
]

# 输入文件的相对路径和文件名
INPUT_SUBDIR = "Schedule I_Data"
INPUT_FILENAME = "sharedassets0.assets"
# --- 配置区结束 ---

def replace_font_in_asset(source_asset_path, target_asset_path, new_font_path):
    """
    替换 Unity 资源文件中的指定字体。

    Args:
        source_asset_path (str): 读取的原始（或备份的）Unity 资源文件路径。
        target_asset_path (str): 输出修改后的新资源文件路径。
        new_font_path (str): 要替换成的新字体文件路径 (.ttf, .otf 等)。
    """
    # 读取新的字体数据（二进制方式读取）
    try:
        with open(new_font_path, "rb") as f:
            new_font_data = f.read()
        print(f"成功读取新字体: {os.path.basename(new_font_path)}")
    except FileNotFoundError:
        print(f"错误：找不到选择的字体文件 '{new_font_path}'")
        return False
    except Exception as e:
        print(f"错误：读取字体文件 '{new_font_path}' 时发生错误: {e}")
        return False

    print(f"将在资源文件中查找并替换以下目标字体：")
    # 为了美观，分行打印目标字体
    for i in range(0, len(TARGET_FONT_NAMES), 4):
         print("  " + ", ".join(TARGET_FONT_NAMES[i:i+4]))
    print("-" * 30) # 分隔线

    # 加载 assets 文件
    try:
        env = UnityPy.load(source_asset_path)
        print(f"成功加载资源文件: {os.path.basename(source_asset_path)}")
    except Exception as e:
        print(f"错误：加载 Unity 文件 '{source_asset_path}' 时发生错误: {e}")
        return False

    replaced_count = 0 # 用于计算实际替换了多少个字体对象
    processed_count = 0 # 用于计算处理了多少个字体对象

    # 遍历所有的对象，查找 Font 类型的对象
    print("开始遍历资源对象并替换字体...")
    for obj in env.objects:
        if obj.type.name == "Font":
            processed_count += 1
            try:
                font_obj = obj.read()
                # 检查当前字体对象的名称是否在我们要替换的目标列表中
                if font_obj.m_Name in TARGET_FONT_NAMES:
                    print(f"  找到并替换字体: {font_obj.m_Name} (PathID: {obj.path_id})")
                    font_obj.m_FontData = new_font_data # 替换字体数据
                    font_obj.save() # 保存对该对象的修改
                    replaced_count += 1
                # else: # 如果需要调试，可以取消注释下一行
                #     print(f"  跳过字体: {font_obj.m_Name} (PathID: {obj.path_id})")

            except Exception as e:
                # 处理读取或保存单个字体对象时可能出现的错误
                font_name_str = getattr(font_obj, 'm_Name', '未知名称') if 'font_obj' in locals() else '未知对象'
                print(f"警告：处理字体对象 (PathID: {obj.path_id}, 可能名称: {font_name_str}) 时出错: {e}")
                # 选择继续处理下一个对象

    print("-" * 30) # 分隔线

    if replaced_count == 0:
         print(f"处理了 {processed_count} 个字体对象，但在资源文件中未找到任何名称匹配的目标字体进行替换。")
         # 虽然没有替换，但还是需要保存文件（因为UnityPy可能做了其他内部更改）
         # 或者可以选择不保存，直接退出。这里选择保存。

    # 将修改后的 assets 保存到新的文件中
    try:
        print(f"正在将修改后的资源保存到: {os.path.basename(target_asset_path)}...")
        with open(target_asset_path, "wb") as f:
            # UnityPy 的 save() 方法可能有多种形式，对于 assets 文件，
            # env.file.save() 通常是正确的。
            f.write(env.file.save())
        print(f"修改后的资源已成功保存！")
    except Exception as e:
        print(f"错误：保存修改后的 Unity 文件 '{target_asset_path}' 时发生严重错误: {e}")
        return False

    if replaced_count > 0:
        print(f"字体替换完成！总共检测到 {processed_count} 个字体对象，成功替换了 {replaced_count} 个目标字体。")

    return True # 表示成功

def main():
    print("--- 字体替换工具 ---")

    # 1. 确定输入文件路径
    current_dir = os.getcwd() # 获取当前工作目录
    input_dir = os.path.join(current_dir, INPUT_SUBDIR)
    original_file_path = os.path.join(input_dir, INPUT_FILENAME)
    backup_file_path = original_file_path + ".bak"

    print(f"脚本执行目录: {current_dir}")
    print(f"目标资源文件: {original_file_path}")

    # 检查输入文件是否存在
    if not os.path.exists(original_file_path):
        print(f"\n错误：找不到目标资源文件 '{original_file_path}'")
        print(f"请确保你在正确的目录下运行此脚本，并且 '{INPUT_SUBDIR}' 子目录及 '{INPUT_FILENAME}' 文件存在。")
        input("按 Enter 键退出...")
        sys.exit(1)

    # 2. 弹出文件浏览窗口选择新字体
    try:
        root = tk.Tk()
        root.withdraw() # 隐藏 Tkinter 的根窗口
        print("\n请在弹出的窗口中选择要替换成的新字体文件 (.ttf 或 .otf)...")
        new_font_path = filedialog.askopenfilename(
            title="选择要替换成的新字体文件",
            filetypes=[("Font Files", "*.ttf *.otf"), ("All Files", "*.*")]
        )
        root.destroy() # 关闭 Tkinter 实例
    except Exception as e:
        print(f"\n错误：无法打开字体选择窗口: {e}")
        print("请检查您的图形环境是否配置正确。")
        input("按 Enter 键退出...")
        sys.exit(1)


    if not new_font_path:
        print("\n操作已取消：未选择任何字体文件。")
        input("按 Enter 键退出...")
        sys.exit(0)

    print(f"已选择新字体: {new_font_path}")

    # 3. 备份原文件
    print(f"\n正在备份原文件 '{INPUT_FILENAME}' -> '{INPUT_FILENAME}.bak'...")
    try:
        if os.path.exists(backup_file_path):
            print(f"警告：备份文件 '{backup_file_path}' 已存在。将会覆盖它。")
            os.remove(backup_file_path)
        os.rename(original_file_path, backup_file_path)
        print(f"已成功备份原文件至: {backup_file_path}")
    except OSError as e:
        print(f"\n错误：备份原文件时发生错误: {e}")
        print("请检查文件权限或是否被其他程序占用。")
        input("按 Enter 键退出...")
        sys.exit(1)

    # 4. 执行替换操作 (读取备份文件，写入原文件名)
    success = False
    try:
        success = replace_font_in_asset(backup_file_path, original_file_path, new_font_path)
    except Exception as e:
        print(f"\n处理过程中发生未预料的严重错误: {e}")
        # 尝试恢复
        print("\n!!! 发生严重错误，尝试从备份恢复原文件 !!!")
        try:
            if os.path.exists(backup_file_path):
                 # 如果新文件创建失败或损坏，可能需要先删除它
                 if os.path.exists(original_file_path):
                      print(f"正在删除可能已损坏的文件: {original_file_path}")
                      os.remove(original_file_path)
                 # 恢复备份
                 print(f"正在将 '{backup_file_path}' 恢复为 '{original_file_path}'")
                 os.rename(backup_file_path, original_file_path)
                 print("已成功从备份恢复原文件。")
            else:
                print("错误：找不到备份文件，无法自动恢复。请手动检查！")
        except OSError as restore_e:
            print(f"错误：恢复原文件时失败: {restore_e}")
            print(f"请手动将 '{backup_file_path}' 重命名为 '{original_file_path}'。")
    finally:
         if success:
             print(f"\n--- 操作成功完成 ---")
         else:
             print(f"\n--- 操作失败 ---")

         input("按 Enter 键退出...")
         sys.exit(0 if success else 1)

if __name__ == "__main__":
    # 确保 UnityPy 存在
    try:
        import UnityPy
    except ImportError:
        print("错误：找不到 UnityPy 模块。")
        print("请先安装 UnityPy: pip install UnityPy")
        input("按 Enter 键退出...")
        sys.exit(1)

    # 确保 tkinter 可用 (通常内建，但在某些最小化环境可能没有)
    try:
        import tkinter
        import tkinter.filedialog
    except ImportError:
        print("错误：找不到 tkinter 模块。")
        print("Tkinter 通常是 Python 的标准库，请确保您的 Python 安装完整。")
        print("在某些 Linux 发行版上，可能需要单独安装，例如：sudo apt-get install python3-tk")
        input("按 Enter 键退出...")
        sys.exit(1)

    main()