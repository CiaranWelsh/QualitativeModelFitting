import os, glob
import pandas as pd
import numpy as np
from collections import OrderedDict

import qualitative_model_fitting as qmf
from example_networks.model_strings import model_string
from example_networks import WD, PLOTS_DIR
import logging

LOG = logging.getLogger(__name__)


def run_timeseries(input, conditions):
    ts = qmf.TimeSeries(model_string,
                        input, 0, 100, 101)
    # plot_selection = OrderedDict(
    #     IRS1=['IRS1', 'IRS1a', 'pIRS1'],
    #     Inputs=['Insulin', 'AA']
    # )
    plot_selection = OrderedDict(
        IRS1=['IRS1', 'IRS1a', 'pIRS1'],
        PI3K=['PI3K', 'pPI3K', 'PI3Ki'],
        PIP2=['PIP2', 'PIP3'],
        PDK1=['PDK1', 'PDK1_PIP3', 'Akt_PIP3'],
        Akt=['Akt', 'Akt_PIP3', 'pAkt', 'Akti'],
        TSC2=['TSC2', 'pTSC2'],
        RhebGDP=['RhebGDP', 'RhebGTP'],
        ppPras40=['ppPras40'],
        mTORC1cyt=['mTORC1cyt', 'mTORC1lys'],
        pmTORC1=['pmTORC1', 'mTORC1_Pras40cyt'],
        mTORC1i=['mTORC1i', 'mTORC1ii', 'mTORC1iii', 'mTORC1iv'],
        RAG_GDP=['RAG_GDP', 'RAG_GTP'],
        FourEBP1=['FourEBP1', 'pFourEBP1'],
        S6K=['S6K', 'pS6K'],
        AMPK=['AMPK', 'pAMPKi', 'pAMPK'],
        CaMKK2a=['CaMKK2a', 'CaMKK2', 'Ca2'],
        LKB1=['LKB1', 'LKB1a'],
        PLCeps=['PLCeps', 'pPLCeps'],
        IP3=['IP3', 'DAG', 'IpR', 'IpRa'],
        PKC=['PKC', 'PKCa'],
        RTK=['RTK', 'pRTK', 'pRTKa'],
        Sos=['Sos', 'pSos'],
        Raf=['Raf', 'pRaf'],
        Mek=['Mek', 'pMek', 'Meki'],
        Erk=['Erk', 'pErk'],
        RasGDP=['RasGDP', 'RasGTP'],
        DUSPmRNA=['DUSPmRNA', 'DUSP']
    )
    tsp = qmf.TimeSeriesPlotter(
        ts, plot_selection,
        conditions=conditions,
        plot_dir=PLOTS_DIR,
        fname='Simulation',
        ncols=4,
        wspace=0.3,
        hspace=0.6,
        legend_fontsize=8,
        legend_loc='upper right',
        figsize=(15, 15),
        seaborn_context='paper',
        savefig=True
    )
    tsp.plot()


if __name__ == '__main__':
    all_inputs = ['AA', 'Insulin', 'EGF', 'Wortmannin', 'Rapamycin', 'AZD', 'MK2206', 'PMA']
    all_inputs = {i: 0 for i in all_inputs}
    all_inputs['Insulin'] = 1

    inputs = dict(
        InsulinOnly=dict(
            inputs=dict(
                Insulin=1,
            ),
            obs=[
                'IRS1a@t=0 < IRS1a@t=10',
                'IRS1a@t=10 < IRS1a@t=20',
                'IRS1a@t=20 < IRS1a@t=30',
                'IRS1a@t=20 < IRS1a@t=40',
            ]
        ),
        InsulinAndAA=dict(
            inputs=dict(
                Insulin=1,
                AA=1
            ),
            obs=[
                'IRS1a@t=0 < IRS1a@t=10',
                'IRS1a@t=20 > IRS1a@t=40'
            ]
        )
    )

    # todo is the problem a iloc thing?

    res = qmf.manual_interface(model_string, inputs, 0, 100, 101)
    print(res.to_df())

    run_timeseries(inputs, ['InsulinAndAA'])

    LOG.debug('doing a log')
