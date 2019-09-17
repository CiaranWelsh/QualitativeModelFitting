import argparse
import os, glob
import pandas as pd
import numpy as np
import site

site.addsitedir(os.path.dirname(os.path.dirname(__file__)))
from qualitative_model_fitting import TimeSeries
from example_networks.model_strings import model_string

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int)
parser.add_argument('stop', type=int)
parser.add_argument('step', type=int)
parser.add_argument('-f', '--file', type=str)
parser.add_argument('-i', '--inputs', nargs='+', metavar='KEY=VALUE')
args = parser.parse_args()

print('inputs from python: ', args.inputs)

if args.file is None:
    args.file = os.path.join(
        os.path.dirname(__file__), 'simulation_data.csv'
    )

inputs = {i.split('=')[0]: float(i.split('=')[1]) for i in args.inputs}
ts = TimeSeries(
    ant_str=model_string, start=args.start,
    stop=args.stop, steps=args.step, inputs=inputs
)

df = ts.simulate()
df.to_csv(args.file)
