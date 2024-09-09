import xlwings as xw

# 2つのブックを開く
wb1 = xw.Book('Book1.xlsx')  # コピー元のブック
wb2 = xw.Book('Book2.xlsx')  # コピー先のブック

# コピー元のシートと範囲を指定（例: Sheet1）
source_sheet = wb1.sheets['Sheet1']
source_range = source_sheet.range('A2:F16')

# コピー先のシートを指定（例: Sheet1）
dest_sheet = wb2.sheets['Sheet1']

# 数式をコピー（数式自体をコピーするには .formula を使用）
dest_sheet.range('A2').options(ndim=2).value = source_range.formula

# 保存して閉じる
wb2.save()
wb1.close()
wb2.close()


# 2. 書式をコピー (値とフォーマットは一緒にコピーされる)
source_range.api.Copy()
dest_sheet.range('A2').api.PasteSpecial(Paste=-4122)  # -4122 は「書式」だけを貼り付けるオプション


    # 8～20行の範囲で折りたたまれている行を展開
    for row in range(8, 21):  # 8行目から20行目までの範囲
        if sheet.range(f"A{row}").api.Rows.OutlineLevel > 1:
            # グループ化されている行のみ展開（OutlineLevelが1より大きい場合）
            sheet.api.Rows(row).ShowDetail = True

https://chatgpt.com/share/90acbadf-b30d-4edf-ac01-3c6c8d434c48