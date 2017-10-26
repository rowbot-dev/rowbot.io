
var Test = (Test || {});
Test.components = (Test.components || {});
Test.components.panel = function (name, args) {
  return ui._component(name, _.merge({
    
  }, args)).then(function (_panel) {
    return _panel;
  });
}
