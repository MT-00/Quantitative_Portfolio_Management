


class DefaultDateSimulator:
	def __init__(self, sim_size, bond_num, default_probability, target_corr_matrix):
		pass

	def run(self):
		self._get_clean_normals()
		self._get_correlated_geometric()

	def _clean_normals(self):
		pass

	def _cholesky_decomposition(self, matrix):
		pass

	

class CDOPricer
	def __init__(self, 
		default_probability, 
		lgd, 
		face_value, 
		coupon_rate, 
		coupon_period, 
		default_dates, 
		classA_notional,
		classB_notianal):
		pass

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
		pass

	def _get_portfolio_cf(self):
		pass

	def _get_class_cf(self):
		pass






