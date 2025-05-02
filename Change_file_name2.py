import os
import re

# 対象フォルダ（必要に応じて変更）
target_dir = "your_directory_path_here"

# 正規表現パターン：ファイル名をマッチングし、根幹ファイル名を抽出
pattern = re.compile(r"^(?:\d+(?:\.\d+)*\s)?Finance_\d+(?:\.\d+)*_(.+?)_202\d+")

# 末尾の _202xxxxx を削除するパターン
remove_trailing_date = re.compile(r"_(202\d{5,})$")

# 先頭の数字とピリオドの組み合わせ（3桁以上）+ 半角スペースを削除
remove_leading_numbers = re.compile(r"^([\d\.]{3,})\s+(.*)")

# Finance_とその前の部分を削除するパターン（Finance_とその後の数字ピリオド群も削除）
remove_finance_part = re.compile(r"^(?:\d+(?:\.\d+)*\s)?Finance_\d+(?:\.\d+)*_")

# マッチしなかったファイル名を記録するリスト
not_matched = []

# フォルダ内のファイルを探索
for root, _, files in os.walk(target_dir):
    for filename in files:
        old_path = os.path.join(root, filename)
        name, ext = os.path.splitext(filename)

        # 正規表現でファイル名をマッチング
        match = pattern.match(name)
        if match:
            # マッチした場合は、根幹ファイル名を抽出
            new_name = match.group(1) + ext
        else:
            # マッチしなかった場合、後処理を行う
            modified_name = name
            # 末尾の _202xxxxx を削除
            modified_name = remove_trailing_date.sub("", modified_name)
            # 先頭の数字 + ピリオド + 半角スペース を削除（ピリオドが含まれている場合のみ）
            match_leading = remove_leading_numbers.match(modified_name)
            if match_leading and "." in match_leading.group(1):
                modified_name = match_leading.group(2)
            # Finance_とその前の部分を削除
            modified_name = remove_finance_part.sub("", modified_name)
            new_name = modified_name + ext
            not_matched.append(filename)

        # ファイル名が変わるときのみリネーム
        if filename != new_name:
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

# マッチしなかったファイル名を記録
with open(os.path.join(target_dir, "Not matched.txt"), "w", encoding="utf-8") as f:
    for name in not_matched:
        f.write(name + "\n")
