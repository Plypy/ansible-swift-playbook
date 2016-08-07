# This is a naive inventory parser used to manipulate inventory files.
# It only parses basic group declaration, not those varialbes and children
# section, which will be ignored. And host variables will be ignored as well.
#
# So use this with caution.

from utils import strip_comment

class Inventory:
    def __init__(self, filename):
        self.groups = {}
        with open(filename) as f:
            self.data = f.read()
        data = self.data.split('\n')
        self._parse(data)

    def _raise_error(self, msg):
        raise Exception(msg)

    def _parse(self, lines):
        '''
        Parse the INI-like inventory file line by line, ignoring those
        attribute sections. Then store them in a dict of dict, self.groups.
        '''
        cur_group = ''
        lineno = 0
        for line in lines:
            lineno += 1
            line = strip_comment(line)

            # skip empty lines and comments
            if '' == line or line.startswith(';') or line.startswith('#'):
                continue

            # section found
            if '[' == line[0]:
                # skip section with attributes, like :vars :children
                if line.find(':') >= 0:
                    cur_group = ''
                    continue

                group = line[1:len(line)-1].strip()
                cur_group = group
                if group in self.groups:
                    continue;

                self.groups[group] = {}
                continue

            # skip attributes section
            if '' == cur_group:
                continue

            # entry found
            # key = value or value

            eq = line.find('=')
            if eq < 0:
                # only value
                key = value = line
                if line.find('[') >= 0:
                    key = value = flatten(line)
            else:
                key = line[0:eq].strip()
                value = line[eq+1:].strip()

            if isinstance(key, list):
                for i in range(len(key)):
                    self.groups[cur_group][key[i]] = value[i]
            else:
                self.groups[cur_group][key] = value


    def write():
        pass


# def get_pair(word):
#     '''
#     Parse string like key=value, or value
#     return [key, value]
#     '''
#     word = word.strip()

#     eq = word.find('=')
#     if eq < 0:
#         # only value
#         key = value = word
#         if word.find('[') >= 0:
#             key = value = flatten(word)
#     else:
#         key = word[0:eq].strip()
#         value = word[eq+1:].strip()

#     return [key, value]


def flatten(range_item):
    '''
    Build a list based on the item with a range, this module only supports
    numerical range for now.
    '''
    lbr = range_item.find('[')
    rbr = range_item.find(']')
    prefix = range_item[0:lbr]
    suffix = range_item[rbr+1:]

    interval = range_item[lbr+1:rbr].split(':')
    lower = interval[0].strip()
    upper = interval[1].strip()

    minlen = len(lower)
    lower = int(lower)
    upper = int(upper)

    ret = []
    for i in range(lower, upper+1):
        entry = prefix + strn(i, minlen) + suffix
        ret.append(entry)
    return ret


def strn(n, l=0):
    '''
    Convert number n to a string padding with leading zeros,
    with minimal length l.
    '''
    n = str(n)
    ln = len(n)

    if ln >= l:
        return n

    return ('0' * (l - ln)) + n

