
TOKENTYPE = {
    "TAG": "TAG",
    "TAGOPEN": "TAGOPEN",
    "TAGCLOSE": "TAGCLOSE",
    "NEWLINE": "NEWLINE",
    "EOF": "EOF",
}
 
def tokenize(input):
    tokens = []
    i = 0
    length = len(input)
 
    while i < length:
        if input[i:i+4] == "<!--":
            closeIndex = input.find("-->", i + 4)
            if closeIndex == -1:
                raise Exception("L001 - Unterminated comment, expected '-->'")
            i = closeIndex + 3
        elif input[i] == "<":
            j = i + 1
            inQuotes = False
            closeIndex = -1
            while j < length:
                char = input[j]
                if char == "\"" and input[j-1] != "\\":
                    inQuotes = not inQuotes
                elif char == ">" and not inQuotes:
                    closeIndex = j
                    break
                j += 1
            if closeIndex == -1:
                raise Exception("L002 - Unterminated tag, expected '>'")
            tagText = input[i+1:closeIndex]
            if tagText.startswith("/"):
                tokens.append({"type": TOKENTYPE["TAGCLOSE"], "value": tagText[1:]})
            elif tagText.endswith("/"):
                tokens.append({"type": TOKENTYPE["TAG"], "value": tagText[:-1]})
            else:
                tokens.append({"type": TOKENTYPE["TAGOPEN"], "value": tagText})
            i = closeIndex + 1
        elif input[i] == "\n":
            tokens.append({"type": TOKENTYPE["NEWLINE"], "value": "\n"})
            i += 1
        else:
            i += 1
 
    tokens.append({"type": TOKENTYPE["EOF"], "value": ""})
    print("Tokenized")
    return tokens