import xlwings as xw

# Excelファイルを開く
wb = xw.Book('your_file.xlsx')

# シート名のリスト
sheets = ['A', 'B', 'C']

# 各シートの8行目に5行挿入する処理
for sheet_name in sheets:
    sheet = wb.sheets[sheet_name]
    # 8行目に5行挿入
    sheet.api.Rows("8:12").Insert()

# 保存して閉じる
wb.save()
wb.close()
