Components = (Components || {});
Components.text = function (id, args) {
	return UI.createComponent(id, {
		name: args.name,
		template: UI.template('div', 'ie'),
		appearance: args.appearance,
		children: [
			UI.createComponent(`${id}-title`, {
				name: 'title',
				template: UI.template('p'),
				appearance: {
					html: args.title,
					style: {
						'font-size': '16px',
						'display': (args.title ? 'block' : 'none'),
					},
				},
			}),
			UI.createComponent(`${id}-value`, {
				name: 'value',
				template: UI.template('p'),
				appearance: {
					html: args.value,
					style: {
						'display': (args.value ? 'block' : 'none'),
					},
				},
			}),
		],
	}).then(function (_text) {
		return _text;
	})
}