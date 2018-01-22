
var App = (App || {});
App.components = (App.components || {});
App.components.sidebar = function () {
  return ui._component('sidebar', {
    style: {
      'height': '100%',
      'width': '150px',
      'border-right': '1px solid black',
      'position': 'absolute',
      'opacity': '0',
      'left': '-150px',
    },
  }).then(function (_sidebar) {

    // vars

    // sidebar
    _sidebar.setStates([
      ui._state('club', {
        children: [
          ui._state('single', {
            fn: {
              animate: function (_this) {
                return _.d(0).then(function () {
                  return _this.show({style: {'left': '0%'}});
                });
              },
            },
          }),
        ],
      }),
    ]);

    return _sidebar;
  });
}
