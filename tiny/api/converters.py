class TinyConverter:
    regex = '[0-9]|[a-z]|[A-Z]{5}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)