
var App = (App || {});
App.components = (App.components || {});
App.components.sidebar = function () {
  return ui._component('sidebar', {
    style: {
      'height': '100%',
      'width': '200px',
      'border-right': '1px solid black',
      'position': 'absolute',
      'opacity': '0',
      'left': '-200px',
    },
    children: [
      ui._component('crest', {
        style: {
          'height': '250px',
        },
      }),
      Components.buttonGroup('menu', {
        style: {
          ' .button': {
            'height': '40px',
            'border-bottom': '1px solid black',
          },
          ' .first': {
            'border-top': '1px solid black',
          },
          ' .hover': {
            'border-color': 'red',
            'color': 'red',
          },
          ' .before': {
            'border-bottom-color': 'red',
          },
        },
        children: [
          Components.button('events', {
            html: 'Events',
          }),
          Components.button('members', {
            html: 'Members',
          }),
          Components.button('teams', {
            html: 'Teams',
          }),
          Components.button('assets', {
            html: 'Assets',
          }),
        ],
      }),
    ],
  }).then(function (_sidebar) {

    // vars
    var _menu = _sidebar.get('menu');
    var _events = _menu.get('events');
    var _members = _menu.get('members');
    var _teams = _menu.get('teams');
    var _assets = _menu.get('assets');

    // sidebar
    _sidebar.setStates([
      ui._state('club', {
        fn: {
          before: function (_this) {
            return _this.hide({style: {'left': '-200px'}});
          },
        },
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
      ui._state('event', {
        fn: {
          before: function (_this) {
            return _this.hide({style: {'left': '-200px'}});
          },
          animate: function (_this) {
            return _this.show({style: {'left': '0%'}});
          },
        },
      }),
    ]);

    // menu
    _events.setBindings({
      'click': function (_this) {
        return ui.states.call('event');
      },
    });
    _members.setBindings({
      'click': function (_this) {
        return ui.states.call('member');
      },
    });
    _teams.setBindings({
      'click': function (_this) {
        return ui.states.call('team');
      },
    });
    _assets.setBindings({
      'click': function (_this) {
        return ui.states.call('asset');
      },
    });

    return _sidebar;
  });
}
