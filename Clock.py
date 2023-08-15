from LoxCallable import LoxCallable
import time

class ClockFunction(LoxCallable):
    def arity(self):
        """Returns the arity of a
        ClockFunction class
        """
        return 0
    def call(self, interpreter, arguments):
        """Returns the time represented as the number
        of seconds since epoch.
        """
        return time.time() / 1000
    def __str__(self):
        """Returns a human readable
        string representing class Clock.
        """
        return "<native fn>"