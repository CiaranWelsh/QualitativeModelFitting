import pandas as pd
from functools import reduce
from lark import Tree, Token

from qualitative_model_fitting._parser import _TimeSeriesArgumentList, _TimeSeriesArgument, _ComparisonStatement, \
    _Observation, _Expression, _ModelEntity
import logging

LOG = logging.getLogger(__name__)


# todo the stuff currently in interpreter seems
# like it should actualy be in parser



class Interpreter:
    """
    Read a Lark tree into a set of classes.
    """

    def __init__(self, tree: Tree):
        """

        Args:
            tree:
        """
        self.tree = tree

    def _get_timeseries_blocks(self):
        return self.tree.find_data('timeseries_block')

    def _get_observation_block(self):
        return self.tree.find_data('observation_block')

    def interpret(self):
        # print(self.tree.pretty())
        ts_list = []
        for ts_block in self.tree.find_data('timeseries_block'):
            ts_list.append(_TimeSeriesBlock(ts_block))

        ss_list = []
        for ss_block in self.tree.find_data('steady_state_block'):
            LOG.warning('steady state functionality is currently a placeholder. '
                        'Not yet implemented')

        comp_list = []
        for comparison_block in self.tree.find_data('comparison_statement'):
            comp_list.append(_ComparisonStatement(comparison_block))

        # print(comp_list)

    @staticmethod
    def _timeseries_block(block):
        """
        Intepret the time series block
        Args:
            block:

        Returns:

        """
        name = block.children[0]
        if name.type != 'NAME':
            raise SyntaxError(name)
        names = []
        amounts = []
        for subtree in block.find_data():
            print(subtree)
        #     for token in subtree.children:
        #         print(token)
        #         if token.type == 'NAME':
        #             names.append(str(token))
        #         elif token.type in ['NUMBER', 'FLOAT', 'DIGIT']:
        #             amounts.append(float(str(token.value)))
        #
        # ts_args = dict(zip(names, amounts))
        # integration_settings = {'start': None, 'stop': None, 'step': None}
        # for tok in block.children:
        #     if isinstance(tok, Tree):
        #         pass
        #     elif isinstance(tok, Token):
        #         if tok.type == 'START':
        #             integration_settings['start'] = float(str(tok.value))
        #         elif tok.type == 'STOP':
        #             integration_settings['stop'] = float(str(tok.value))
        #         elif tok.type == 'STEP':
        #             integration_settings['step'] = float(str(tok.value))
        # for k, v in integration_settings.items():
        #     if v == [] or v is None:
        #         raise ValueError
        #
        # return dict(name=name, conditions=ts_args, integration_settings=integration_settings)

    @staticmethod
    def observation_block(block):
        """
        objectify the observation block
        Args:
            block:

        Returns:

        """
        block = [i for i in block]
        print(block)
        if len(block) != 1:
            raise SyntaxError('There must be exactly 1'
                              ' observation block but found "{}"'.format(len(block)))
        block = block[0]
        statement_list = [i for i in block.find_data('statement')]
        new_statement_list = []
        for state in statement_list:
            s = _Observation(state)
            new_statement_list.append(s)
        return new_statement_list

    @staticmethod
    def comparison_observation():
        """
        objectify the observation block
        Args:
            block:

        Returns:

        """
        block = [i for i in block]
        print(block)
        if len(block) != 1:
            raise SyntaxError('There must be exactly 1'
                              ' observation block but found "{}"'.format(len(block)))
        block = block[0]
        statement_list = [i for i in block.find_data('statement')]
        new_statement_list = []
        for state in statement_list:
            s = _Observation(state)
            new_statement_list.append(s)
        return new_statement_list




