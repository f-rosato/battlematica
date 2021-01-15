import re

comm = re.compile('#.*')
multiline = re.compile('\.\.\. *\n')
FOUR_SPACES = '    '


def preparse(s: str, indenter=FOUR_SPACES, block_open='{', block_close='}'):
    s = _straighten(s)
    s = _uncomment(s)
    s = _blockify(s, indenter, block_open, block_close)
    s = _unsweeten(s)
    return s


def _uncomment(s: str):
    return comm.sub('', s)


def _straighten(s: str):
    return multiline.sub('', s)


def _blockify(s: str, indenter=FOUR_SPACES, block_open='{', block_close='}'):
    s = s.upper()

    # this code turns the python-style indentation into
    # traditional limited blocks
    preparsed_lines = []
    level = 0
    for line in s.splitlines():
        if len(line.strip()) == 0:
            continue
        linelevel = 0
        while line.startswith(indenter):
            linelevel += 1
            line = line[len(indenter):]

        # indenters are re-included for clarity. They will be
        # ignored by the tokenizer anyways.
        if linelevel < level:
            preparsed_lines.append(indenter*linelevel + block_close * (level - linelevel) + line)
        elif linelevel > level:
            preparsed_lines.append(indenter*linelevel + block_open + line)
        else:
            preparsed_lines.append(indenter*linelevel + line)

        level = linelevel

    result = '\n'.join(preparsed_lines)

    return result


def _unsweeten(s: str):
    # ME is syntactic sugar for the filter+identifier construct ME BOT
    # that is "a bot whose uid is mine"
    return s.replace('ME', 'ME BOT')
