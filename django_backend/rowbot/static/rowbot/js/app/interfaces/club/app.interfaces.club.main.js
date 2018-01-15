
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.club = (App.interfaces.club || {});
App.interfaces.club.main = function () {
  return ui._component('club', {
    classes: ['hidden'],
    style: {
      'height': '100%',
      'width': '100%',
      'opacity': '0',
    },
  }).then(function (_club) {

    _club.setStates([
      ui._state('club', {
        fn: {
          after: function (_this) {
            return _this.show(300);
          },
        },
      }),
    ]);

    return _club;
  });
}
