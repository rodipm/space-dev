import re

def parse_commands(command):
    cmd = command
    p = re.compile('<<(.+)>>')
    sequence = p.findall(command)

    if len(sequence):
        sequence = sequence[0]
        cmd = cmd.replace('<<'+sequence+'>>', '')
        sequence = sequence.split('+')
        return cmd, sequence

    else:
        return cmd, None
print(parse_commands("eiuhaseshaieuh ieu hsaie uhsaiue haiueh isa a+b+c+d+asdas>>"))