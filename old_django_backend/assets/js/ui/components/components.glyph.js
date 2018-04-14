
var Components = (Components || {});
Components.glyph = function (name, args) {
  return ui._component(name, _.merge({
    tag: 'span',
    classes: ['glyphicon', `glyphicon-${args.glyph}`, 'notouch'],
  }, args)).then(function (_glyph) {
    return _glyph;
  })
}
