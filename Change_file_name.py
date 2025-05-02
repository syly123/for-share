import os
import re

# 対象のフォルダを指定（例：カレントディレクトリ）
target_folder = "path/to/your/folder"
not_matched_file = os.path.join(target_folder, "Not matched.txt")

# パターン：[数字.数字...] [Finance]_[数字.数字...]_[根幹名]_[202xxxxx]
pattern = re.compile(r"^\d+(?:\.\d+)* Finance_\d+(?:\.\d+)*_([^_]+)_202\d+")

matched_core_names = []
not_matched = []

for root, dirs, files in os.walk(target_folder):
    for filename in files:
        if filename == "Not matched.txt":
            continue  # 自分自身は除く
        match = pattern.match(filename)
        if match:
            core_name = match.group(1)
            matched_core_names.append(core_name)
        else:
            not_matched.append(os.path.join(root, filename))

# 結果出力
print("抽出された根幹ファイル名:")
for name in matched_core_names:
    print(name)

# Not matched.txt に出力
with open(not_matched_file, "w", encoding="utf-8") as f:
    for path in not_matched:
        f.write(path + "\n")

print(f"\nマッチしなかったファイルは {not_matched_file} に出力されました。")
