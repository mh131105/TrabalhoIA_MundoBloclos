"""Simulador geométrico: valida planos sem consultar variáveis/cláusulas SAT."""
from cenarios import BLOCKS, MAX_POINT, MAX_LEVEL


def span(b, p):
    return set(range(p, p + BLOCKS[b]))


def valid_state(s):
    if set(s) != set(BLOCKS):
        return False
    for b, (p, level) in s.items():
        if not (0 <= p <= MAX_POINT - BLOCKS[b] and 0 <= level <= MAX_LEVEL):
            return False
        cells = span(b, p)
        for other, (q, height) in s.items():
            if b != other and height == level and cells & span(other, q):
                return False
        if level:
            support = set().union(*(span(c, q) for c, (q, h) in s.items()
                                    if c != b and h == level - 1))
            if len(cells & support) < (BLOCKS[b] + 1) // 2:
                return False
    return True


def clear(s, b):
    p, level = s[b]
    return not any(h > level and span(b, p) & span(c, q)
                   for c, (q, h) in s.items() if c != b)


def move(s, action):
    b, y, p = action
    if b not in BLOCKS or y not in (*BLOCKS, 'T') or b == y:
        raise ValueError('bloco/apoio inválido')
    if not valid_state(s) or not clear(s, b):
        raise ValueError('estado inválido ou origem bloqueada')
    level = 0 if y == 'T' else s[y][1] + 1
    if s[b] == (p, level):
        raise ValueError('ação nula')
    cells = span(b, p)
    if y != 'T' and not cells & span(y, s[y][0]):
        raise ValueError('sem contato com apoio escolhido')
    if any(h >= level and cells & span(c, q)
           for c, (q, h) in s.items() if c != b):
        raise ValueError('destino/corredor vertical bloqueado')
    result = dict(s, **{b: (p, level)})
    if not valid_state(result):
        raise ValueError('destino fora da mesa, colisão ou instabilidade')
    return result


def replay(initial, actions):
    states = [dict(initial)]
    for action in actions:
        states.append(move(states[-1], action))
    return states


def successors(s):
    for b, length in BLOCKS.items():
        if clear(s, b):
            for y in (*BLOCKS, 'T'):
                if y != b:
                    for p in range(MAX_POINT - length + 1):
                        action = (b, y, p)
                        try:
                            yield action, move(s, action)
                        except ValueError:
                            pass


def derive_on(s):
    return {b: (['T'] if level == 0 else
                [c for c, (q, h) in s.items() if c != b and h == level - 1
                 and span(b, p) & span(c, q)]) for b, (p, level) in s.items()}
