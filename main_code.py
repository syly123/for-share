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
