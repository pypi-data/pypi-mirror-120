class MulticurrencyException(Exception):
    def __init__(self, message=None):
        self.message = message if message else ''

    def __str__(self) -> str:
        return f'Multicurrency Exception {self.message}'