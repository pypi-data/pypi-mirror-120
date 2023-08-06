class CordraId(str):
    handle = ""
    id = ""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, handle, id):
        self.handle = handle.strip("/")
        self.id = id.strip("/")

    def __str__(self):
        return f"{self.handle}/{self.id}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)