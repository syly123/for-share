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
global UseRegex := False  ; 正規表現検索を管理するフラグ

; ホットキー: Win + Shift + Space で検索ボックスを表示
#+Space:: {
    global MyGui, WindowActive, GlobalData, BoxChanged, FileMode, UseRegex

    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    WindowActive := true
    GlobalData := LoadTSVData()
    BoxChanged := False
    FileMode := True
    UseRegex := False  ; 初期状態は通常検索

    MyGui := Gui()
    MyGui.SetFont("s12")
    MyGui.Opt("+Resize")

    SearchBox := MyGui.Add("Edit", "vSearchBox w600 h40", "")
    SearchBox.OnEvent("Change", DelayedSearch)

    ResultList := MyGui.Add("ListView", "r30 vResultList w1400 h700", ["ファイル名", "パス", "更新日", "作成日"])
    ResultList.ModifyCol(1, 750)
    ResultList.ModifyCol(2, 1250)
    ResultList.ModifyCol(3, 200)
    ResultList.ModifyCol(4, 200)

    MyGui.Add("Button", "y+10 Default", "エクスプローラーで表示").OnEvent("Click", ShowDetails)

    MyGui.OnEvent("Close", HandleEsc)

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
    global BoxChanged, FileMode, UseRegex
    BoxChanged := True

    SearchText := MyGui["SearchBox"].Text

    FileMode := (SubStr(SearchText, 1, 2) = "p ") ? False : True

    if !FileMode
        SearchText := SubStr(SearchText, 3)

    UseRegex := (SubStr(SearchText, 1, 2) = "r:") ? True : False

    if UseRegex
        SearchText := SubStr(SearchText, 3)

    SetTimer(SearchTsv, -300)
}

SearchTsv(*) {
    global GlobalData, SearchResults, PathList, MyGui, to_Omit, WindowActive, BoxChanged, FileMode, UseRegex

    if !WindowActive
        return

    SearchText := MyGui["SearchBox"].Text

    FileMode := (SubStr(SearchText, 1, 2) = "p ") ? False : True
    if !FileMode
        SearchText := SubStr(SearchText, 3)

    UseRegex := (SubStr(SearchText, 1, 2) = "r:") ? True : False
    if UseRegex
        SearchText := SubStr(SearchText, 3)

    if (StrLen(SearchText) <= 2) {
        SearchResults := []
        PathList := []
        MyGui["ResultList"].Delete()
        return
    }

    SearchText := StrReplace(SearchText, "　", " ")
    SearchText := StrLower(SearchText)
    ;SearchText := RegExReplace(SearchText, "\p{Z}", "")

    BoxChanged := False

    SearchResults := []
    PathList := []

    for Item in GlobalData {
        SearchTarget := FileMode ? Item.FileName : Item.FilePath

        Try {
            MatchFound := !UseRegex ? InStr(StrLower(SearchTarget), SearchText) : RegExMatch(StrLower(SearchTarget), SearchText)
        } Catch {
            MatchFound := False
            return
        }

        if MatchFound {
            FullPath := Item.FilePath
            DisplayPath := FullPath

            for OmitText in to_Omit {
                DisplayPath := StrReplace(DisplayPath, OmitText, "")
            }

            ; DisplayPath := RegExReplace(DisplayPath, "\\[^\\]+?\.[^.]+?$", "")
            DisplayPath := StrReplace(DisplayPath, Item.FileName, "")
            SearchResults.Push([Item.FileName, DisplayPath, Item.UpdateDate, Item.CreationDate])
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

        ResultList.Add(, Row[1], Row[2], Row[3], Row[4])
    }
}

HandleEsc(*) {
    global MyGui, WindowActive, BoxChanged
    WindowActive := False
    BoxChanged := True
    MyGui.Destroy()

    Hotkey("Esc", HandleEsc, "Off")
}

ShowDetails(*) {
    global PathList, MyGui, to_Omit
    ResultList := MyGui["ResultList"]
    SelectedIndex := MyGui["ResultList"].GetNext()

    if (SelectedIndex > 0) {
        ; SelectedPath := PathList[SelectedIndex]
        SelectedPath := to_Omit[1] . ResultList.GetText(SelectedIndex, 2) . ResultList.GetText(SelectedIndex, 1)
        Run "explorer.exe /select," SelectedPath
        A_Clipboard := SelectedPath
    }
}