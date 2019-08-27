import tellurium as te
from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter
import matplotlib.pyplot as plt
import seaborn

seaborn.set_context('talk')

ant = """
model simple()
    compartment Cell = 1;
    kcat = 1;
    km = 1;
    ki = 0.01;
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
        inputs=dict(
            S=0, I=0
        )
    ),
    StimulationOnly=dict(
        inputs=dict(
            S=1,
            I=0
        )
    ),
    InhibitionOnly=dict(
        inputs=dict(
            S=0, I=1
        )
    ),
    StimulationAndInhibition=dict(
        inputs=dict(S=1, I=1)
    )

)
ts = TimeSeries(ant, input, 0, 100, 101)

data = ts.simulate()
# print(data)
#
fig = plt.figure(figsize=(8, 8))
count = 1
for label, df in data.items():
    plt.subplot(2, 2, count)
    plt.plot(df.index, df['A'], label='A')
    plt.plot(df.index, df['B'], label='B')
    plt.title(label)
    plt.xlabel('time')
    plt.ylabel('Conc.')
    plt.legend()
    seaborn.despine(fig=fig, top=True, right=True)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    count += 1

# plt.show()
plt.savefig('x.png', dpi=300, bbox_inches='tight')


# TimeSeriesPlotter(ts, savefig=False)