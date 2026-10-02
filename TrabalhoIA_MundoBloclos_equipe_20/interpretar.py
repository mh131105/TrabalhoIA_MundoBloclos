"""Decodifica resultado MiniSAT, confere CNF e reexecuta a geometria."""
import argparse
from pathlib import Path
from cenarios import BLOCKS
from dominio import replay, derive_on


def read_map(path):
    result = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        number, name = line.split(maxsplit=1)
        number = int(number)
        kind, args = name.rstrip(')').split('(')
        if number in result:
            raise ValueError('ID duplicado no mapa')
        result[number] = (kind, args.split(','))
    if set(result) != set(range(1, len(result) + 1)):
        raise ValueError('IDs do mapa não são consecutivos')
    return result


def read_result(path):
    tokens = Path(path).read_text().split()
    if not tokens or tokens[0] not in ('SAT', 'UNSAT'):
        raise ValueError('esperado SAT ou UNSAT em formato MiniSAT')
    if tokens[0] == 'UNSAT':
        return None
    literals = [int(x) for x in tokens[1:] if x != '0']
    if len({abs(x) for x in literals}) != len(literals):
        raise ValueError('modelo contém atribuições repetidas/contraditórias')
    return literals


def check_cnf(path, literals, variable_count):
    truth = set(literals)
    count, declared, pending = 0, None, []
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        if line.startswith('p'):
            _, kind, n, declared = line.split()
            if kind != 'cnf' or int(n) != variable_count:
                raise ValueError('cabeçalho CNF incompatível com mapa')
            declared = int(declared)
            continue
        for literal in map(int, line.split()):
            if literal:
                if abs(literal) > variable_count:
                    raise ValueError('literal fora do mapa')
                pending.append(literal)
            else:
                count += 1
                if not truth.intersection(pending):
                    raise ValueError(f'cláusula {count} não satisfeita')
                pending = []
    if pending or count != declared:
        raise ValueError('CNF incompleta ou contagem incorreta')


def decode(mapping, literals):
    truth = set(literals)
    states, actions = {}, {}
    for number, (kind, args) in mapping.items():
        if number not in truth:
            continue
        if kind in ('at', 'lev'):
            b, coordinate, t = args
            row = states.setdefault(int(t), {}).setdefault(b, {})
            if kind in row:
                raise ValueError('coordenada não única')
            row[kind] = int(coordinate)
        elif kind == 'mv':
            b, y, p, t = args
            if int(t) in actions:
                raise ValueError('mais de uma ação por instante')
            actions[int(t)] = (b, y, int(p))
    if not states or set(states) != set(range(max(states) + 1)):
        raise ValueError('estados temporais incompletos')
    trace = []
    for t in range(len(states)):
        if set(states[t]) != set(BLOCKS) or any(set(row) != {'at', 'lev'} for row in states[t].values()):
            raise ValueError('estado incompleto')
        trace.append({b: (states[t][b]['at'], states[t][b]['lev']) for b in BLOCKS})
    if set(actions) != set(range(len(trace) - 1)):
        raise ValueError('sequência de ações incompleta')
    plan = [actions[t] for t in range(len(actions))]
    if replay(trace[0], plan) != trace:
        raise ValueError('modelo diverge do simulador independente')
    return plan, trace


def interpret(result, map_path, cnf_path):
    mapping = read_map(map_path)
    literals = read_result(result)
    if literals is None:
        return 'UNSAT: nenhum plano neste horizonte (não significa impossibilidade global).\n'
    if {abs(x) for x in literals} != set(mapping):
        raise ValueError('atribuição incompleta ou mapa incompatível')
    check_cnf(cnf_path, literals, len(mapping))
    plan, trace = decode(mapping, literals)
    lines = [f'PLANO ENCONTRADO ({len(plan)} ações); CNF e simulação validadas.']
    for t, (b, y, p) in enumerate(plan):
        lines.append(f'{t + 1}. t={t}: mover {b} para {"MESA" if y == "T" else y}, p={p}')
    for t, state in enumerate(trace):
        lines.append(f'S{t}: ' + '; '.join(f'{b}=({p},{h})' for b, (p, h) in state.items()))
    lines.append('Apoios finais: ' + '; '.join(f'{b} sobre {",".join(ys)}' for b, ys in derive_on(trace[-1]).items()))
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resultado', type=Path)
    parser.add_argument('--mapa', type=Path)
    parser.add_argument('--cnf', type=Path)
    args = parser.parse_args()
    directory = args.resultado.parent
    print(interpret(args.resultado, args.mapa or directory / 'trab01_blocos2SAT.map',
                    args.cnf or directory / 'trab01_blocos2SAT.cnf'), end='')


if __name__ == '__main__':
    main()
