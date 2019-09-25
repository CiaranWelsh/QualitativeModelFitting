import os, glob
import pandas as pd
import numpy as np
from collections import OrderedDict

import qualitative_model_fitting as qmf
from example_networks.extended_model_string import model_string
from example_networks import WD, PLOTS_DIR
import logging

LOG = logging.getLogger(__name__)

string = """
timeseries Null                 {} 0, 100, 101
timeseries FedOnly               {Feeding=1} 0, 100, 101
timeseries InsulinOnly          {Insulin=1} 0, 100, 101
timeseries InsulinFed            {Insulin=1, Feeding=1} 0, 100, 101
timeseries FedOnlyWort           {Feeding=1, Wortmannin=1} 0, 100, 101
timeseries InsulinOnlyWort      {Insulin=1, Wortmannin=1} 0, 100, 101
timeseries InsulinFedWort        {Insulin=1, Wortmannin=1, Feeding=1} 0, 100, 101
timeseries FedRapamycin          {Feeding=1, Rapamycin=1} 0, 100, 101
timeseries InsulinRapamycin     {Insulin=1, Rapamycin=1} 0, 100, 101
timeseries InsulinFedRapamycin   {Feeding=1, Rapamycin=1, Insulin=1} 0, 100, 101

//timeseries RhebKD {Insulin=1, Feeding=1, RhebGDP=1} 0, 100, 101
//timeseries TSC2KO {Insulin=1, Feeding=1, TSC2=0} 0, 100, 101

observation
    Obs1    : IRS1a[InsulinOnly]@t=0 < IRS1a[InsulinOnly]@t=20
    Obs2    : IRS1a[InsulinOnly]@t=20 < IRS1a[InsulinFed]@t=20
    Obs3    : sum(IRS1a[InsulinOnly]@t=(0, 100)) < Sum(IRS1a[InsulinFed]@t=(0, 100))
    // // Patursky 2014 
    // PaturskyFig2A1: pS6K[FedOnly]@t=0 < pS6K[FedOnly]@t=10 //need hyperbolic up here
    // PaturskyFig2A2: pS6K[FedOnly]@t=10 < pS6K[FedOnly]@t=20
    // PaturskyFig2A3: all(pS6K[FedOnly]@t=(0, 100) >= pS6K[FedRapamycin]@t=(0, 100))
    // 
    // // hinalt2004
    // HinaltFig1A1: pmTORC1[InsulinOnly]@t=80 > pmTORC1[Null]@t=80 
    // HinaltFig1A2: pmTORC1[InsulinOnly]@t=80 > pmTORC1[FedOnly]@t=80 
    // HinaltFig1A3: pmTORC1[FedOnly]@t=80 > pmTORC1[Null]@t=80 
    // HinaltFig1A4: pmTORC1[InsulinFed]@t=80 > pmTORC1[FedOnly]@t=80 
    // HinaltFig1A5: pmTORC1[InsulinFed]@t=80 > pmTORC1[InsulinOnly]@t=80
    // // with wortmannin 
    // HinaltFig1A6: pmTORC1[InsulinFed]@t=80 > pmTORC1[InsulinFedWort]@t=80 
    // HinaltFig1A7: pmTORC1[InsulinFed]@t=80 > pmTORC1[InsulinFedWort]@t=80 
    // HinaltFig1A8: pS6K[FedOnly]@t=80 > pS6K[Null]@t=80 
    // HinaltFig1A9: pS6K[InsulinFed]@t=80 > pS6K[FedOnly]@t=80 
    // HinaltFig1A10: pS6K[InsulinFed]@t=80 > pS6K[InsulinOnly]@t=80 
    // HinaltFig1A11: pS6K[InsulinFed]@t=80 > pS6K[Null]@t=80 
    // HinaltFig1A12: pS6K[InsulinFed]@t=80 > pS6K[InsulinFedWort]@t=80 
    // // fig 2
    // HinaltFig2A1: pAkt[FedOnly]@t=80 < pAkt[InsulinOnly]@t=80 
    // HinaltFig2A2: pAkt[FedOnly]@t=80 < pAkt[InsulinFed]@t=80 
    // HinaltFig2A3: pAkt[FedOnly]@t=80 < pAkt[InsulinFed]@t=80 
    // HinaltFig2A4: pAkt[FedOnlyWort]@t=80 < pAkt[InsulinFedWort]@t=80 
    // HinaltFig2A5: pAkt[InsulinFedWort]@t=80 > pAkt[Null]@t=80 
    // HinaltFig2A6: pAkt[InsulinFedWort]@t=80 > pAkt[InsulinOnly]@t=80 
    // HinaltFig2A7: pAkt[InsulinFedWort]@t=80 > pAkt[FedOnlyWort]@t=80 
    // HinaltFig2A8: pAkt[InsulinFedWort]@t=80 > pAkt[FedOnlyWort]@t=80 
    // // fig4
    // HinaltFig4B1: pAkt[InsulinFedWort]@t=80 > pAkt[FedOnlyWort]@t=80 
    // HinaltFig4B2: pAkt[InsulinRapamycin]@t=80 > pAkt[InsulinOnly]@t=80 //because of feedback S6K
    // HinaltFig4B3: pAkt[InsulinFed]@t=80 > pAkt[InsulinFedRapamycin]@t=80 
    
    // Obs1        : sum(pAkt['
     


    //// without Fed, mTORC1 is not activated so neither is s6k and no feedback.
    //// therefore IRS1a is hyperbolic in this instance.
    //obs1: IRS1a[InsulinOnly]@t=0 < IRS1a[InsulinOnly]@t=10 
    //obs2: IRS1a[InsulinOnly]@t=10 < IRS1a[InsulinOnly]@t=20
    //
    //// with Fed, S6K negative FB causes transient negative shape
    //obs3: IRS1a[InsulinFed]@t=0 < IRS1a[InsulinFed]@t=10 
    //obs4: IRS1a[InsulinFed]@t=10 > IRS1a[InsulinFed]@t=20
    //
    //// lacher2010, figure 1a
    //obs5: RhebGDP[RhebKD]@t=0 < RhebGDP[InsulinFed]@t=0 
    //obs6: max(pS6K[RhebKD]@t=(0, 100)) < max(pS6K[InsulinFed]@t=(0, 100)) 
    //
    //// vander2007
    //// Cells lacking TSC2 result in constitutive activation of mTORC1
    //obs7: max(pmTORC1[TSC2KO]@t=(0, 100)) > max(pmTORC1[InsulinFed]@t=(0, 100))
    


"""

if __name__ == '__main__':

    # some flags

    RUN_QMF = True

    PLOT_TS = False

    WORKING_DIR = os.path.dirname(os.path.dirname(__file__))
    MODELS_DIR = os.path.join(WORKING_DIR, 'models')
    COPASI_FILE = os.path.join(MODELS_DIR, 'copasi_model.cps')
    SIMULATIONS_DIR = os.path.join(WORKING_DIR, 'simulations')
    PLOT_BASE_DIR = os.path.join(SIMULATIONS_DIR, 'ExtendedPI3KModel')
    VALIDATIONS_DIR = os.path.join(PLOT_BASE_DIR, 'validations')
    SCRATCH_DIR = os.path.join(PLOT_BASE_DIR, 'ScratchPad')
    STORIES_DIR = os.path.join(PLOT_BASE_DIR, 'Stories')

    dirs = ['WORKING_DIR',
            'MODELS_DIR',
            'COPASI_FILE',
            'SIMULATIONS_DIR',
            'PLOT_BASE_DIR',
            'VALIDATIONS_DIR',
            'SCRATCH_DIR',
            'STORIES_DIR']
    for i in dirs:
        if not os.path.isdir(i):
            os.makedirs(i)

    if RUN_QMF:
        res = qmf.ManualRunner(model_string, string)
        print(res.run())

    if PLOT_TS:
        inputs = dict(Insulin=1)
        ts = qmf.TimeSeries(model_string, inputs, 0, 100, 101)
        qmf.TimeSeriesPlotter(
            ts,
            plot_selection={
                'IRS1': ['IRS1a'],
                'Akt': ['pAkt'],
                'TSC2': ['TSC2', 'pTSC2'],
                'Rheb': ['RhebGTP', 'RhebGDP'],
                'mTORC1': ['pmTORC1'],
                'S6K': ['pS6K']},
            ncols=3,
            plot_dir=SCRATCH_DIR,
            fname='sim.png',
        ).plot()

        # plot_selection = OrderedDict(
        #     IRS1=['IRS1', 'IRS1a', 'pIRS1'],
        #     PI3K=['PI3K', 'pPI3K', 'PI3Ki'],
        #     PIP2=['PIP2', 'PIP3'],
        #     PDK1=['PDK1', 'PDK1_PIP3', 'Akt_PIP3'],
        #     Akt=['Akt', 'Akt_PIP3', 'pAkt', 'Akti'],
        #     TSC2=['TSC2', 'pTSC2'],
        #     RhebGDP=['RhebGDP', 'RhebGTP'],
        #     ppPras40=['ppPras40'],
        #     mTORC1cyt=['mTORC1cyt', 'mTORC1lys'],
        #     pmTORC1=['pmTORC1', 'mTORC1_Pras40cyt'],
        #     mTORC1i=['mTORC1i', 'mTORC1ii', 'mTORC1iii', 'mTORC1iv'],
        #     RAG_GDP=['RAG_GDP', 'RAG_GTP'],
        #     FourEBP1=['FourEBP1', 'pFourEBP1'],
        #     S6K=['S6K', 'pS6K'],
        #     AMPK=['AMPK', 'pAMPKi', 'pAMPK'],
        #     CaMKK2a=['CaMKK2a', 'CaMKK2', 'Ca2'],
        #     LKB1=['LKB1', 'LKB1a'],
        #     PLCeps=['PLCeps', 'pPLCeps'],
        #     IP3=['IP3', 'DAG', 'IpR', 'IpRa'],
        #     PKC=['PKC', 'PKCa'],
        #     RTK=['RTK', 'pRTK', 'pRTKa'],
        #     Sos=['Sos', 'pSos'],
        #     Raf=['Raf', 'pRaf'],
        #     Mek=['Mek', 'pMek', 'Meki'],
        #     Erk=['Erk', 'pErk'],
        #     RasGDP=['RasGDP', 'RasGTP'],
        #     DUSPmRNA=['DUSPmRNA', 'DUSP']
        # )
        # mapk_plot_selection = OrderedDict(
        #     RTK=['RTK', 'pRTK', 'pRTKa'],
        #     Sos=['Sos', 'pSos'],
        #     Raf=['Raf', 'pRaf'],
        #     Mek=['Mek', 'pMek', 'Meki'],
        #     Erk=['Erk', 'pErk'],
        #     RasGDP=['RasGDP', 'RasGTP'],
        #     DUSPmRNA=['DUSPmRNA', 'DUSP']
        # )
        # # mTORC1 activation
        # insulin_plot_selection = OrderedDict(
        #     IRS1=['IRS1', 'IRS1a', 'pIRS1'],
        #     PI3K=['PI3K', 'pPI3K', 'PI3Ki'],
        #     PIP2=['PIP2', 'PIP3'],
        #     PDK1=['PDK1', 'PDK1_PIP3', 'Akt_PIP3'],
        #     Akt=['Akt', 'Akt_PIP3', 'pAkt', 'Akti'],
        #     TSC2=['TSC2', 'pTSC2'],
        #     RhebGDP=['RhebGDP', 'RhebGTP'],
        #     ppPras40=['ppPras40'],
        #     mTORC1loc=['mTORC1cyt', 'mTORC1lys'],
        #     pmTORC1=['pmTORC1', 'mTORC1_Pras40cyt'],
        #     mTORC1i=['mTORC1i', 'mTORC1ii', 'mTORC1iii', 'mTORC1iv'],
        #     RAG_GDP=['RAG_GDP', 'RAG_GTP'],
        #     FourEBP1=['FourEBP1', 'pFourEBP1'],
        #     S6K=['S6K', 'pS6K'],
        # )
        #
        # dct = OrderedDict(
        #     InsulinStimulation=OrderedDict(
        #         inputs=OrderedDict(
        #             Insulin=[0, 1],
        #             Fed=[0, 1],
        #         ),
        #         plot_selection=insulin_plot_selection,
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         subplots_adjust=dict(top=0.9),
        #     ),
        #     InsulinStimulationAndPI3KInhibition=OrderedDict(
        #         inputs=OrderedDict(
        #             Insulin=[1],
        #             Fed=[1],
        #             Wortmannin=[0, 1]
        #         ),
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         plot_selection=insulin_plot_selection,
        #         subplots_adjust=dict(top=0.9)
        #     ),
        #     InsulinStimulationAndAktInhibition=OrderedDict(
        #         inputs=OrderedDict(
        #             Insulin=[1],
        #             Fed=[1],
        #             MK2206=[0, 1]
        #         ),
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         subplots_adjust=dict(top=0.9),
        #         plot_selection=insulin_plot_selection,
        #
        #     ),
        #     InsulinStimulationAndmTORC1Inhibition=OrderedDict(
        #         inputs=OrderedDict(
        #             Insulin=[1],
        #             Fed=[1],
        #             Rapamycin=[0, 1]
        #         ),
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         subplots_adjust=dict(top=0.9),
        #         plot_selection=insulin_plot_selection,
        #     ),
        #     InsulinStimulationAndTSC2Manipulation=OrderedDict(
        #         inputs=OrderedDict(
        #             Insulin=[1],
        #             Fed=[1],
        #             TSC2=[0, 10, 20]
        #         ),
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         subplots_adjust=dict(top=0.9),
        #         plot_selection=insulin_plot_selection,
        #     ),
        #     EGFStimulation=OrderedDict(
        #         inputs=OrderedDict(
        #             EGF=[0, 1]
        #         ),
        #         plot_selection=mapk_plot_selection,
        #         hspace=0.5,
        #     ),
        #     EGFStimulatioAndAZD=OrderedDict(
        #         inputs=OrderedDict(
        #             EGF=[1],
        #             AZD=[0, 1]
        #         ),
        #         plot_selection=mapk_plot_selection,
        #         hspace=0.5,
        #     ),
        #     EGFStimulationPI3KOutput=OrderedDict(
        #         inputs=OrderedDict(
        #             EGF=[0, 1]
        #         ),
        #         plot_selection=insulin_plot_selection,
        #         figsize=(12, 12),
        #         ncols=3,
        #         hspace=0.5,
        #         subplots_adjust=dict(top=0.9),
        #     ),
        #     EGFStimulatioAndAZDPI3KOutput=OrderedDict(
        #         inputs=OrderedDict(
        #             EGF=[1],
        #             AZD=[0, 1]
        #         ),
        #         plot_selection=insulin_plot_selection,
        #         hspace=0.5,
        #         figsize=(12, 12),
        #         ncols=3,
        #         subplots_adjust=dict(top=0.9)
        #     )
        # )
        # from qualitative_model_fitting import TimeSeries, TimeSeriesPlotter
        #
        # TimeSeries(model_string, )
        # # for k, v in dct.items():
        #     plot_dir = os.path.join(STORIES_DIR, k)
        #     if not os.path.isdir(plot_dir):
        #         os.makedirs(plot_dir)
        #     ts = TimeSeries(model_string,
        #                            start=0, stop=150, steps=151,
        #                            savefig=True,
        #                            plot_dir=plot_dir,
        #                            use_cache=True,
        #                            **v,
        #                            )
