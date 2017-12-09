
var Components = (Components || {});
Components.text = function (name, args) {
  args = (args || {});
  return ui._component(name, _.merge({
    children: [
      ui._component('title', {
        tag: 'h3',
        style: {
          'display': args.title !== undefined ? 'block' : 'none',
        },
        html: args.title,
      }),
      ui._component('value', {
        tag: 'p',
        style: {
          'display': args.value !== undefined ? 'block' : 'none',
        },
        html: args.value,
      }),
    ],
  }, args)).then(function (_text) {
    _text.title = args.title;
    _text.value = args.value;
    _text.update = function (_args) {
      _args = (_args || {});
      return _.all([
        _text.get('title').setHTML((_args.title || _text.title)),
        _text.get('title').setStyle({'display': _args.title ? 'block' : 'none'}),
        _text.get('value').setHTML((_args.value || _text.value)),
        _text.get('value').setStyle({'display': _args.value ? 'block' : 'none'}),
      ]);
    }
    return _text;
  });
}
