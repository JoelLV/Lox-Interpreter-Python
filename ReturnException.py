class Return(RuntimeError):
    def __init__(self, value):
        """Creates a return
        exception object that
        inherits from RuntimeError
        for handling Return statements.
        >>> return_obj = Return(2)
        >>> return_obj.value
        2
        >>> return_obj = Return("Some value")
        >>> return_obj.value
        'Some value'
        """
        super().__init__()
        self.value = value

if __name__ == '__main__':
    import doctest
    doctest.testmod()