#Requires AutoHotkey v2

; グローバル変数の定義
global GlobalData := []
global SearchResults := []
global PathList := []
global TsvFilePath := "C:\Users\tatsu\Documents\for-share\sample.tsv"
global MyGui := ""
global WindowActive := false
global SearchTimer := 0
global to_Omit := ["C:\Users\tatsu\Documents\", "C:\Shared\"]
global BoxChanged := False
global FileMode := True

; ホットキー: Win + Shift + Space で検索ボックスを表示
#+Space:: {
    global MyGui, WindowActive, GlobalData, BoxChanged, FileMode

    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    WindowActive := true
    GlobalData := LoadTSVData()
    BoxChanged := False
    FileMode := True

    MyGui := Gui()
    MyGui.SetFont("s12")

    SearchBox := MyGui.Add("Edit", "vSearchBox w600 h40", "")
    SearchBox.OnEvent("Change", DelayedSearch)

    ResultList := MyGui.Add("ListView", "r30 vResultList w800 h300", ["ファイル名", "パス"])
    ResultList.ModifyCol(1, 250)
    ResultList.ModifyCol(2, 550)

    MyGui.Add("Button", "y+10 Default", "エクスプローラーで表示").OnEvent("Click", ShowDetails)

    MyGui.OnEvent("Close", HandleEsc)

    Hotkey("Enter", HandleKeyEnter, "On")
    Hotkey("Esc", HandleEsc, "On")

    MyGui.Show("x400 y200")
}

LoadTSVData() {
    global TsvFilePath
    Data := []

    Loop Read, TsvFilePath {
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
    global BoxChanged, FileMode
    BoxChanged := True

    SearchText := MyGui["SearchBox"].Text
    FileMode := (SubStr(SearchText, 1, 2) = "p ") ? False : True

    ; p  の場合は先頭2文字を削除し、xxx のみを検索
    if !FileMode
        SearchText := SubStr(SearchText, 3)

    SetTimer(SearchTsv, -300)
}

SearchTsv(*) {
    global GlobalData, SearchResults, PathList, MyGui, to_Omit, WindowActive, BoxChanged, FileMode

    if !WindowActive
        return

    SearchText := MyGui["SearchBox"].Text

    ; p  の場合は先頭2文字を削除して検索
    if !FileMode
        SearchText := SubStr(SearchText, 3)

    ; 検索ボックスが2文字以下の場合は検索しない
    if (StrLen(SearchText) <= 2) {
        SearchResults := []
        PathList := []
        MyGui["ResultList"].Delete()
        return
    }


    BoxChanged := False

    SearchResults := []
    PathList := []

    for Item in GlobalData {
        SearchTarget := FileMode ? Item.FileName : Item.FilePath

        if (InStr(SearchTarget, SearchText)) {
            FullPath := Item.FilePath
            DisplayPath := FullPath

            for OmitText in to_Omit {
                DisplayPath := StrReplace(DisplayPath, OmitText, "")
            }

            DisplayPath := RegExReplace(DisplayPath, "\\[^\\]+?\.[^.]+?$", "")
            SearchResults.Push([Item.FileName, DisplayPath])
            PathList.Push(FullPath)
        }
        if BoxChanged
            return
    }
    if !WindowActive
        return
    ResultList := MyGui["ResultList"]
    ResultList.Delete()
    for Row in SearchResults {
        if BoxChanged
            return

        ResultList.Add(, Row[1], Row[2])
    }
}

HandleKeyEnter(*) {
    global MyGui, WindowActive
    if !WindowActive || SearchResults.Length = 0
        return

    ShowDetails()
}

HandleEsc(*) {
    global MyGui, WindowActive, BoxChanged
    WindowActive := False
    BoxChanged := True
    MyGui.Destroy()

    Hotkey("Enter", HandleKeyEnter, "Off")
    Hotkey("Esc", HandleEsc, "Off")
}

ShowDetails(*) {
    global PathList, MyGui
    SelectedIndex := MyGui["ResultList"].GetNext()

    if (SelectedIndex > 0) {
        SelectedPath := PathList[SelectedIndex]
        Run "explorer.exe /select," SelectedPath
        A_Clipboard := SelectedPath
    }
}