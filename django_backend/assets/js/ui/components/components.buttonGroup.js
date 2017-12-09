
var Components = (Components || {});
Components.buttonGroup = function (name, args) {
  return ui._component(name, _.merge({

  }, args)).then(function (_buttonGroup) {

    _buttonGroup.setHover = function (index) {
      return _.all(_buttonGroup.children().map(function (_button, _index) {
        if (_index === index) {
          return _button.setClasses(['hover']);
        } else if (_index === index - 1) {
          return _button.setClasses(['before']);
        } else {
          return _.all([
            _button.removeClass('hover'),
            _button.removeClass('before'),
          ]);
        }
      }));
    }

    // map bindings to all children
    _buttonGroup.children().map(function (_button, index) {
      _button.setBindings({
        'mouseover': function (_this, event) {
          _buttonGroup.setHover(index);
        },
        'mouseout': function (_this, event) {
          _buttonGroup.setHover();
        }
      });
    });

    return _buttonGroup;
  });
}
