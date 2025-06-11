#Requires AutoHotkey v2

global GlobalData := [] ; TSVデータを事前に保持する配列
global SearchResults := [] ; 検索結果を保持する配列
global PathList := [] ; パスを保持する配列
global TsvFilePath := "C:\Users\tatsu\Documents\for-share\sample.tsv" ; TSVファイルのパス
global MyGui := "" ; GUIオブジェクトを明示的に初期化
global WindowActive := false ; ウィンドウが表示中かどうかを管理

; Win + Shift + Spaceで検索ボックスを表示するホットキー
#+Space::
{
    global MyGui, WindowActive, GlobalData, SearchResults, PathList

    ; GUIオブジェクトが既に存在する場合は破棄して再作成
    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    WindowActive := true ; ウィンドウ表示中

    ; **TSVデータを事前にロード**
    GlobalData := LoadTSVData()

    MyGui := Gui()
    MyGui.SetFont("s12") ; フォント設定

    ; 検索ボックスを作成
    SearchBox := MyGui.Add("Edit", "vSearchBox w600 h40", "")
    SearchBox.OnEvent("Change", SearchTsv) ; 入力内容が変更された際のイベント

    ; リストボックスを作成
    ResultList := MyGui.Add("ListBox", "r10 vResultList w800 h300", [])

    ; 選択ボタンを作成
    MyGui.Add("Button", "y+10 Default", "エクスプローラーで表示").OnEvent("Click", ShowDetails)

    ; GUI全体をEscキーで閉じる処理を設定
    MyGui.OnEvent("Close", HandleEsc)

    ; ホットキーを有効化
    Hotkey("Up", HandleKeyUp, "On")
    Hotkey("Down", HandleKeyDown, "On")
    Hotkey("Enter", HandleKeyEnter, "On")
    Hotkey("Esc", HandleEsc, "On")

    MyGui.Show("x400 y200") ; GUIを表示
}

LoadTSVData() {
    global TsvFilePath
    Data := []

    ; **TSVファイルを事前に読み込み**
    Loop Read, TsvFilePath
    {
        LineData := StrSplit(A_LoopReadLine, "`t")
        if (LineData.Length < 5) ; 列が不足している場合は無視
            continue

        Data.Push({
            FolderOrFile: LineData[1],
            FileName: LineData[2],
            FilePath: LineData[3],
            CreationDate: LineData[4],
            UpdateDate: LineData[5]
        })
    }
    return Data
}

SearchTsv(*) {
    global GlobalData, SearchResults, PathList, MyGui

    SearchText := MyGui["SearchBox"].Text ; 検索ボックスの入力を取得

    ; 検索ボックスが空の場合は処理を終了
    if (SearchText = "") {
        SearchResults := [] ; **検索結果を常に初期化**
        PathList := []
        MyGui["ResultList"].Delete() ; リストボックスをクリア
        return
    }

    SearchResults := [] ; 検索結果を初期化
    PathList := []

    ; **事前読み込みしたTSVデータを検索**
    for Item in GlobalData {
        if (InStr(Item.FileName, SearchText) || InStr(Item.FilePath, SearchText)) {
            SearchResults.Push(Item.FileName " - " Item.FilePath) ; ファイル名とパスの形式で格納
            PathList.Push(Item.FilePath) ; パスの形式で格納
        }
    }

    ; 配列をリストボックスに一括設定
    ResultList := MyGui["ResultList"]
    ResultList.Delete() ; 既存アイテムを削除
    ResultList.Add(SearchResults) ; 配列を直接リストボックスに渡す
}

HandleKeyUp(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive || SearchResults.Length = 0 ; **検索結果が空のときは動作させない**
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Max(ResultList.Value - 1, 1) ; 上矢印キーで移動
}

HandleKeyDown(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive || SearchResults.Length = 0 ; **検索結果が空のときは動作させない**
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Min(ResultList.Value + 1, SearchResults.Length) ; 下矢印キーで移動
}

HandleKeyEnter(*) {
    global MyGui, WindowActive
    if !WindowActive || SearchResults.Length = 0 ; **検索結果が空のときは動作させない**
        return
    ShowDetails() ; Enterキーでエクスプローラーを開く
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
    global PathList, MyGui

    SelectedIndex := MyGui["ResultList"].Value ; 選択されたアイテムのインデックスを取得
    if (SelectedIndex > 0) {
        SelectedPath := PathList[SelectedIndex] ; 選択されたパスを取得

        ; **エクスプローラーでフォルダを開く**
        Run "explorer.exe /select," SelectedPath

        ; **クリップボードにパスをコピー**
        A_Clipboard := SelectedPath
    }
}