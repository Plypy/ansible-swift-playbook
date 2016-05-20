# This is a simple parser for the key: value formatted Ansible variable file.
# It will only perform trivial syntax check.

from utils import strip_comment

class Varmap:
    def __init__(self, filename):
        self.data = {}
        with open(filename) as f:
            data = f.read()
        data = data.split('\n')
        self._parse(data)

    def _raise_error(self, msg):
        raise Exception(msg)

    def _parse(self, lines):

        #handle --- and ...
        lines = [line.strip() for line in lines]
        st = 0
        ed = len(lines)
        if '---' in lines:
            st = lines.index('---')+1
        if '...' in lines:
            ed = lines.index('...')
        lines = lines[st:ed]

        lineno = 0
        for line in lines:
            lineno += 1

            line = strip_comment(line)

            if '' == line or line.startswith(';') or line.startswith('#'):
                continue

            colon = line.find(':')
            if colon < 0:
                self._raise_error('Wrong syntax at line ' + str(lineno))

            pair = line.split(':')
            key = pair[0].strip()
            value = pair[1].strip()
            self.data[key] = value
