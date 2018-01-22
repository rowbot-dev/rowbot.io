
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
      Components.text('title'),

      // events
      Components.list('events', {
        style: {
          'height': '500px',
        },
      }),
    ],
  }).then(function (_single) {

    // vars
    var _title = _single.get('title');
    var _events = _single.get('events');

    // single
    _single.setStates([
      ui._state('club', {
        children: [
          ui._state('single', {
            fn: {
              after: function (_this) {
                return _events.data.load.main();
              },
              animate: function (_this) {
                return _.all([
                  _this.show({style: {'left': '150px'}}),
                  _title.update({title: api.active.Club.name}),
                ]);
              },
            },
          }),
        ],
      }),
    ]);

    // events
    _events.setTargets([
      _events._target('events', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.EventInstance.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          args = (args || {});
          var _target = this;
          var _query = (args.query || _events.metadata.query);
          return [];
        },
        normalise: function (_instance) {
          return _instance.related('event').then(function (_event) {
            return {
              _id: _instance._id,
              main: _event.name,
            }
          });
        },
        unit: function (name, args) {
          return ui._component(name, {
            style: {
              'width': '100%',
              'height': '200px',
              'border-bottom': '1px solid black',
              'padding': '10px',
              'clear': 'left',
            },
            children: [
              ui._component('crest', {
                classes: ['notouch'],
                style: {
                  'width': '100px',
                  'height': '100px',
                  'position': 'relative',
                  'float': 'left',
                  'background-color': '#ccc',
                },
              }),
              ui._component('details', {
                classes: ['notouch'],
                style: {
                  'padding': '10px',
                  'height': '100%',
                  'width': 'calc(100% - 100px)',
                  'position': 'relative',
                  'float': 'left',
                },
                children: [
                  Components.text('name', {
                    classes: ['notouch'],
                  }),
                ],
              }),
            ],
          }).then(function (_unit) {

            // vars
            var _name = _unit.get('details.name');

            _unit.isHidden = false;
            _unit.update = function (_datum) {
              _unit.datum = _datum;
              return _name.update({
                title: _datum.normalised.main,
              }).then(function () {
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
                return _this.datum.item.activate().then(function () {
                  _.l('event');
                });
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _events.get('search').setClasses('hidden');
    _events.get('pagination').setClasses('hidden');

    return _single;
  });
}
