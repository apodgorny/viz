# ======================================================================
# Series description and data container for visualization
# ======================================================================

class VizInfo:
	valid_attrs = {
		'color' : str,
		'size'  : int,
	}

	def __init__(self, name, data, **attrs):
		self.name  = name
		self.data  = list(data)
		self.attrs = {}

		for key, value in attrs.items():
			if key in self.valid_attrs and value is not None:
				self.attrs[key] = self.valid_attrs[key](value)

	def __len__(self):
		return len(self.data)
