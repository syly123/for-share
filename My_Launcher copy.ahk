#Requires AutoHotkey v2

global SearchResults := [] ; 検索結果を保持する配列
global TargetFolder := "C:\Users\tatsu\Documents\for-share\" ; 検索対象のフォルダを指定
global MyGui := "" ; GUIオブジェクトを明示的に初期化

; Win + Shift + Spaceで検索ボックスを表示するホットキー
#+Space::
{
    global MyGui ; グローバル変数を宣言

    ; GUIオブジェクトが既に存在する場合は破棄して再作成
    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    MyGui := Gui()
    MyGui.SetFont("s12") ; フォント設定

    ; 横長の検索ボックスを作成
    MyGui.Add("Edit", "vSearchBox w600 h40", "").OnEvent("Change", SearchFolders)

    ; 空のリストボックスを作成
    MyGui.Add("ListBox", "r5 vResultList w600 h200", []) ; 初期値として空の配列を設定
    MyGui.Add("Button", "y+10 Default", "選択").OnEvent("Click", GoToFolder)

    MyGui.Show("x400 y200") ; GUIを表示
}

SearchFolders(*) {
    global SearchResults, TargetFolder, MyGui

    SearchText := MyGui["SearchBox"].Text ; 検索ボックスの入力を取得
    SearchResults := [] ; 検索結果を初期化

    ; サブフォルダを検索し、条件にマッチするものを取得
    Loop Files, TargetFolder "\*", "D" ; "D" オプションでディレクトリのみ取得
    {
        if InStr(A_LoopFileName, SearchText) ; サブフォルダ名に検索文字が含まれる場合
        {
            SearchResults.Push(A_LoopFileFullPath)
            if (SearchResults.Length >= 3) ; 最大3件まで結果を表示
                break
        }
    }

    ; 配列をリストボックスに一括追加
    MyGui["ResultList"].Delete() ; リストボックスの既存アイテムを削除
    MyGui["ResultList"].Add(SearchResults) ; 配列を直接渡してアイテムを設定
}

GoToFolder(*) {
    global SearchResults, MyGui

    SelectedIndex := MyGui["ResultList"].Value ; 選択されたアイテムのインデックスを取得
    if (SelectedIndex > 0) {
        SelectedFolder := SearchResults[SelectedIndex] ; 配列から選択されたフォルダを取得
        Run SelectedFolder ; フォルダを開く
        MyGui.Destroy() ; GUIを閉じる
    }
}