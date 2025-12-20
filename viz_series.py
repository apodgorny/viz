# ======================================================================
# Series description and data container for visualization
# ======================================================================

class VizSeries:
	valid_attrs = {
		'color' : str,
		'width' : int,
		'units' : str,
		'dots'  : bool
	}

	def __init__(self, data, name=None, **attrs):
		self.name  = name
		self.data  = list(data)
		self.attrs = {}

		for key, value in attrs.items():
			if key in self.valid_attrs and value is not None:
				self.attrs[key] = self.valid_attrs[key](value)

	def __len__(self):
		return len(self.data)
