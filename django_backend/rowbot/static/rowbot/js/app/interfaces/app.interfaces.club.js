
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.club = function () {
  return ui._component('club', {
    classes: ['interface'],
    style: {
      'padding-left': '20px',
    },
    children: [
      Components.text('title', {
        title: 'Rowbot.io',
      }),
      Components.list('clubs', {

      }),
    ],
  }).then(function (_club) {

    var _list = _club.get('clubs');

    // list
    _list.setTargets([
      _list._target('clubs', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Club.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          return [{
            // server: ''
          }];
        },
        normalise: function (_instance) {
          return _.p({
            _id: _instance._id,
            main: _instance.name,
          });
        },
        unit: function (name, args) {
          return Components.button(name, {

          }).then(function (_unit) {

            _unit.isHidden = false;
            _unit.update = function (_datum) {
              _unit.datum = _datum;
              return _unit.setHTML(_datum.normalised.main).then(function () {
                return _unit;
              });
            }
            _unit.hide = function () {
              _unit.isHidden = true;
              return _unit.setClasses('hidden');
            }
            _unit.show = function () {
              _unit.isHidden = false;
              return _unit.removeClass('hidden');
            }
            _unit.setBindings({
              'click': function (_this, event) {
                return _unit.datum.item.activate().then(function () {
                  return ui.states.call('members');
                });
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _list.get('search').setStyle({

    });
    _list.get('pagination').setClasses('hidden');
    _list.setStates([
      ui._state('clubs', {
        fn: {
          after: function () {
            return _list.data.load.main();
          },
        },
      }),
    ]);

    // club
    _club.setStates([
      ui._state('members', {
        classes: ['hidden'],
      }),
    ]);

    return _club;
  });
}
