import os
import io
import csv
import requests
import zipfile

def download_edinet_documents():
  api_key = ''
  docID = 'S100SP8X'
  # ダウンロード先フォルダ
  filer_name_dir = 'docs'
  os.makedirs(filer_name_dir, exist_ok=True)
  # EDINETからpdfを取得
  url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{docID}?type=2&Subscription-Key={api_key}"
  response = requests.request("GET", url)
  with open(os.path.join(filer_name_dir, f"{docID}.pdf"), "wb") as f:
    f.write(response.content)
  # EDINETからzipを取得
  url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{docID}?type=5&Subscription-Key={api_key}"
  response = requests.request("GET", url)
  # ZIPファイルを解凍する
  with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extractall(filer_name_dir)
  return


# ダウンロードした文書から必要な情報をCSVファイルから抽出する
def extract_content_from_csv():
  content_data = {}
  filer_name_dir = 'docs'
  # 解凍したzipのXBRL_TO_CSVフォルダ内のjpcrpから始まるcsvファイルを解析する
  for file in os.listdir(os.path.join(filer_name_dir, "XBRL_TO_CSV")):
    if file.startswith("jpcrp") and file.endswith(".csv"):
      csv_path = os.path.join(filer_name_dir, "XBRL_TO_CSV", file)
      with open(csv_path, "r", encoding="utf-16") as csv_file:
        reader = csv.reader(csv_file, delimiter="\t")
        for row in reader:
          # 要素ID＆コンテキストIDで検索
          # 売上
          if row[0] == 'jpcrp_cor:NetSalesSummaryOfBusinessResults' and row[2] == 'CurrentYearDuration_NonConsolidatedMember':
            content_data["netsale"] = row[8]
          # １～４期前の売上
          if row[0] == 'jpcrp_cor:NetSalesSummaryOfBusinessResults' and row[2] == 'Prior1YearDuration_NonConsolidatedMember':
            content_data["netsale1"] = row[8]
          if row[0] == 'jpcrp_cor:NetSalesSummaryOfBusinessResults' and row[2] == 'Prior2YearDuration_NonConsolidatedMember':
            content_data["netsale2"] = row[8]
          if row[0] == 'jpcrp_cor:NetSalesSummaryOfBusinessResults' and row[2] == 'Prior3YearDuration_NonConsolidatedMember':
            content_data["netsale3"] = row[8]
          if row[0] == 'jpcrp_cor:NetSalesSummaryOfBusinessResults' and row[2] == 'Prior4YearDuration_NonConsolidatedMember':
            content_data["netsale4"] = row[8]
          # 純利益
          elif row[0] == 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults' and row[2] == 'CurrentYearDuration':
            content_data["profit"] = row[8]
          # １～４期前の純利益
          elif row[0] == 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults' and row[2] == 'Prior1YearDuration':
            content_data["profit1"] = row[8]
          elif row[0] == 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults' and row[2] == 'Prior2YearDuration':
            content_data["profit2"] = row[8]
          elif row[0] == 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults' and row[2] == 'Prior3YearDuration':
            content_data["profit3"] = row[8]
          elif row[0] == 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults' and row[2] == 'Prior4YearDuration':
            content_data["profit4"] = row[8]
  return content_data


# pdfとcsvをダウンロード
download_edinet_documents()
# csvから必要なデータを取得
content_data = extract_content_from_csv()

print(f"売上：{content_data['netsale']} {int(content_data['netsale']) / int(content_data['netsale1'])}") 
print(f"売上：{content_data['netsale1']} {int(content_data['netsale1']) / int(content_data['netsale2'])}") 
print(f"売上：{content_data['netsale2']} {int(content_data['netsale2']) / int(content_data['netsale3'])}") 
print(f"売上：{content_data['netsale3']} {int(content_data['netsale3']) / int(content_data['netsale4'])}") 
print(f"売上：{content_data['netsale4']}") 

print(f"純利益：{content_data['profit']} {int(content_data['profit']) / int(content_data['profit1'])}") 
print(f"純利益：{content_data['profit1']} {int(content_data['profit1']) / int(content_data['profit2'])}") 
print(f"純利益：{content_data['profit2']} {int(content_data['profit2']) / int(content_data['profit3'])}") 
print(f"純利益：{content_data['profit3']}  {int(content_data['profit3']) / int(content_data['profit4'])}")
print(f"純利益：{content_data['profit4']}") 