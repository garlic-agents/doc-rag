class DocumentParser:
    def __init__(self, document):
        self.document = document

    def parse(self):
        return self.document.split()
