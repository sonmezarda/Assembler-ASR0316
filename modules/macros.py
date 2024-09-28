from typing import Callable

def macro_push(line:str) -> list[str]:
    if '{' not in line or '}' not in line:
        return line
    lines = []
    params = line[line.index('{')+1:line.index('}')]
    params = [param.strip() for param in params.split(',')]
    for param in params:
        f = f"push {param}"
        lines.append(f)
    return lines

def macro_pop(line:str) -> list[str]:
    if '{' not in line or '}' not in line:
        return line
    lines = []
    params = line[line.index('{')+1:line.index('}')]
    params = [param.strip() for param in params.split(',')]
    for param in params:
        f = f"pop {param}"
        lines.append(f)
    lines.reverse()
    return lines

macro_words:dict[str, Callable] = {"push":macro_push,
                                   "pop":macro_pop}


if __name__ == '__main__':
    line = "push {r1, r2, r3}"
    print(macro_push(line))