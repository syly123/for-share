r'(?:\n|^)((?:[^\n]*\n){1,3})(?=\n{2,}|$)'
r'(?:\n|^)([^\n]*(?:\n[^\n]*){0,2})(?:\n|$)'
r'(?<=\n)\n((?:[^\n]+\n){1,4})(?=\n)'
r'([^\n]*\.\n)((?:[^\n]*\n){0,3})([^\n]*\.\n)'

regex_pattern = r'([^\n]*\.\n)((?:[^\n]*\n){0,3})([^\n]*\.\n)'
matches = re.findall(regex_pattern, text)

# B+Cを取得して整形
extracted_texts = [f"{match[1].strip()}{match[2]}" for match in matches]
return extracted_texts