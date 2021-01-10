def blockify(s: str, indenter='    ', block_open='{', block_close='}'):
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

    return unsweeten('\n'.join(preparsed_lines))


def unsweeten(s: str):
    return s.replace('ME', 'ME BOT')
    # ME is syntactic sugar for filter+i ME BOT, or "a bot whose uid is mine"
