import os
import re

# 対象フォルダ（必要に応じて変更）
target_dir = "your_directory_path_here"

# 正規表現パターン：完全一致形式（マッチすれば根幹ファイル名を抽出）
pattern = re.compile(r"^\d+(?:\.\d+)*\s+Finance_\d+(?:\.\d+)*_([\w\s.-]+)_202\d{5,}$")

# 後処理パターン（マッチしなかったときのみ）
remove_trailing_date = re.compile(r"_(202\d{5,})$")
remove_leading_numbers = re.compile(r"^(\d{3,}(?:\.\d+)+)\s+(.*)")

not_matched = []

for root, _, files in os.walk(target_dir):
    for filename in files:
        old_path = os.path.join(root, filename)
        name, ext = os.path.splitext(filename)

        match = pattern.match(name)
        if match:
            new_name = match.group(1) + ext
        else:
            modified_name = name
            # 末尾の _202xxxxx を削除
            modified_name = remove_trailing_date.sub("", modified_name)
            # 先頭の 3桁以上の数字＋ピリオド＋スペース を削除（ピリオドがない場合は除外）
            match_leading = remove_leading_numbers.match(modified_name)
            if match_leading:
                modified_name = match_leading.group(2)
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
