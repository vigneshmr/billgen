
class Util:
    @staticmethod
    def print_line():
        Util.write(str('-' * 80))

    @staticmethod
    def read_value(key):
        print '%s: ' % key
        return raw_input()

    @staticmethod
    def write(s):
        print s
