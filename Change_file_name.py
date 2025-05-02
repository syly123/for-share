import os
import re

# 対象フォルダのパス
target_folder = "path/to/your/folder"
not_matched_file = os.path.join(target_folder, "Not matched.txt")

# 正規表現パターン：指定された形式にマッチするもの
pattern = re.compile(r"^(\d+(?:\.\d+)*) Finance_\d+(?:\.\d+)*_([^_]+)_202\d+")

not_matched = []

for root, dirs, files in os.walk(target_folder):
    for filename in files:
        if filename == "Not matched.txt":
            continue  # 自分自身はスキップ

        match = pattern.match(filename)
        if match:
            core_name = match.group(2)
            ext = os.path.splitext(filename)[1]
            new_filename = core_name + ext
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)

            # 同名ファイルがすでにある場合はスキップ（または "_1" などで区別してもよい）
            if os.path.exists(new_path):
                count = 1
                while True:
                    new_filename_alt = f"{core_name}_{count}{ext}"
                    new_path = os.path.join(root, new_filename_alt)
                    if not os.path.exists(new_path):
                        break
                    count += 1

            os.rename(old_path, new_path)
        else:
            not_matched.append(os.path.join(root, filename))

# マッチしなかったファイルの記録
with open(not_matched_file, "w", encoding="utf-8") as f:
    for path in not_matched:
        f.write(path + "\n")

print(
    "ファイル名のリネーム完了。マッチしなかったファイルは Not matched.txt に出力されました。"
)
