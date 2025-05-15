#Requires AutoHotkey v2

global GlobalData := [] ; TSVデータを事前に保持する配列
global SearchResults := [] ; 検索結果を保持する配列
global PathList := [] ; パスを保持する配列
global TsvFilePath := "C:\Users\tatsu\Documents\for-share\sample.tsv" ; TSVファイルのパス
global MyGui := "" ; GUIオブジェクトを明示的に初期化
global WindowActive := false ; ウィンドウが表示中かどうかを管理
global SearchTimer := 0 ; 検索遅延用のタイマー

; Win + Shift + Spaceで検索ボックスを表示するホットキー
#+Space::
{
    global MyGui, WindowActive, GlobalData, SearchResults, PathList

    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    WindowActive := true

    GlobalData := LoadTSVData()

    MyGui := Gui()
    MyGui.SetFont("s12")

    ; 検索ボックスを作成
    SearchBox := MyGui.Add("Edit", "vSearchBox w600 h40", "")
    SearchBox.OnEvent("Change", DelayedSearch) ; 入力時に検索を遅延

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

    MyGui.Show("x400 y200")
}

LoadTSVData() {
    global TsvFilePath
    Data := []

    Loop Read, TsvFilePath
    {
        LineData := StrSplit(A_LoopReadLine, "`t")
        if (LineData.Length < 5)
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

DelayedSearch(*) {
    global SearchTimer
    SetTimer(SearchTsv, -300) ; **0.3秒後にSearchTsvを実行**
}

SearchTsv(*) {
    global GlobalData, SearchResults, PathList, MyGui

    SearchText := MyGui["SearchBox"].Text

    ; **検索ボックスが空 or 1文字以下の場合は検索しない**
    if (StrLen(SearchText) <= 1) {
        SearchResults := []
        PathList := []
        MyGui["ResultList"].Delete()
        return
    }

    SearchResults := []
    PathList := []

    for Item in GlobalData {
        if (InStr(Item.FileName, SearchText) || InStr(Item.FilePath, SearchText)) {
            SearchResults.Push(Item.FileName " - " Item.FilePath)
            PathList.Push(Item.FilePath)
        }
    }

    ResultList := MyGui["ResultList"]
    ResultList.Delete()
    ResultList.Add(SearchResults)
}

HandleKeyUp(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive || SearchResults.Length = 0
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Max(ResultList.Value - 1, 1)
}

HandleKeyDown(*) {
    global MyGui, SearchResults, WindowActive
    if !WindowActive || SearchResults.Length = 0
        return
    ResultList := MyGui["ResultList"]
    ResultList.Value := Min(ResultList.Value + 1, SearchResults.Length)
}

HandleKeyEnter(*) {
    global MyGui, WindowActive
    if !WindowActive || SearchResults.Length = 0
        return
    ShowDetails()
}

HandleEsc(*) {
    global MyGui, WindowActive
    WindowActive := false
    MyGui.Destroy()

    Hotkey("Up", HandleKeyUp, "Off")
    Hotkey("Down", HandleKeyDown, "Off")
    Hotkey("Enter", HandleKeyEnter, "Off")
    Hotkey("Esc", HandleEsc, "Off")
}

ShowDetails(*) {
    global PathList, MyGui

    SelectedIndex := MyGui["ResultList"].Value
    if (SelectedIndex > 0) {
        SelectedPath := PathList[SelectedIndex]

        Run "explorer.exe /select," SelectedPath

        A_Clipboard := SelectedPath
    }
}