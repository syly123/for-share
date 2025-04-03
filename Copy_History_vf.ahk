#Requires AutoHotkey v2

global ClipboardHistory := []
global MyGui ; グローバル変数として宣言

; クリップボードの変更を監視して履歴を記録
SetTimer MonitorClipboard, 100

MonitorClipboard() {
    static LastClipboard := ""
    if (A_Clipboard != LastClipboard && StrLen(A_Clipboard)) {
        LastClipboard := A_Clipboard
        AddToHistory(A_Clipboard)
    }
}

AddToHistory(clip) {
    global ClipboardHistory
    ; 指定項目がすでに存在するか確認し削除
    for index, item in ClipboardHistory {
        if (item = clip) { ; 一致する場合
            ClipboardHistory.RemoveAt(index) ; 削除
            break ; 最初に見つけたものだけ削除して終了
        }
    }
    ClipboardHistory.InsertAt(1, clip) ; リストの先頭に追加
}

; Enterキー押下時のコールバック関数
EnterPressed(*) {
    global ClipboardHistory, MyGui
    SelectedItem := MyGui["ClipboardList"].Text ; リストボックスの変数名で選択項目を取得
    if SelectedItem != "" { ; 有効な選択項目か確認
        A_Clipboard := SelectedItem ; クリップボードにコピー
        Send "^v" ; 貼り付け
        AddToHistory(SelectedItem) ; 選択された履歴を最上部に移動
        MyGui.Destroy() ; GUIを閉じる
    }
}

; Ctrl+Win+Vで履歴を表示するホットキー
^#v::
{
    global ClipboardHistory, MyGui
    MyGui := Gui() ; GUIオブジェクトをグローバルに保持
    MyGui.SetFont("s12") ; フォント設定

    ; リストボックスを作成して履歴を表示
    MyGui.Add("ListBox", "vClipboardList w400 h300", ClipboardHistory)

    ; デフォルトの不可視ボタンを作成し、Enterキーでイベント処理
    MyGui.Add("Button", "y-30 Default").OnEvent("Click", EnterPressed)

    MyGui.Show()
}

; Shift + Ctrl + Win + Vで履歴をファイルに保存するホットキー
+^#v::
{
    global ClipboardHistory, FilePath := A_ScriptDir "\ClipboardHistory.txt"
    FileDelete(FilePath) ; 古い履歴ファイルを削除
    for item in ClipboardHistory {
        FileAppend(item "`n", FilePath) ; ファイルに履歴を書き込む
    }
    MsgBox("クリップボード履歴を " FilePath " に保存しました。")
}

