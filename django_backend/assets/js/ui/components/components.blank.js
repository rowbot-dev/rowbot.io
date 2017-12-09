
// var SourceComponents = (SourceComponents || {});
// SourceComponents.context = (SourceComponents.context || {});
// SourceComponents.context.view = (SourceComponents.context.view || {});
blank = function (name, args) {
  return ui._component(name, _.merge({

  }, args)).then(function (_blank) {
    return _blank;
  });
}
