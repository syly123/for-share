import win32com.client
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# from tkinter import filedialog
import re
import os
import pyperclip
import time
import json

# import Auto_Kairan_Paris


def get_toRecipient(mail):
    to_recipients = []
    for recipient in mail.Recipients:
        if recipient.Type == 1:  # To受信者
            ad = recipient.Address
            # print(ad)
            if "EXCHANGELABS" in str(ad).upper():
                try:
                    # print(recipient.AddressEntry)
                    ad = recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress
                except Exception as e:
                    # print(e)
                    ad = "gs.com"
            to_recipients.append(ad)
    return to_recipients


def list_subdirectories(directory):
    # ディレクトリ内のすべてのフォルダ名を格納するリスト
    subdirectories = []
    # 指定されたディレクトリ内のすべてのファイルとフォルダを取得
    for entry in os.listdir(directory):
        # フルパスを取得
        full_path = os.path.join(directory, entry)
        # エントリがディレクトリかどうかをチェック
        if os.path.isdir(full_path):
            subdirectories.append(entry)
    return subdirectories


def read_json(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file ({json_path}) was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file ({json_path}).")
        return None


def contains_all_parts(text, kw):
    # 文字列を「アルファベットと数字」以外で分割
    parts = re.split(r"\W+", kw)
    # 空の文字列を除去
    parts = [part for part in parts if part]
    # print(parts)
    # 各部分が元の文字列に含まれているかをチェック
    for part in parts:
        if part not in text:
            return False
    return True


def search_first_matching_folder(
    root_folder, search_strings, ignore_list=["dummy dummy"]
):
    # ignoreを空リストにするとすべてを無視してしまう
    # フォルダ内に"kw1,kw2"形式で記載した検索文字一覧をすべて含むフォルダがあればパス
    search_list = search_strings.lower().split(",")
    # print(search_list)

    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check if all search strings are in the current directory path
        if all(
            search_string in (dirpath.lower() + "\\") for search_string in search_list
        ):
            print(dirpath.lower() + "\\")
            for ignore in ignore_list:
                if ignore not in dirpath:
                    return dirpath
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            # print(full_path)
            # Check if all search strings are in any of the subdirectory names
            if all(search_string in full_path.lower() for search_string in search_list):
                for ignore in ignore_list:
                    if ignore not in full_path:
                        return full_path
    return ""  # Return empty string if no matching folder is found


def search_save_dir_by_subject(search_dir, info_dic, subject, ignore_dir):
    # 件名に対して、「ファイル名検索用文字」と「件名検索用文字」の二つで検索し、
    # 両方マッチする場合は後者を優先
    break_all = False
    save_folder_by_subject = ""

    for key, value in info_dic.items():
        # print("start search for key: ", key)
        key = key.lower()

        for filename_rule in value[0]:
            filename_rule = filename_rule.lower()
            if contains_all_parts(
                subject, filename_rule
            ):  # 今はファイル名ではなく件名で判断
                save_folder_by_subject = search_first_matching_folder(
                    search_dir, key, ignore_dir
                )
                print(
                    f"件名検索>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{key}---{save_folder_by_subject}"
                )
                break_all = True
                break

        if break_all:
            break

        if len(value) > 1:
            for subject_rule in value[1]:
                subject_rule = subject_rule.lower()
                if contains_all_parts(subject, subject_rule):
                    save_folder_by_subject = search_first_matching_folder(
                        search_dir, key, ignore_dir
                    )
                    print(
                        f"件名検索>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{key}---{save_folder_by_subject}"
                    )
                    break_all = True
                    break

        if break_all:
            break
    if save_folder_by_subject == "":
        print("件名検索 xxxxxxxxxxxxx No match")
        return False
    else:
        return save_folder_by_subject


def search_save_dir_by_filename(search_dir, info_dic, attachment, ignore_dir):
    break_all = False
    save_folder_by_filename = ""
    for key, value in info_dic.items():
        key = key.lower()
        for filename_rule in value[0]:
            filename_rule = filename_rule.lower()
            if contains_all_parts(
                str(attachment.FileName).lower(), filename_rule
            ):  # 要変更:今はファイル名ではなく件名で判断している
                save_folder_by_filename = search_first_matching_folder(
                    search_dir, key, ignore_dir
                )
                break_all = True
                break
        if break_all:
            break
    if save_folder_by_filename == "":
        return False
    else:
        return {"filename": save_folder_by_filename, "key": key}


def find_pj(mail, pj_list):
    categories = str(mail.Categories)
    matched_pj = "None"
    for pj in pj_list:
        if pj in categories:
            if matched_pj != "None":
                return "ERROR:複数PJラベル"  # エラーを返す、既にPJラベル済なのに再マッチ+1メールが複数PJ
            else:
                matched_pj = pj
    return matched_pj


def save_attachment(mail, json_info, pj, calendar):
    forDebug = [0, 0, 0, 0, 0]
    saved_info = []  # リストのリスト形式で、ファイルごとの格納先と付随情報
    categories = str(mail.Categories)
    try:
        if pj == "ERROR:複数PJラベル":
            return ["ERROR:複数PJラベル", saved_info]
        elif pj == "None":
            return [
                "ERROR:PJラベル無し",
                saved_info,
            ]  # PJラベルが見つからなかった場合はエラーを返す

        else:
            pj_json_info = json_info[pj]
            # save_dir_info = pj_json_info["save_dir_info"]
            save_dir_info_by_filename = pj_json_info["save_dir_info_by_filename"]
            ignore_dir = pj_json_info["ignore_dir"]
            domain_dic = pj_json_info["domain_dic"]
            search_dir = pj_json_info["search_dir"]
            name_dic = pj_json_info["name_dic"]
            # print(search_dir)

        body = mail.Body.lower()
        original_sub = mail.Subject
        subject = original_sub.lower()
        body_before_from = get_current_msg(body)  # 今回の文のメール本文のみ
        # if re.search('polestar', body + subject, flags=re.IGNORECASE):
        #     print(mail.categories)
        if (
            "意見" in categories or "書類" in categories or "回覧" in categories
        ) and "if not" in categories:
            print(original_sub)
            to_recipients = get_toRecipient(mail)

            # search_dir = r'\\firmwide.corp.gs.com\ibdroot\projects\IBD-SI\buxaceae2024\931449_1'
            save_folder_by_subject = search_save_dir_by_subject(
                search_dir, save_dir_info_by_filename, subject, ignore_dir
            )

            # もし件名からファイル特定不可能だった場合はUndefinedに格納
            if save_folder_by_subject == False:
                save_folder_by_subject = search_dir + r"\Undefined"

            save_folder = save_folder_by_subject
            sender = find_sender(mail, domain_dic)
            receiver = find_receiver(
                body_before_from, to_recipients, domain_dic, name_dic
            )
            version = find_draft_version(subject, body_before_from)
            is_comments = "意見" in categories
            need_kairan = "回覧" in categories
            new_dir_name = create_dirname(
                mail, sender, receiver, version, is_comments
            )  # is_commentsで帰ってくる値が変わる

            # mail.Categories = mail.Categories + ", '済"
            # mail.Save()

            attachments = mail.Attachments
            no_attachment = True
            break_all = False
            save_folder_by_filename = ""
            new_dir_path = ""

            for attachment in attachments:
                if str(attachment.FileName)[-3:] in [
                    "png",
                    "jpg",
                    "peg",
                ]:  # これらの拡張子は無視
                    continue

                # search_dir = r'\\firmwide.corp.gs.com\ibdroot\projects\IBD-SI\buxaceae2024\931449_1'
                save_folder_by_filename = search_save_dir_by_filename(
                    search_dir, save_dir_info_by_filename, attachment, ignore_dir
                )

                if save_folder_by_filename:
                    save_folder = save_folder_by_filename["filename"]
                    # print("fn sf:", save_folder)

                if is_comments:
                    new_dir_path = (
                        save_folder
                        + r"/"
                        + new_dir_name
                        + r"/"
                        + get_time_str(mail.ReceivedTime)
                        + "_from_"
                        + sender
                    )  # Comments dir 内に各社フォルダ作成
                    query = new_dir_name.replace("_9999", "")

                    if search_first_matching_folder(save_folder, query) != "":
                        # print(query)
                        new_dir_path = (
                            search_first_matching_folder(save_folder, query)
                            + r"/"
                            + get_time_str(mail.ReceivedTime)
                            + "_from_"
                            + sender
                        )  # Comments dir 内に各社フォルタ作成
                else:
                    new_dir_path = save_folder + r"/" + new_dir_name
                pyperclip.copy(new_dir_path.replace("/", "\\"))
                # if not os.path.isdir(new_dir_path):
                if not os.path.isdir(new_dir_path):
                    if save_folder != save_folder_by_subject:
                        print(
                            f"ファイル名検索>>>>>>>>>>>>>>>>>>>>>>>>>{save_folder_by_filename['key']}---{save_folder}"
                        )  # 初めてディレクトリが作られるときの処理
                    os.makedirs(new_dir_path, exist_ok=True)
                    savename = re.sub(
                        r'[<>:"/\\|?*]', "", original_sub
                    )  # 元メール保存する際に名前に変な文字入れない
                    path_to_save = os.path.join(new_dir_path, savename + ".msg")
                    mail.SaveAs(path_to_save, 3)
                    saved_info.append([original_sub, savename + ".msg", path_to_save])

                    # if need_kairan:
                    #     Auto_Kairan_Paris.create_kairan_draft(
                    #         mail, new_dir_path, calendar
                    #     )

                no_attachment = False
                path_to_save = os.path.join(new_dir_path, str(attachment.FileName))
                res = attachment.SaveAsFile(path_to_save)
                saved_info.append([original_sub, attachment.FileName, path_to_save])

            # Body内に指定されたWordがあるならマッチとする方法
            # 回覧とコメントに分け、回覧については件名・Sender・日付を記録し、その際にどのフォルダに属していたかを記録、コメントについては一個前のメールを参照させる
            forDebug[1] = 1
            if no_attachment:
                if is_comments:
                    print("No Comments: ", sender)
                    new_dir_path = (
                        save_folder + r"/" + new_dir_name
                    )  # わざわざsenderフォルタ作らずcomment2486直下にIにメールにメール保存
                    if (
                        search_first_matching_folder(
                            save_folder, new_dir_name.replace("_9999_", "")
                        )
                        != ""
                    ):
                        new_dir_path = search_first_matching_folder(
                            save_folder,
                            new_dir_name.replace("_9999_", ""),
                        )
                    os.makedirs(new_dir_path, exist_ok=True)
                    pyperclip.copy(new_dir_path.replace("/", "\\"))
                    name_to_save = ""
                    if (
                        "no comment" in body_before_from
                        or "no additional comment" in body_before_from
                        or "コメントはございません" in body_before_from
                        or "コメントございません" in body_before_from
                        or "コメントは御座いません" in body_before_from
                        or "コメント御座いません" in body_before_from
                    ):
                        name_to_save = sender + "_NC.msg"
                    else:
                        name_to_save = (
                            get_time_str(mail.ReceivedTime)
                            + "_"
                            + sender
                            + " Comment.msg"
                        )
                    path_to_save = os.path.join(new_dir_path, name_to_save)
                    mail.SaveAs(path_to_save, 3)
                    saved_info.append([original_sub, name_to_save, path_to_save])
                else:
                    new_dir_path = save_folder + r"/" + new_dir_name
                    os.makedirs(new_dir_path, exist_ok=True)
                    pyperclip.copy(new_dir_path.replace("/", "\\"))
                    savename = re.sub(r'[<>:"/\\|?*]', "", original_sub)
                    path_to_save = os.path.join(new_dir_path, savename + ".msg")
                    mail.SaveAs(path_to_save, 3)
                    saved_info.append([original_sub, savename + ".msg", path_to_save])

            mail.Categories = mail.Categories + ", 済"
            mail.Save()
        return ["SUCCESS", saved_info]
    except Exception as e:
        print(forDebug)
        print(e)
        return ["ERROR", saved_info]


def get_current_msg(body):
    msg_list = re.split("regards|sincerely|宜しく|よろしく", body)
    if len(msg_list) < 2:
        return body.split("from:")[0]
    else:
        return msg_list[0]


def get_current_time():
    # タイムスタンプを取得
    timestamp = datetime.now(timezone.utc)

    # JST(日本標準時)に変換
    jst_timezone = timezone(timedelta(hours=9))
    jst_time = timestamp.astimezone(jst_timezone)
    # フォーマットして表示
    formatted_time = jst_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


# 本文の先頭に最も近い(最初に見つかった)リスト内のマッチ要素を返す
def find_top_match(text, word_list):
    nearest_index = len(text)
    nearest_word = ""
    for word in word_list:
        index = text.find(word)
        if index != -1 and index < nearest_index:
            nearest_index = index
            nearest_word = word
    return nearest_word


def find_draft_version(subject, body, ver_list=""):
    # 戻り値:バージョン[例]3rd(文字列)
    if ver_list == "":
        ver_list = [
            "1st",
            "first",
            "2nd",
            "second",
            "3rd",
            "third",
            "3th",
            "4th",
            "5th",
            "semifinal",
            "6th",
            "final",
        ]

    for kw in ver_list:
        if kw.lower() in subject:
            print("ver in sbj: ", kw)
            if kw in ["first"]:
                return "1st"
            elif kw in ["second"]:
                return "2nd"
            elif kw in ["third"]:
                return "3rd"
            else:
                return kw

    # if kw.lower() in body:
    matched = find_top_match(body, ver_list)
    if matched == "":
        print("no version info")
        return
    else:
        print("ver in body: ", matched)
        return matched


def find_receiver(body, to_recipients, domain_dic, name_dic=""):
    # 戻り値:宛先[例]UW-side(文字列)
    receiver = ""

    if name_dic == "":
        name_dic = {
            "All": ["皆様", "関係者", "all", "各位"],
            "UW-side": ["引受", "underwrit", "引き受け", "審査"],
            "Issuer-side": ["発行側", "発行体"],
            "LC": ["弁護士", "法律事務所"],
            "JLM": ["jlm"],
            "GS": ["gs"],
        }

    all_list = []
    # 全リストを統合
    for k, v in name_dic.items():
        all_list = all_list + v
    matched = find_top_match(body, all_list)
    # print("To: ", matched)

    for k, v in name_dic.items():
        if matched in v:
            receiver = k
            break

    # 上記の受取人検索でマッチしなかった場合
    if receiver == "":
        for k, v in domain_dic.items():
            # print(to_recipients[0])
            # 先頭のToに入っているドメインを受け取り者とする
            if v in to_recipients[0]:
                receiver = k

    return receiver


def find_sender(mail, domain_dic):
    sender_ad = mail.SenderEmailAddress
    sender = ""

    if "EXCHANGELABS" in str(sender_ad).upper():
        sender_ad = mail.Sender.GetExchangeUser().PrimarySmtpAddress
        # print(sender_ad)

    for k, v in domain_dic.items():
        if v in sender_ad:
            sender = k

    return sender


def get_time_str(time):
    # timeldmail.ReceivedTime
    mail_date = time
    date_str = mail_date.strftime("%Y%m%d")
    time_str = mail_date.strftime("%H%M")
    date_and_time = date_str + "_" + time_str
    return date_and_time


def get_current_time_num():
    now = datetime.now()
    return [now.year, now.month, now.day, now.hour, now.minute]


def create_dirname(mail, sender, receiver, version, is_comments):
    mail_date = mail.ReceivedTime
    date_str = mail_date.strftime("%Y%m%d")
    time_str = mail_date.strftime("%H%M")
    date_and_time = date_str + "_" + time_str + "_"

    new_dir_name = date_and_time

    # version = ""  # 意図的にversion情報を入れない(案件ごとにトグル)
    if is_comments:
        date = int(mail_date.strftime("%d"))
        hour = int(mail_date.strftime("%H"))
        if hour < 6:
            date = date - 1
        # new_dir_name = mail_date.strftime('%Y%m') + str(date).zfill(2) + '_999999 Comments from All to receiver'
        new_dir_name = (
            mail_date.strftime("%Y%m")
            + str(date).zfill(2)
            + "_9999_Comments from All to "
            + receiver
        )
    else:
        if sender != "":
            new_dir_name = new_dir_name + "_from_" + sender
        if receiver != "":
            new_dir_name = new_dir_name + "_to_" + receiver
        if version != "":
            new_dir_name = new_dir_name + "_" + version + "-draft"

    return new_dir_name
