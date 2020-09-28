
import math
import numpy as np
import pandas as pd
import dateutil
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


class CdoPricer:
    def __init__(self,
                 default_dates=[],
                 bond_size=10,
                 default_probability=0.04,
                 lgd=0.6,
                 face_value=10000000,
                 coupon_rate=0.06,
                 years=5,
                 frequency=4,
                 risk_free_rate=0.01,
                 classA_notional=20000000,
                 classB_notianal=10000000,
                 classA_coupon_rate=0.02,
                 classB_coupon_rate=0.04):

        self.default_dates = default_dates
        self.bond_size = bond_size
        self.default_probability = default_probability
        self.lgd = lgd
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.years = years
        self.frequency = frequency
        self.risk_free_rate = risk_free_rate
        self.classA_notional = classA_notional
        self.classB_notianal = classB_notianal
        self.classA_coupon_rate = classA_coupon_rate
        self.classB_coupon_rate = classB_coupon_rate

        self.periods = self.years * self.frequency
        self.sim_size = len(default_dates)

        self.sim_cashflow = []
        self._initialize_cashflow()

    def _initialize_cashflow(self):
        for i in range(self.sim_size):
            self.sim_cashflow.append(
                pd.DataFrame(index=list(range(1, self.periods + 1)),
                             columns=['bond_' + str(i) for i in range(self.bond_size)] +
                                     ['aggregated_cf', 'classA_target', 'classA_get', 'classB_target', 'classB_get',
                                      'classC_get']
                             )
            )

    def get_default_rate(self):
        pass

    def get_default_rate_parameters(self):
        # loop _get_class_cf(), _get_default_rate()
        pass

    def get_cash_flow(self):
        self._get_bond_cf()
        self._get_portfolio_cf()
        self._get_class_cf()

    def _get_bond_cf(self):
        for sim_num in range(self.sim_size):
            for bond_num in range(self.bond_size):
                bond_name = 'bond_' + str(bond_num)
                default_period = math.ceil(self.default_dates[sim_num][bond_num] * self.frequency)
                if default_period >= self.periods:
                    self.sim_cashflow[sim_num][bond_name] = self.face_value * self.coupon_rate / self.frequency
                    self.sim_cashflow[sim_num][bond_name].iloc[-1] = self.sim_cashflow[sim_num][bond_name].iloc[-1] + self.face_value
                else:
                    self.sim_cashflow[sim_num][bond_name][:default_period] = self.face_value * self.coupon_rate / self.frequency
                    self.sim_cashflow[sim_num][bond_name][default_period] = self.face_value * self.lgd
            self.sim_cashflow[sim_num] = self.sim_cashflow[sim_num].fillna(0)

    def _get_portfolio_cf(self):
        for sim_num in range(self.sim_size):
            self.sim_cashflow[sim_num]['aggregated_cf'] = self.sim_cashflow[sim_num][['bond_'+str(i) for i in range(self.bond_size)]].sum(axis=1)


    def _get_class_cf(self):
        pass


pricer = CdoPricer(
    default_dates=[[1.5, 2.2, 3.1], [7, 2.3, 3.7], [1.1, 1.9, 2.3]],
    bond_size=3,
    default_probability=0.04,
    lgd=0.6,
    face_value=10000000,
    coupon_rate=0.06,
    years=5,
    frequency=4,
    risk_free_rate=0.01,
    classA_notional=20000000,
    classB_notianal=10000000,
    classA_coupon_rate=0.02,
    classB_coupon_rate=0.04
)
pricer._get_bond_cf()
pricer._get_portfolio_cf()