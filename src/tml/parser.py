import lexer

def parse(tokens):
    pos = 0
    def peek(): return tokens[pos]
    def consume(): 
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t
    def expect(type):
        t = consume()
        if t["type"] != type:
            raise Exception(f"Expected {type}, got {t["type"]}")
            return t
    def parseDocument():
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"]:
            while peek()["type"] == lexer.TOKENTYPE["NEWLINE"]: consume()
            if peek()["type"] == lexer.TOKENTYPE["EOF"]: break
            if peek()["type"] == lexer.TOKENTYPE["TAG"]:
                children.append(parseTag())
        return {"type": "Document", "children": children}
    def parseTag():
        t = consume()
        return {"type": "Tag", "name": t["value"]}
    def parseUntil(closeType):
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"] and peek()["type"] != closeType:
            children.append(parseTag())
        if peek()["type"] == closeType:
            consume()
        return children
    return parseDocument()