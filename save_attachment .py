import win32com.client
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
import os
import pyperclip
import time
import common
import csv
import sys

# 関数をcommonモジュールからインポート
contains_all_parts = common.contains_all_parts
read_json = common.read_json
search_first_matching_folder = common.search_first_matching_folder
search_save_dir_by_subject = common.search_save_dir_by_subject
find_draft_version = common.find_draft_version
find_receiver = common.find_receiver
get_toRecipient = common.get_toRecipient
create_dirname = common.create_dirname
search_save_dir_by_filename = common.search_save_dir_by_filename
find_sender = common.find_sender
get_current_msg = common.get_current_msg
save_attachment = common.save_attachment
find_pj = common.find_pj
get_current_time = common.get_current_time

## 使用例
# json_path = r"C:\Users\mizuta\Src\save_setting_Mstg_02.json"
# json_data = read_json(json_path)
# if json_data:
#    save_dir_info = json_data["save_dir_info"]
#    save_dir_info_by_filename = json_data["save_dir_info_by_filename"]
#    ignore_dir = json_data["ignore_dir"]
#    domain_dic = json_data["domain_dic"]
#    pj_list = ["Mstg", "Paris"]
#    json_info = []
#    all_pj_saved_info = {}

# 以下の処理はjsonファイルの読み込み、設定内容を保持
pj_list = ["Paris"]
json_info = {}
all_pj_saved_info = {}

for pj in pj_list:
    # 全PJの情報を含む辞書を作成
    json_path = r"C:\Users\Tatsuhiko.M\Documents\for-share\save_setting_" + pj + ".json"
    json_data = read_json(json_path)

    # 全PJでJson構造を一致させないとエラーが出る
    if json_data:
        json_info[pj] = {
            "save_dir_info_by_filename": json_data["save_dir_info_by_filename"],
            "ignore_dir": json_data["ignore_dir"],
            "domain_dic": json_data["domain_dic"],
            "search_dir": json_data["search_dir"],
            "name_dic": json_data["name_dic"],
        }
        all_pj_saved_info[pj] = []

# タイムゾーン設定
jst = ZoneInfo("Asia/Tokyo")
utc = ZoneInfo("UTC")

# Outlookアプリケーションのセットアップ
outlook_app = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts = outlook_app.Folders

# 受信トレイ選択・・「6」が受信トレイ
inbox = outlook_app.GetDefaultFolder(6)
calendar = outlook_app.GetDefaultFolder(9)
mails = inbox.Items
mails.Sort("[ReceivedTime]", Descending=True)

max_load = 200  # 読み込むメール数
search_period = 30  # 読み込む日数

for i, mail in enumerate(mails):
    try:
        mail_date = mail.ReceivedTime
        if i >= max_load:
            break
        if mail.Class != 43:  # メールタイプではない場合
            # print("not mail type")
            continue
        if True or mail_date > datetime.now(jst) - timedelta(
            days=search_period
        ):  # 検索期間内のメールのみ処理
            pj = find_pj(mail, pj_list)
            res = save_attachment(mail, json_info, pj, calendar)  # 中心処理
            status = res[0]
            if "ERR" in status:
                print(status + ", " + mail.Subject)
            else:
                saved_info = res[1]
                # print(all_pj_saved_info)
                all_pj_saved_info[pj] = all_pj_saved_info[pj] + saved_info
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print("ERR line: " + str(exception_traceback.tb_lineno) + ", " + str(e))
        continue
