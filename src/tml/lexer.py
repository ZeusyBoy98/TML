TOKENTYPE = {
    "TAG": "TAG",
    "NEWLINE": "NEWLINE",
    "EOF": "EOF",
}

def tokenize(input):
    tokens = []
    i = 0

    while i < len(input):
        if input[i] == "<":
            closeIndex = input.find("/>", i)
            tagText = input[i+1:closeIndex]
            i = closeIndex + 2
            tokens.append({"type": TOKENTYPE["TAG"], "value": tagText})
        elif input[i] == "\n":
            tokens.append({"type": TOKENTYPE["NEWLINE"], "value": "\n"})
            i += 1

    tokens.append({"type": TOKENTYPE["EOF"], "value": ""})
    return tokens