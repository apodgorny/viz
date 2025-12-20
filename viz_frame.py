# ======================================================================
# Visualization frame holding series and info columns
# ======================================================================

import json

from viz_series import VizSeries
from viz_info   import VizInfo


class VizFrame:
	def __init__(self, *cols):
		self.cols = {}

		for col in cols:
			if isinstance(col, (VizSeries, VizInfo)):
				self.add(col)
			else:
				raise TypeError(f'Unsupported column type for `{name}`: {type(value)}')

	# ==================================================================
	# PUBLIC METHODS
	# ==================================================================

	# Add numeric series column.
	# ------------------------------------------------------------------
	def add(self, col):
		self.cols[col.name] = col

	# Convert frame into json-serializable structure.
	# ------------------------------------------------------------------
	def to_json(self):
		columns = []
		rows    = []

		length = 0
		for col in self.cols.values():
			length   = max(length, len(col))
			col_data = {
				'name' : col.name,
				'type' : col.__class__.__name__
			}
			col_data.update(col.attrs)
			columns.append(col_data)

		for idx in range(length):
			row = {}
			for col in self.cols.values():
				row[col.name] = col.data[idx] if idx < len(col) else None
			rows.append(row)

		return json.dumps({
			'columns' : columns,
			'rows'    : rows
		}, ensure_ascii=False, indent=2)
