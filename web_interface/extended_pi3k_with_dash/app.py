import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_canvas import DashCanvas, utils as dash_canvas_utils
from dash.dependencies import Input, Output
from PIL import Image
import os
import pandas as pd
import numpy as np
from qualitative_model_fitting import TimeSeries
from example_networks.growth_model_string import model_string
import plotly.graph_objs as go
from collections import OrderedDict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
WD = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
WEB_INTERFACE_DIR = os.path.join(WD, 'web_interface')
APP_DIR = os.path.join(WEB_INTERFACE_DIR, 'extended_pi3k_with_dash')
ASSETS_DIR = os.path.join(APP_DIR, 'assets')

PLOTTABLE_SPECIES_FILE = os.path.join(WEB_INTERFACE_DIR, 'plottable_species.txt')
NETWORK_FNAME = os.path.join(WEB_INTERFACE_DIR, 'network.png')
# STYLESHEET_FILE = os.path.join(STYLESHEETS_DIR, 'dash-style.css')
# STYLESHEET_FILE = os.path.join(STYLESHEETS_DIR, 'dash-style-mod.css')

# checks for directories
for i in [WD, WEB_INTERFACE_DIR, ASSETS_DIR, APP_DIR]:
    if not os.path.isdir(i):
        raise ValueError(i)

# checks for files
for i in [PLOTTABLE_SPECIES_FILE, NETWORK_FNAME]:
    if not os.path.isfile(i):
        raise ValueError

# get img as matrix
img = Image.open(NETWORK_FNAME)
img = np.array(img.convert('RGBA'))
img = dash_canvas_utils.array_to_data_url(img)

# some css
css = {

}

# Dash app begin
app = dash.Dash(
    __name__,
    assets_folder=ASSETS_DIR,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],

)

# inputs string
model_inputs = [
    'Insulin',
    'AA',
    'E2',
    'Rapamycin',
    'MK2206',
    'AZD',
    'EGF',
    'Wortmannin',
    'PMA',
    'IGF',
    'INFg',
    'Feeding',
]

# load from file plottable species. #todo replace with string manipulation of model string
with open(PLOTTABLE_SPECIES_FILE, 'r') as f:
    species = f.read().split('\n')
species = sorted([i.strip() for i in species])

app.layout = html.Div(children=[
    html.H1(children='Extended PI3K Model'),

    # for graph and inputs
    html.Div([

        # a left panel for inputs
        html.H2('Select Model Inputs'),
        html.Div([
            dcc.Checklist(
                id='model_inputs',
                options=[
                    {'label': i, 'value': i} for i in model_inputs
                ],
                # multi=True,
                value=['Insulin', 'AA'],
                labelStyle={"display": "inline-block"},
                style={'text-align': 'center'}
            ),

            html.H2('Select Model Outputs'),
            dcc.Dropdown(
                id='outputs',
                options=[{'label': i, 'value': i} for i in species],
                value=['pmTORC1'],
                multi=True
            ),
            html.Button(id='all_output_btn', children='All Outputs'),
            html.Button(id='all_pi3k_output_btn', children='PI3K Outputs'),
            html.Button(id='active_pi3k_output_btn', children='Active PI3K Outputs'),
            html.Button(id='erk_output_btn', children='Erk Output'),
            html.Button(id='ampk_output_btn', children='AMPK Output'),
            html.Button(id='ip3_output_btn', children='IP3 Output'),
            html.Button(id='e2_output_btn', children='Estrogen Output'),
            html.Button(id='phenom_output_btn', children='Phenomenological Output'),
            html.Button(id='infg_output_btn', children='INFg Output'),
            html.Button(id='trp_output_btn', children='Trp Output'),

            html.H2('Integration Parameters'),
            html.Form([
                html.Label('Start'),
                dcc.Input(placeholder='', type='text', value=0, id='start', style={'float': 'left'}),
                html.Label('Stop'),
                dcc.Input(placeholder='', type='text', value=100, id='stop', style={'float': 'left'}),
                html.Label('Step'),
                dcc.Input(placeholder='', type='text', value=101, id='step', style={'float': 'left'}),
            ],
                style={'display': 'flex'},
                # className='form-inline'
            )

        ]),

        # right panel is graph
        html.Div([dcc.Graph(id='graph')]),
    ]),

    # for network image
    html.Div([
        DashCanvas(id='canvas_image',
                   image_content=img,
                   tool='select',
                   )
    ]),

    html.Div([
        dcc.Markdown(model_string, id='model_string')
    ])

], style={
    # 'background-color': 'coral',
    'width': '100%',
    'height': '100%'
})


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [
        Input(component_id='model_string', component_property='children'),
        Input(component_id='model_inputs', component_property='value'),
        Input(component_id='start', component_property='value'),
        Input(component_id='stop', component_property='value'),
        Input(component_id='step', component_property='value'),
        Input(component_id='outputs', component_property='value'),
    ]
)
def update_inputs(model_string, model_inputs, start, stop, step, outputs):
    model_inputs = {i: 1 for i in model_inputs}
    ts = TimeSeries(model_string, model_inputs, float(start), float(stop), int(step)).simulate()
    ts = ts[outputs]
    traces = []
    for i in ts:
        traces.append(
            go.Scatter(
                x=np.array(ts.index),
                y=ts[i],
                name=i,
                mode='lines'
            )
        )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Time (AU)'},
            yaxis={'title': '[AU]'},
            showlegend=True
        )
    }


NCLICKS_DCT = OrderedDict(
    all_output_btn={
        'n_clicks': 0,
        'output': species
    },
    all_pi3k_output_btn={
        'n_clicks': 0,
        'output': ['IRS1', 'IRS1a', 'pIRS1', 'PI3K',
                   'pPI3K', 'PI3Ki', 'PIP2', 'PIP3',
                   'PDK1', 'PDK1_PIP3', 'Akt', 'Akt_PIP3',
                   'pAkt', 'Akt_PIP3', 'Akti', 'TSC2',
                   'pTSC2', 'RagGDP', 'TSC2_Rag', 'RagGTP',
                   'mTORC1cyt', 'mTORC1lys',
                   'RhebGTP', 'pmTORC1', 'RhebGDP', 'mTORC1i',
                   'mTORC1ii', 'mTORC1iii', 'FourEBP1',
                   'pFourEBP1', 'S6K', 'pS6K', 'PTEN']
    },
    active_pi3k_output_btn={
        'n_clicks': 0,
        'output': ['IRS1a', 'pPI3K', 'pAkt', 'TSC2_Rag', 'RagGTP',
                   'RhebGTP', 'pmTORC1', 'pFourEBP1', 'pS6K']
    },
    ampk_output_btn={
        'n_clicks': 0,
        'output': [
            'AMPK', 'AMP',
            'AMPK_AMP', 'ADP', 'AMPK_ADP', 'ATP',
            'AMPK_ATP', 'pAMPKi', 'pAMPK', 'CaMKK2',
            'CaMKK2a', 'Ca2', 'PKC', 'PKCa', 'LKB1a', 'LKB1'
        ]
    },
    erk_output_btn={
        'n_clicks': 0,
        'output': ['RTK', 'pRTK', 'Sos', 'pRTKa', 'pSos',
                   'RasGDP', 'RasGTP', 'Raf', 'pRaf', 'Mek',
                   'pMek', 'Erk', 'pErk', 'Meki', 'DUSPmRNA', 'DUSP',
                   ]
    },
    ip3_output_btn={
        'n_clicks': 0,
        'output': ['PLCeps', 'pPLCeps', 'IP3', 'DAG', 'IpR', 'IpRa', ]
    },

    e2_output_btn={
        'n_clicks': 0,
        'output': ['E2_cyt', 'ERa_cyt', 'ERa_E2', 'ERa_dimer',
                   'ERa_dimer_nuc', 'ERa_nuc', 'TFFmRNA', 'Greb1mRNA', 'TFF',
                   'Greb1', 'mER'
                   ]
    },
    phenom_output_btn={
        'n_clicks': 0,
        'output': ['ProlifSignals', 'Growth', 'Immuno']
    },
    infg_output_btn={
        'n_clicks': 0,
        'output': ['pJak', 'Jak', 'Stat1', 'pStat1',
                   'pStat1_dim_cyt', 'pStat1_dim_nuc', 'IDO1mRNA', 'IDO1']
    },
    trp_output_btn={
        'n_clicks': 0,
        'output': ['tRNA_Trp', 'Trp', 'Kyn', 'tRNA',
                   'tRNA_trp', 'GCN2', 'GCN2_a', 'eIFa',
                   'peIFa', 'mERa',
                   ]
    },
)


@app.callback(
    Output('outputs', 'value'),
    [Input(i, 'n_clicks') for i in list(NCLICKS_DCT.keys())]
)
def output_callbacks(*args):
    print(args)
    if all(args) is None:
        raise dash.exceptions.PreventUpdate

    for i in range(len(args)):
        btn = list(NCLICKS_DCT.keys())[i]
        nclick = args[i]
        existing_nclick = NCLICKS_DCT[btn]['n_clicks']
        print('btn', btn)
        print('nclick', nclick)
        print('existing_nclick', existing_nclick)

        if nclick is not None:
            if nclick != existing_nclick:
                print('doing a return')
                NCLICKS_DCT[btn]['n_clicks'] = nclick
                return NCLICKS_DCT[btn]['output']
            else:
                continue


if __name__ == '__main__':
    app.run_server(debug=True)
