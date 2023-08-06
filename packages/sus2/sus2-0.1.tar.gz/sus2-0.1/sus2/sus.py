def toSus(text) -> str:
    if len(text) >= 2:
        if text[-2:] != "us": text += "us"
    else: text += "us"
    return str(text)

class amogus():
    def __init__(self) -> None:
        self.text = ""

    def isSus(self) -> bool:
        return "us" in self.text

    def sussify(self) -> None:
        self.text =  ' '.join(list(map(toSus, (self.text).split())))