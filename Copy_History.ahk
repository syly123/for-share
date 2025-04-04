#Requires AutoHotkey v2

global ClipboardHistory := [], FilePath := A_ScriptDir "\ClipboardHistory.txt"

; Clipboardの変更を監視して履歴を記録
SetTimer MonitorClipboard, 100

MonitorClipboard() {
    static LastClipboard := ""
    if (A_Clipboard != LastClipboard && StrLen(A_Clipboard)) {
        LastClipboard := A_Clipboard
        AddToHistory(A_Clipboard)
    }
}

AddToHistory(clip) {
    global ClipboardHistory, FilePath
    FormatTime := Format("{1:yyyy-MM-dd HH:mm:ss}", A_Now)
    ClipboardHistory.Push({ Time: FormatTime, Content: clip })
    FileAppend(Format("{1}`n{2}`n", FormatTime, clip), FilePath)
}

; Ctrl+Win+Vで履歴を表示
^#v::
{
    global ClipboardHistory
    GuiObj := Gui() ; 新しいGuiオブジェクトを作成
    GuiObj.SetFont("s12")

    ; ListBoxの内容を作成
    Items := []
    for Item in ClipboardHistory {
        Items.Push(Item.Time " | " Item.Content)
    }

    ListBox := GuiObj.Add("ListBox", "w400 h300", Items)
    GuiObj.Add("Button", "Default", "Close").OnEvent("Click", (*) => GuiObj.Destroy())
    GuiObj.Show()
}