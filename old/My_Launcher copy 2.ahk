#Requires AutoHotkey v2

global SearchResults := [] ; 検索結果を保持する配列
global TargetFolder := "C:\Users\tatsu\" ; 検索対象のフォルダを指定
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
    SearchBox.OnEvent("Change", SearchFolders) ; 入力内容が変更された際のイベント

    ; リストボックスを作成
    ResultList := MyGui.Add("ListBox", "r5 vResultList w600 h200", [])

    ; 選択ボタンを作成
    MyGui.Add("Button", "y+10 Default", "選択").OnEvent("Click", GoToFolder)

    ; GUI全体をEscキーで閉じる処理を設定
    MyGui.OnEvent("Close", HandleEsc)

    ; ホットキーを有効化
    Hotkey("Up", HandleKeyUp, "On")
    Hotkey("Down", HandleKeyDown, "On")
    Hotkey("Enter", HandleKeyEnter, "On")
    Hotkey("Esc", HandleEsc, "On")

    MyGui.Show("x400 y200") ; GUIを表示
}

SearchFolders(*) {
    global SearchResults, TargetFolder, MyGui

    SearchText := MyGui["SearchBox"].Text ; 検索ボックスの入力を取得

    ; 検索ボックスが空の場合は処理を終了
    if (SearchText = "") {
        MyGui["ResultList"].Delete() ; リストボックスをクリア
        return
    }

    SearchResults := [] ; 検索結果を初期化

    ; サブフォルダを全階層にわたって検索
    Loop Files, TargetFolder "\*", "D R" ; 再帰検索を有効化
    {
        if InStr(A_LoopFileName, SearchText) ; サブフォルダ名に検索文字が含まれる場合
        {
            SearchResults.Push(A_LoopFileFullPath)
            if (SearchResults.Length >= 3) ; 最大3件まで結果を表示
                break
        }
    }

    ; 配列をリストボックスに設定
    ResultList := MyGui["ResultList"]
    ResultList.Delete() ; 既存アイテムを削除
    ResultList.Add(SearchResults) ; 新しいアイテムを追加
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
    GoToFolder() ; Enterキーで選択を確定
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

GoToFolder(*) {
    global SearchResults, MyGui, WindowActive
    if !WindowActive ; ウィンドウが非表示なら無効
        return
    SelectedIndex := MyGui["ResultList"].Value ; 選択されたアイテムのインデックスを取得
    if (SelectedIndex > 0) {
        SelectedFolder := SearchResults[SelectedIndex] ; 選択されたフォルダを取得
        Run SelectedFolder ; フォルダを開く
        MyGui.Destroy() ; GUIを閉じる
    }
}