def preparse(s: str, indenter='    ', block_open='{', block_close='}'):

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

        if linelevel < level:
            preparsed_lines.append(indenter*linelevel + block_close * (level - linelevel) + line)
        elif linelevel > level:
            preparsed_lines.append(indenter*linelevel + block_open + line)
        else:
            preparsed_lines.append(indenter*linelevel + line)

        level = linelevel

    result = '\n'.join(preparsed_lines)

    # unsweetening
    result = unsweeten(result)

    return result


def unsweeten(s: str):
    # ME is syntactic sugar for the filter+identifier construct ME BOT
    # that is "a bot whose uid is mine"
    return s.replace('ME', 'ME BOT')
