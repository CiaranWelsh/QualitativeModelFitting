import logging
import pandas as pd
from qualitative_model_fitting._parser import Parser

LOG = logging.getLogger(__name__)


class Runner:
    """
        The manual interface into model valiation

        This interface is intended for iteratively checking whether your
        model reproduces your observations. The :py:class:`manual_interface`
        is ideal for iteratively modifying a model and checking whether
        the required observations are met by your model.

        This contrasts with the :py:class:`automatic_interface` which will modify parameters
        automatically until it finds a set that complies with all observations.



        >>> antimony_string = '''
        ... model SimpleFeedback()
        ...     compartment Cell = 1;
        ...     var A in Cell;
        ...     var B in Cell;
        ...     var C in Cell;
        ...     const S;
        ...     const I;
        ...
        ...     A = 0;
        ...     B = 0;
        ...     C = 0;
        ...     S = 0;
        ...     I = 0;
        ...     BI = 0;
        ...
        ...     k1 = 0.1;
        ...     k2 = 0.1;
        ...     k3 = 0.1;
        ...     k4 = 0.1;
        ...     k5 = 10;
        ...     k6 = 0.1;
        ...     k7 = 0.1;
        ...     k8 = 0.1;
        ...
        ...     R1: => A            ; Cell * k1*S;
        ...     R2: A =>            ; Cell * k2*A*C;
        ...     R3: => B            ; Cell * k3*A;
        ...     R4: B =>            ; Cell * k4*B;
        ...     R5: B + I => BI     ; Cell * k5*B*I;
        ...     R6: BI => B + I     ; Cell * k6*BI;
        ...     R7: => C            ; Cell * k7*B;
        ...     R8: C =>            ; Cell * k8*C;
        ... end'''

        >>> input_string = '''
        ... timeseries None { S=0, I=0 } 0, 100, 101
        ... timeseries S { S=1, I=0 } 0, 100, 101
        ... timeseries I { S=0, I=1 } 0, 100, 101
        ... timeseries SI { S=1, I=1 } 0, 100, 101
        ... observation
        ...     Obs1: A[None]@t=0 > A[S]@t=10
        ...     Obs2: mean B[SI]@t=(0, 100) > C[I]@t=10
        ...     Obs3: C[SI]@t=10 == A[None]@t=10'''
        >>> Runner.run(antimony_string, input_string)


        Args:
            ant_str:
            input_string:

        Returns:

        """

    def __init__(self, ant_str, obs_str):
        self.ant_str = ant_str
        self.obs_str = obs_str

    def run(self):
        results = []
        parser = Parser(self.ant_str, self.obs_str)
        for obs in parser.observation_block:
            obs_result = dict(
                name=obs.name,
                observation=str(obs),
                evaluation=obs.reduce()
            )
            df = pd.DataFrame(obs_result, index=[0])
            results.append(df)
        df = pd.concat(results).reset_index(drop=True)
        return df

