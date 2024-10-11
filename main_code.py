r'(?:\n|^)((?:[^\n]*\n){1,3})(?=\n{2,}|$)'
r'(?:\n|^)([^\n]*(?:\n[^\n]*){0,2})(?:\n|$)'
r'(?<=\n)\n((?:[^\n]+\n){1,4})(?=\n)'
r'([^\n]*\.\n)((?:[^\n]*\n){0,3})([^\n]*\.\n)'

    regex_pattern = r'([^\n]*\.\n)((?:(?![^\n]*\.\n)[^\n]*\n?){0,3})([^\n]*\.\n)'


    regex_pattern = r'(?<=\.\n)(.*?)(?=\n[^\n]*\.\n)'
    matches = re.findall(regex_pattern, text, re.DOTALL)

    # 抽出されたテキストを行数でフィルタリング
    extracted_texts = []
    for match in matches:
        lines = match.strip().splitlines()
        if len(lines) <= 4:  # 行数が4行以下の場合
            extracted_texts.append(match.strip())
    
    return extracted_texts