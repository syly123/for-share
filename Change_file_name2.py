import os
import re

target_dir = "your_directory_path_here"

# マッチパターン：正式な命名規則に従っている場合の抽出
pattern = re.compile(r"^(?:\d+(?:\.\d+)*\s)?Finance_\d+(?:\.\d+)*_(.+?)_202\d+")

# 末尾の日付を削除するパターン（例: _20230101）
remove_trailing_date = re.compile(r"_(202\d{5,})$")

# 先頭の数字ピリオド+空白を削除（ピリオドを含むもののみ）
remove_leading_numbers = re.compile(r"^([\d\.]{3,})\s+(.*)")

# Finance_とその前後の数字ピリオド郡を削除
remove_finance_part = re.compile(r"^(?:\d+(?:\.\d+)*\s)?Finance_\d+(?:\.\d+)*_")

# 結果記録
not_matched = []


def process_entry(entry_path, name):
    name_only, ext = os.path.splitext(name)
    match = pattern.match(name_only)
    if match:
        new_name = match.group(1) + ext
    else:
        modified_name = name_only
        # 末尾 _202xxxx 削除
        modified_name = remove_trailing_date.sub("", modified_name)
        # 先頭 数字ピリオド + スペース 削除（ピリオド含む場合のみ）
        m = remove_leading_numbers.match(modified_name)
        if m and "." in m.group(1):
            modified_name = m.group(2)
        # Finance_と前後数字ピリオド削除
        modified_name = remove_finance_part.sub("", modified_name)
        new_name = modified_name + ext
        not_matched.append(name)

    return new_name


for root, dirs, files in os.walk(target_dir, topdown=False):
    # フォルダ処理
    for dirname in dirs:
        old_path = os.path.join(root, dirname)
        new_name = process_entry(old_path, dirname)
        new_path = os.path.join(root, new_name)
        if dirname != new_name and not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Renamed folder: {dirname} → {new_name}")
    # ファイル処理
    for filename in files:
        old_path = os.path.join(root, filename)
        new_name = process_entry(old_path, filename)
        new_path = os.path.join(root, new_name)
        if filename != new_name and not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Renamed file: {filename} → {new_name}")

# マッチしなかった名前の記録
with open(os.path.join(target_dir, "Not matched.txt"), "w", encoding="utf-8") as f:
    for name in not_matched:
        f.write(name + "\n")
