
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.load = function () {
  return ui._component('load', {
    style: {
      'height': '100%',
      'width': '100%',
    },
    children: [
      // loading display
      Components.text('display', {
        style: {
          'width': '200px',
          'float': 'left',
          'text-align': 'center',
        },
        classes: ['centred'],
        title: 'Loading...',
      }),
    ],
  }).then(function (_load) {

    _load.load = function () {
      return _.all([
        api.models.EventModel.objects.all(),
        api.models.Event.objects.all(),
        api.models.Club.objects.all(),
        api.models.Role.objects.all(),
        api.models.RoleModel.objects.all(),
        api.models.Member.objects.all(),
      ]).then(function () {
        return ui.states.call('club');
      });
    }

    _load.setStates([
      ui._state('load', {
        fn: {
          after: function (_this) {
            return _this.load();
          },
        },
      }),
      ui._state('club', {
        fn: {
          animate: function (_this) {
            return _this.hide();
          },
        },
      }),
    ]);

    return _load;
  });
}
