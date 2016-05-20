def strip_comment(line):
    '''
    Helper function. Naively strip characters after the first '#' found.
    As the simple usage we have, this should not cause any harm.
    '''
    pos = line.find('#')
    if pos <= 0:
        return line.strip()

    return line[0:pos-1].strip()
