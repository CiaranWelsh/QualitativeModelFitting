import tellurium as te
from qualitative_model_fitting._simulator_old import TimeSeries, TimeSeriesPlotter
import matplotlib.pyplot as plt
import seaborn
seaborn.set_context('talk')


ant = """
model simple()
    compartment Cell = 1;
    kcat = 0.1;
    km = 1;
    ki = 0.5;
    k2 = 0.1;

    A = 10;
    B = 0;
    S = 1;
    I = 0;

    R1: A => B; Cell* kcat*S*A / (km + A + (km*I / ki));
    R2: B => A; Cell * k2*B;

end
"""

# mod = te.loada(ant)

# print(mod)


input = dict(
    Neither=dict(
        S=0, I=0
    ),
    StimulationOnly=dict(
        S=1,
        I=0
    ),
    InhibitionOnly=dict(
        S=0, I=1
    ),
    StimulationAndInhibition=dict(
        S=1, I=1
    )

)
ts = TimeSeries(ant, input, 0, 10, 11)

data = ts.simulate()
print(data)













