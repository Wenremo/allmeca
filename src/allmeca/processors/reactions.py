class _Base:
    pass


class Noop(_Base):
    pass


class Stop(_Base):
    pass


class Response(_Base):
    def __init__(self, response):
        self.response = response
