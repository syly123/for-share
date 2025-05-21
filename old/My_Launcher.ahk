#Requires AutoHotkey v2

global SearchResults := [] ; 検索結果を保持する配列
global TargetFolder := "C:\Users\tatsu\Documents\for-share\" ; 検索対象のフォルダを指定
global MyGui := "" ; GUIオブジェクトを明示的に初期化

; Win + Shift + Spaceで検索ボックスを表示するホットキー
#+Space::
{
    global MyGui ; グローバル変数を宣言

    ; GUIオブジェクトを再生成する前に確認
    if IsObject(MyGui) {
        MyGui.Destroy()
    }

    MyGui := Gui() ; 新しいGUIオブジェクトを作成
    MyGui.SetFont("s12") ; フォント設定

    ; 横長の検索ボックスを作成
    MyGui.Add("Edit", "vSearchBox w600 h40", "").OnEvent("Change", SearchFolders)

    ; 検索結果を表示するリストボックス
    MyGui.Add("ListBox", "vResultList w600 h200", SearchResults)
    MyGui.Add("Button", "y+10 Default", "選択").OnEvent("Click", GoToFolder)

    MyGui.Show("x400 y200") ; GUIを表示
}

SearchFolders(*) {
    global SearchResults, TargetFolder, MyGui ; グローバル変数を宣言

    SearchText := MyGui["SearchBox"].Text ; 検索ボックスの入力を取得
    SearchResults := [] ; 検索結果を初期化

    ; サブフォルダを検索し、条件にマッチするものを取得
    Loop Files, TargetFolder "\*", "D" ; "D" オプションでディレクトリのみ取得
    {
        if InStr(A_LoopFileName, SearchText) ; サブフォルダ名に検索文字が含まれる場合
        {
            SearchResults.Push(A_LoopFileFullPath)
            if (SearchResults.Length() >= 3) ; 最大3件まで結果を表示
                break
        }
    }

    ; リストボックスを更新
    MyGui["ResultList"].Value := SearchResults
}

GoToFolder(*) {
    global SearchResults, MyGui ; グローバル変数を宣言

    SelectedFolder := MyGui["ResultList"].Text ; 選択されたフォルダを取得
    if (SelectedFolder != "")
    {
        Run SelectedFolder ; フォルダを開く
        MyGui.Destroy() ; GUIを閉じる
    }
}