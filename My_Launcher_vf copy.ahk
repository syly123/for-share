#Requires AutoHotkey v2

global SearchResults := [] ; 検索結果を保持する配列
global TsvFilePath := "C:\Users\tatsu\Documents\for-share\sample.tsv" ; 検索対象のTSVファイルのパス
global MyGui := "" ; GUIオブジェクトを明示的に初期化
global WindowActive := false ; ウィンドウが表示中かどうかを管理

; Win + Shift + Spaceで検索ボックスを表示するホットキー
#+Space::
{
    global MyGui, WindowActive ; グローバル変数を宣言

    ; GUIオブジェクトが既に存在する場合は破棄して再作成
    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    WindowActive := true ; ウィンドウ表示中

    MyGui := Gui()
    MyGui.SetFont("s12") ; フォント設定

    ; 検索ボックスを作成
    SearchBox := MyGui.Add("Edit", "vSearchBox w600 h40", "")
    SearchBox.OnEvent("Change", SearchTsv) ; 入力内容が変更された際のイベント

    ; リストボックスを作成
    ResultList := MyGui.Add("ListBox", "r10 vResultList w800 h300", [])

    ; 選択ボタンを作成
    MyGui.Add("Button", "y+10 Default", "詳細を見る").OnEvent("Click", ShowDetails)

    ; GUI全体をEscキーで閉じる処理を設定
    MyGui.OnEvent("Close", HandleEsc)

    ; ホットキーを有効化
    Hotkey("Up", HandleKeyUp, "On")
    Hotkey("Down", HandleKeyDown, "On")
    Hotkey("Enter", HandleKeyEnter, "On")
    Hotkey("Esc", HandleEsc, "On")

    MyGui.Show("x400 y200") ; GUIを表示
}

SearchTsv(*) {
    global SearchResults, TsvFilePath, MyGui

    SearchText := MyGui["SearchBox"].Text ; 検索ボックスの入力を取得

    ; 検索ボックスが空の場合は処理を終了
    if (SearchText = "") {
        MyGui["ResultList"].Delete() ; リストボックスをクリア
        return
    }

    SearchResults := [] ; 検索結果を初期化

    ; TSVファイルを読み取る
    Loop Read, TsvFilePath
    {
        ; 行をタブで分割
        LineData := StrSplit(A_LoopReadLine, "`t")
        if (LineData.Length < 5) ; 列が不足している場合は無視
            continue

        FolderOrFile := LineData[1]
        FileName := LineData[2]
        FilePath := LineData[3]
        CreationDate := LineData[4]
        UpdateDate := LineData[5]

        ; 検索文字がファイル名またはパスに含まれる場合、結果に追加
        if (InStr(FileName, SearchText) || InStr(FilePath, SearchText)) {
            SearchResults.Push(FileName " - " FilePath) ; ファイル名とパスの形式で格納
        }
    }

    ; 配列をリストボックスに一括設定
    ResultList := MyGui["ResultList"]
    ResultList.Delete() ; 既存アイテムを削除
    ResultList.Add(SearchResults) ; 配列を直接リストボックスに渡す
}

HandleKeyUp(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive ; ウィンドウが非表示なら無効
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Max(ResultList.Value - 1, 1) ; 上矢印キーで移動
}

HandleKeyDown(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive ; ウィンドウが非表示なら無効
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Min(ResultList.Value + 1, SearchResults.Length) ; 下矢印キーで移動
}

HandleKeyEnter(*) {
    global MyGui, WindowActive
    if !WindowActive ; ウィンドウが非表示なら無効
        return
    ShowDetails() ; Enterキーで詳細を表示
}

HandleEsc(*) {
    global MyGui, WindowActive
    WindowActive := false ; ウィンドウが非表示状態
    MyGui.Destroy() ; EscキーでGUIを閉じる

    ; ホットキーを無効化
    Hotkey("Up", HandleKeyUp, "Off")
    Hotkey("Down", HandleKeyDown, "Off")
    Hotkey("Enter", HandleKeyEnter, "Off")
    Hotkey("Esc", HandleEsc, "Off")
}

ShowDetails(*) {
    global SearchResults, MyGui

    SelectedIndex := MyGui["ResultList"].Value ; 選択されたアイテムのインデックスを取得
    if (SelectedIndex > 0) {
        ; 選択された結果の詳細情報を取得
        SelectedResult := SearchResults[SelectedIndex]

        ; 詳細をメッセージボックスに表示
        MsgBox("選択された項目: " SelectedResult)
    }
}