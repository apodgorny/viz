$(function () {
	render_plot(window.VIZ_DATA)
})

function render_plot(payload) {
	const columns = payload.columns
	const rows    = payload.rows

	const x = rows.map((_, i) => i)

	const traces   = []
	const infoCols = []

	$.each(columns, function (_, col) {
		if (col.type === 'VizSeries') {
			const y = rows.map(r => r[col.name])

			traces.push({
				x          : x,
				y          : y,
				mode       : col.dots ? 'lines+markers' : 'lines',
				name       : col.name,
				line       : {
					color : col.color || '#ffffff',
					width : col.width || 2
				},
				hoverinfo  : 'x+y+name'
			})
		}

		if (col.type === 'VizInfo') {
			infoCols.push(col.name)
		}
	})

	const layout = {
		paper_bgcolor : '#000000',
		plot_bgcolor  : '#000000',
		font          : { color: '#dddddd' },
		xaxis         : { title: 'Chunks' },
		yaxis         : { title: 'Value' },
		legend        : { orientation: 'h' },
		hovermode     : 'x unified',
		hoverdistance : 100,
		spikedistance : -1
	}

	Plotly.newPlot('plot', traces, layout, { displayModeBar: false })

	const $plot = $('#plot')
	const $info = $('#row')

	const renderInfo = function (index) {
		const row = rows[index]
		$info.empty()

		if (row) {
			$.each(infoCols, function (_, key) {
				const value = row[key]
				if (value === undefined || value === null) {
					return
				}

				const $line  = $('<div>').addClass('info-row')
				const $label = $('<div>').addClass('info-label').text(key)
				const $value = $('<div>').addClass('info-value').text(String(value))

				$line.append($label)
				$line.append($value)
				$info.append($line)
			})
		}
	}

	$plot.on('plotly_hover', function (_, event) {
		const point = event && event.points && event.points[0]
		const index = point ? point.pointIndex : 0
		renderInfo(index)
	})

	renderInfo(0)
}
