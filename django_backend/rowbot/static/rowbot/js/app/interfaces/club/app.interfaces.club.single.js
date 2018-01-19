
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.club = (App.interfaces.club || {});
App.interfaces.club.single = function () {
  return ui._component('single', {
    classes: ['interface', 'hidden'],
    style: {
      'width': 'calc(100% - 190px)',
      'padding': '20px',
      'left': '-100px',
    },
    children: [
      // title
      Components.text('title', {
        title: 'Club',
      }),
    ],
  }).then(function (_single) {

    // vars

    // single
    _single.setStates([
      ui._state('club', {
        children: [
          ui._state('single', {
            fn: function (_this) {
              return _.d(30).then(function () {
                return _this.show({style: {'left': '150px'}});
              });
            },
          }),
        ],
      }),
    ]);

    return _single;
  });
}
