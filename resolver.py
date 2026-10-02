"""SAT real (MiniSat22 via PySAT); enumera horizontes e salva os artefatos."""
import argparse
from pathlib import Path
from pysat.solvers import Minisat22
from cenarios import FIGURAS, METAS
from bw2cnf_var import encode
from interpretar import interpret


def solve(initial, goal, directory, result_name, max_horizon=14):
    directory = Path(directory)
    history = []
    for horizon in range(max_horizon + 1):
        encoding = encode(initial, goal, horizon)
        with Minisat22(bootstrap_with=encoding.clauses) as solver:
            sat = solver.solve()
            model = solver.get_model() if sat else None
        history.append({'horizonte': horizon, 'status': 'SAT' if sat else 'UNSAT',
                        'variaveis': len(encoding.ids), 'clausulas': len(encoding.clauses)})
        print(f'{directory.name}: T={horizon} {history[-1]["status"]}', flush=True)
        directory.mkdir(parents=True, exist_ok=True)
        if sat:
            encoding.write(directory)
            result = directory / result_name
            result.write_text('SAT\n' + ' '.join(map(str, model)) + ' 0\n')
            print(interpret(result, directory / 'trab01_blocos2SAT.map',
                            directory / 'trab01_blocos2SAT.cnf'), end='')
            return history
    raise RuntimeError(f'nenhum plano até T={max_horizon}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cenario', type=int, choices=FIGURAS)
    parser.add_argument('--meta')
    parser.add_argument('--todos', action='store_true', help='inclui todas as metas desenhadas')
    parser.add_argument('--max-horizonte', type=int, default=14)
    parser.add_argument('--saida', type=Path, default=Path('resultados'))
    args = parser.parse_args()
    if args.meta and not args.cenario:
        parser.error('--meta exige --cenario')
    for i in ([args.cenario] if args.cenario else FIGURAS):
        goals = ([args.meta] if args.meta else
                 [g for g in FIGURAS[i] if g != 'S0'] if args.todos else [METAS[i]])
        for goal in goals:
            if goal not in FIGURAS[i]:
                parser.error(f'meta inexistente: {goal}')
            folder = args.saida / f'cenario{i}'
            if goal != METAS[i]:
                folder /= goal
            solve(FIGURAS[i]['S0'], FIGURAS[i][goal], folder,
                  f'resultado{i}.txt', args.max_horizonte)


if __name__ == '__main__':
    main()
