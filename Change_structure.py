import os
import shutil

# 元のルートパスとResult保存先
root_path = r"C:\your\root\path"
result_root = os.path.join(root_path, "Result")

# キーワードでカテゴリーフォルダを識別
category_keywords = ["Business", "Corporate", "Tax"]
destination_keywords = ["HD", "SEJ", "SEI"]

# Businessなどを含むカテゴリーフォルダを検索
category_folders = [
    f
    for f in os.listdir(root_path)
    if os.path.isdir(os.path.join(root_path, f))
    and any(kw in f for kw in category_keywords)
]

# コピー処理
for cat_folder in category_folders:
    cat_path = os.path.join(root_path, cat_folder)

    for subfolder in os.listdir(cat_path):
        if subfolder in destination_keywords:
            source_subfolder = os.path.join(cat_path, subfolder)

            # コピー先のパス：Result/HD/2.Business など
            dest_sub_base = os.path.join(result_root, subfolder, cat_folder)
            os.makedirs(dest_sub_base, exist_ok=True)

            for item in os.listdir(source_subfolder):
                src_item_path = os.path.join(source_subfolder, item)
                dst_item_path = os.path.join(dest_sub_base, item)

                try:
                    if os.path.isfile(src_item_path):
                        shutil.copy2(src_item_path, dst_item_path)
                    elif os.path.isdir(src_item_path):
                        shutil.copytree(
                            src_item_path,
                            os.path.join(dest_sub_base, item),
                            dirs_exist_ok=True,
                        )
                except Exception as e:
                    print(f"コピー失敗: {src_item_path} → {dst_item_path}, 理由: {e}")
