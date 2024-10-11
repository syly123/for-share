import re
from PyPDF2 import PdfReader

def extract_text_between_numbers_and_newline(pdf_path):
    # PDFファイルを読み込む
    reader = PdfReader(pdf_path)
    extracted_texts = []

    # 各ページを繰り返し処理
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()

        # 正規表現で[数字]に続くテキストを取得
        matches = re.findall(r'\[\d+\](.*?)(?:\n|$)', text, re.DOTALL)

        # 結果をリストに追加
        extracted_texts.extend(matches)

    return extracted_texts

# 使用例
pdf_path = "example.pdf"  # ここに対象のPDFファイルのパスを指定
extracted_texts = extract_text_between_numbers_and_newline(pdf_path)

for text in extracted_texts:
    print(text)
