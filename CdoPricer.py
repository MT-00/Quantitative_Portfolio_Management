
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
        self.classB_notional = classB_notianal
        self.classA_coupon_rate = classA_coupon_rate
        self.classB_coupon_rate = classB_coupon_rate

        self.periods = self.years * self.frequency
        self.sim_size = len(default_dates)

        self.sim_cashflow = []
        self.sim_result = pd.DataFrame(index=range(self.sim_size),
                                       columns=['classA_default', 'classB_default'])
        self.sim_statistics = {'classA_default_rate': np.nan,
                               'classB_default_rate': np.nan}
        self._initialize_cashflow()

    def _initialize_cashflow(self):
        for i in range(self.sim_size):
            self.sim_cashflow.append(
                pd.DataFrame(index=list(range(1, self.periods + 1)),
                             columns=['bond_' + str(i) for i in range(self.bond_size)] +
                                     ['aggregated_cf', 'classA_required', 'classA_get', 'classB_required',
                                      'classB_get', 'classC_get']
                             )
            )

    def get_default_rate_parameters(self, classA_notionals):
        classA_default_rates = []
        for classA_notion in classA_notionals:
            self.classA_notional = classA_notion
            self.run()
            classA_default_rates.append(self.sim_statistics['classA_default_rate'])
        self.multi_default_rate = pd.DataFrame({'classA_notional': classA_notionals,
                                               'classA_default_rate': classA_default_rates})

    def run(self):
        self._get_bond_cf()
        self._get_portfolio_cf()
        self._get_class_required_cf()
        self._get_class_get_cf()
        self._get_sim_result()
        self._get_sim_statistics()

    def _get_bond_cf(self):
        for sim_num in range(self.sim_size):
            for bond_num in range(self.bond_size):
                bond_name = 'bond_' + str(bond_num)
                default_period = math.ceil(self.default_dates[sim_num][bond_num] * self.frequency)
                if default_period >= self.periods:
                    self.sim_cashflow[sim_num][bond_name] = self.face_value * self.coupon_rate / self.frequency
                    self.sim_cashflow[sim_num][bond_name].iloc[-1] += self.face_value
                else:
                    self.sim_cashflow[sim_num][bond_name].loc[:default_period] = self.face_value * self.coupon_rate \
                                                                                    / self.frequency
                    self.sim_cashflow[sim_num][bond_name].loc[default_period] = self.face_value * self.lgd
            self.sim_cashflow[sim_num] = self.sim_cashflow[sim_num].fillna(0)

    def _get_portfolio_cf(self):
        for sim_num in range(self.sim_size):
            self.sim_cashflow[sim_num]['aggregated_cf'] = self.sim_cashflow[sim_num][
                                                        ['bond_' + str(i) for i in range(self.bond_size)]].sum(axis=1)

    def _get_class_required_cf(self):
        for sim_num in range(self.sim_size):
            self.sim_cashflow[sim_num]['classA_required'] = self.classA_notional * self.classA_coupon_rate \
                                                            / self.frequency
            self.sim_cashflow[sim_num]['classA_required'].iloc[-1] += self.classA_notional
            self.sim_cashflow[sim_num]['classB_required'] = self.classB_notional * self.classB_coupon_rate \
                                                            / self.frequency
            self.sim_cashflow[sim_num]['classB_required'].iloc[-1] += self.classB_notional

    def _get_class_get_cf(self):
        for sim_num in range(self.sim_size):
            self.sim_cashflow[sim_num]['classA_get'] = self.sim_cashflow[sim_num][['aggregated_cf', 'classA_required']].min(axis=1)
            self.sim_cashflow[sim_num]['cf_afterA'] = self.sim_cashflow[sim_num]['aggregated_cf'] - self.sim_cashflow[sim_num]['classA_get']
            self.sim_cashflow[sim_num]['classB_get'] = self.sim_cashflow[sim_num][['cf_afterA', 'classB_required']].min(axis=1)
            self.sim_cashflow[sim_num]['classC_get'] = self.sim_cashflow[sim_num]['aggregated_cf'] \
                                                       - self.sim_cashflow[sim_num]['classA_get'] \
                                                       - self.sim_cashflow[sim_num]['classB_get']

    def _get_sim_result(self):
        for sim_num in range(self.sim_size):
            self.sim_result.loc[sim_num]['classA_default'] = sum(abs(self.sim_cashflow[sim_num]['classA_required']
                                                                     - self.sim_cashflow[sim_num]['classA_get'])) != 0
            self.sim_result.loc[sim_num]['classB_default'] = sum(abs(self.sim_cashflow[sim_num]['classB_required']
                                                                     - self.sim_cashflow[sim_num]['classB_get'])) != 0

    def _get_sim_statistics(self):
        self.sim_statistics['classA_default_rate'] = self.sim_result['classA_default'].mean()
        self.sim_statistics['classB_default_rate'] = self.sim_result['classB_default'].mean()

pricer = CdoPricer(
    default_dates=[[1.5, 2.2, 3.1, 12, 13],
                   [7, 7.3, 8.7, 17, 20],
                   [1.1, 1.9, 2.3, 5, 6],
                   [8, 1, 9, 9, 10.2],
                   [7.1, 5.2, 6.6, 8.8, 9.9]],
    bond_size=5,
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
pricer.run()
pricer.get_default_rate_parameters(classA_notionals=list(range(10000000, 80000000, 5000000)))

aa = pricer.sim_cashflow[1]
