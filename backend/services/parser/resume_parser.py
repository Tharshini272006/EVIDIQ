import fitz

def parse_resume(path):

    text=""

    doc=fitz.open(path)

    for page in doc:
        text+=page.get_text()

    return text