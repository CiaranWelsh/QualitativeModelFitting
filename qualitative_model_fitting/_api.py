import pandas as pd

from ._interpreter import Interpreter
from ._runner import ManualRunner
from ._parser import Parser


def manual_interface(ant_str, input_string):
    p = Parser()
    tree = p.parse(string=input_string)
    interpreter = Interpreter(tree)
    ts, obs = interpreter.interpret()
    runner = ManualRunner(ant_str, ts, obs)
    results = runner.run()
    df = pd.DataFrame(results).transpose().reset_index()
    df.columns = ['observation', 'truth']
    return df


def automatic_interface():
    pass
