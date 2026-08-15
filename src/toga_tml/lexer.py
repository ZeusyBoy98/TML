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

    while i < len(input):
        if input[i] == "<":
            closeIndex = input.find(">", i)
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