import win32com.client

word = win32com.client.Dispatch("Word.Application")
doc = word.Documents.Open(r"C:\Users\tatsu\OneDrive\01_参照用\06_日常\会話録.docx")
doc.SaveAs(r"C:\path\to\output.pdf", FileFormat=17)
doc.Close()
word.Quit()