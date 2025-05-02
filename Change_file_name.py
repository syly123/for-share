import os
import re

# 対象フォルダを指定
target_folder = "path/to/your/folder"
not_matched_file = os.path.join(target_folder, "Not matched.txt")

# パターンの定義（_202で終わる前の文字列をグループ化）
pattern = re.compile(r"^\d+(?:\.\d+)* Finance_\d+(?:\.\d+)*_(.+?)_202\d+")

not_matched = []

for root, dirs, files in os.walk(target_folder):
    for filename in files:
        if filename == "Not matched.txt":
            continue  # 自分自身は除外

        name, ext = os.path.splitext(filename)
        match = pattern.match(name)
        if match:
            core_name = match.group(1)
            new_filename = core_name + ext
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)

            # 同名ファイルが存在する場合は _1, _2 で重複回避
            if os.path.exists(new_path):
                count = 1
                while True:
                    alt_name = f"{core_name}_{count}{ext}"
                    new_path = os.path.join(root, alt_name)
                    if not os.path.exists(new_path):
                        break
                    count += 1

            os.rename(old_path, new_path)
        else:
            not_matched.append(os.path.join(root, filename))

# マッチしなかったファイルを記録
with open(not_matched_file, "w", encoding="utf-8") as f:
    for path in not_matched:
        f.write(path + "\n")

print("✅ リネーム完了。マッチしなかったファイルは Not matched.txt に出力しました。")
