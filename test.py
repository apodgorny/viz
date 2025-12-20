# ======================================================================
# Manual test for Viz interactive plotting
# ======================================================================

import math

from viz import Viz
x = list(range(50))

def main():
	frame = Viz.Frame(
		Viz.Series(
			name  = 'Late Interaction',
			data  = [math.sin(i / 5) + 1 for i in x],
			color = '#ff5555',
			units = 'score',
			dots  = True
		),
		Viz.Series(
			name  = 'Bayes',
			data  = [math.cos(i / 7) + 1 for i in x],
			color = '#55ff55',
			units = 'prob',
			dots  = False
		),
		Viz.Info(
			name = 'Sample text 1',
			data = [f'Sample 1 #{i}: synthetic test sentence' for i in x]
		),
		Viz.Info(
			name = 'Sample text 2',
			data = [f'Sample 2 #{i}: synthetic test sentence' for i in x]
		),
	)

	Viz.render(
		view = 'plot',
		data = frame
	)

	return None


if __name__ == '__main__':
	main()
