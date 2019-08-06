import os, glob, re
import pandas as pd
import numpy as np

from qualitative_model_fitting import _simulator

# registery for rules classes
REGISTERED_MUTEXCL_RULES = set()
REGISTERED_COMB_RULES = set()


class MutExclRuleRegister(type):
    """
    Metaclass which automatically register rule classes into the REGISTER_RULES set
    """

    def __new__(mcs, clsname, superclasses, attribute_dict):
        newclass = type.__new__(mcs, clsname, superclasses, attribute_dict)
        if superclasses:
            REGISTERED_MUTEXCL_RULES.add(newclass)
        return newclass


class CombRuleRegister(type):
    """
    Metaclass which automatically register rule classes into the REGISTER_RULES set
    """

    def __new__(mcs, clsname, superclasses, attribute_dict):
        newclass = type.__new__(mcs, clsname, superclasses, attribute_dict)
        if superclasses:
            REGISTERED_COMB_RULES.add(newclass)
        return newclass


class _RuleBase:
    operators = ['>', '<', '>=', '<=', '!>', '!<', '=', '!=']
    pattern = None

    def __init__(self, rule: str) -> None:
        self.rule = rule

    def syntax_checking(self):
        match = re.findall(self.pattern, self.rule)
        if match == []:
            raise SyntaxError(f'The syntax for {self.__class__.__name__} is {self.pattern}')

    def _extract_grammar(self):
        if self.pattern is None:
            raise ValueError('pattern is of type None')
        return re.findall(self.pattern, self.rule)


class _MutExclRuleBase(_RuleBase, metaclass=MutExclRuleRegister):
    def __init__(self, rule: str):
        super().__init__(rule)


class _CombRuleBase(_RuleBase, metaclass=CombRuleRegister):
    def __init__(self, rule: str):
        super().__init__(rule)


class _AlwaysRule(_MutExclRuleBase):
    pattern = '\A(\w*)\s([^!]*.)\s(\w*)'


class _NeverRule(_MutExclRuleBase):
    pattern = '\A(\w*)\s(!.)\s(\w*)'


class _TimeRule(_MutExclRuleBase):
    pattern = '(.*)(@t=\d*)\s(.{1,2})\s(.*)(@t=\d*)'


class _MultiplierRule(_CombRuleBase):
    pattern = None


class Parser:

    def __init__(self, rule: str) -> None:
        self.rule = rule

    def _dispatch(self):
        clsobj = None
        for cls in REGISTERED_MUTEXCL_RULES:
            obj = cls(self.rule)
            if obj.pattern is None:
                continue
            extracted = obj._extract_grammar()
            if extracted != []:
                clsobj = (cls, obj)
                break
        # if clsobj is None:
        #     raise ValueError('Did not recognise "{}" as valid syntax for an existing rule'.format(self.rule))
        return clsobj
