# This class comes courtesy of http://stackoverflow.com/a/287944/1070011

class bcolors:
    HEADER = '\033[95m'
    R2D2_BACK = '\033[44;2m'
    R2D2_FORE = '\033[37;1m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''