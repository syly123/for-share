import os
import shutil

root_path = r"C:\your\root\path"  # 適宜変更
result_root = os.path.join(root_path, "Result")

category_keywords = ["Business", "Corporate", "Tax"]
destination_keywords = ["HD", "SEJ", "SEI"]

# カテゴリフォルダ（2.Businessなど）を取得
category_folders = [
    f
    for f in os.listdir(root_path)
    if os.path.isdir(os.path.join(root_path, f))
    and any(kw in f for kw in category_keywords)
]

for cat_folder in category_folders:
    cat_path = os.path.join(root_path, cat_folder)

    for subfolder in os.listdir(cat_path):
        # "HD", "SEJ", "SEI" を名前に含むサブフォルダを探す（例：2.1 HD など）
        for keyword in destination_keywords:
            if keyword in subfolder:
                src = os.path.join(cat_path, subfolder)
                dst = os.path.join(
                    result_root, keyword, cat_folder
                )  # 例：Result/HD/2.Business
                os.makedirs(dst, exist_ok=True)

                for item in os.listdir(src):
                    src_item = os.path.join(src, item)
                    dst_item = os.path.join(dst, item)

                    try:
                        if os.path.isfile(src_item):
                            shutil.copy2(src_item, dst_item)
                        elif os.path.isdir(src_item):
                            shutil.copytree(
                                src_item, os.path.join(dst, item), dirs_exist_ok=True
                            )
                    except Exception as e:
                        print(f"コピー失敗: {src_item} → {dst_item}, 理由: {e}")
