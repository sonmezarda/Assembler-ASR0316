def macro_push(line:str) -> list[str]:
    lines = []
    params = line[line.index('{')+1:line.index('}')]
    params = [param.strip() for param in params.split(',')]
    for param in params:
        f = f"push {param}"
        lines.append(f)
    return lines



if __name__ == '__main__':
    line = "push {r1, r2, r3}"
    print(macro_push(line))