#Requires AutoHotkey v2

global ClipboardHistory := []

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
    ClipboardHistory.Push(clip)
}

; リストボックス選択変更時のコールバック関数
OnListBoxChange(thisListBox, Info) {
    global ClipboardHistory
    SelectedIndex := thisListBox.Value
    if (SelectedIndex >= 1) { ; 有効なインデックスか確認
        SelectedItem := ClipboardHistory[SelectedIndex]
        A_Clipboard := SelectedItem ; クリップボードにコピー
        Send "^v" ; 貼り付け
        thisListBox.Gui.Destroy() ; GUIを閉じる
    }
}

; Ctrl+Win+V で履歴を表示するホットキー
^#v::
{
    global ClipboardHistory
    MyGui := Gui()
    MyGui.SetFont("s12") ; フォント設定

    ; リストボックスを作成して内容を設定
    MyListBox := MyGui.Add("ListBox", "w400 h300 +Wrap vClipboardList", ClipboardHistory)

    ; イベント登録
    MyListBox.OnEvent("Change", OnListBoxChange)

    MyGui.Show()
}


; MyGui_Close(thisGui) {  ; Declaring this parameter is optional.
;     if MsgBox("Are you sure you want to close the GUI?", , "y/n") = "No"
;         return true  ; true = 1
; }

; Ctrl_Change(GuiCtrlObj, Info) {
;     MsgBox(GuiCtrlObj.text)
;     return true
; }
; ; Ctrl+Win+V で履歴を表示するホットキー
; ^#v::
; {
;     MyGui := Gui()
;     MyListBox := MyGui.Add("ListBox", "r12 vColorChoice", ["a", "b"])
;     ; MyGui.AddText("", "Press Alt+F4 or the X button in the title bar.")
;     ; MyGui.OnEvent("Close", MyGui_Close)
;     MyListBox.OnEvent("Change", Ctrl_Change)

;     MyGui.Show()
; }

; MyGui := Gui()
; LinkText := 'Click to run <a href="notepad" id="notepad">Notepad</a> or open <a id="help" href="https://www.autohotkey.com/docs/">online help</a>.'
; Link := MyGui.Add("Link", "w200", LinkText)
; Link.OnEvent("Click", Link_Click)
; Link_Click(Ctrl, ID, HREF)
; {
;     MsgText := Format("
; (
;     ID: {1}
;     HREF: {2}

;     Execute this link?
; )", ID, HREF)
;     if MsgBox(MsgText, , "y/n") = "yes"
;         Run(HREF)
; }
; MyGui.Show()
