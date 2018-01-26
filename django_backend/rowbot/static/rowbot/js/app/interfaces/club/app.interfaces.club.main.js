
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.club = (App.interfaces.club || {});
App.interfaces.club.main = function () {
  return ui._component('club', {
    classes: ['interface', 'hidden'],
    style: {
      'padding': '20px',
      'opacity': '0',
    },
    children: [
      ui._component('all', {
        style: {
          'width': '100%',
          'height': '100%',
        },
        children: [
          // title
          Components.text('title', {
            title: 'Clubs you are a part of',
            style: {

            },
          }),

          // list of clubs
          Components.list('clubs', {
            style: {
              'height': 'calc(100% - 57px)', // accounts for padding and height of title
            },
          }),
        ],
      }),
      App.interfaces.club.single(),
    ],
  }).then(function (_club) {

    // vars
    var _all = _club.get('all');
    var _clubs = _all.get('clubs');

    // interfaces


    // club
    _club.setStates([
      ui._state('club', {
        fn: {
          animate: function (_this) {
            return _.d(300).then(function () {
              return _this.show();
            });
          }
        },
      }),
      ui._state('event', {
        fn: {
          animate: function (_this) {
            return _this.hide();
          }
        },
      }),
    ]);

    // all
    _all.setStates([
      ui._state('club', {
        children: [
          ui._state('single', {
            fn: {
              animate: function (_this) {
                return _this.hide({style: {'left': '-100%'}});
              },
            },
          }),
        ],
      }),
    ]);

    // clubs
    _clubs.setTargets([
      _clubs._target('clubs', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Club.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          args = (args || {});
          var _target = this;
          var _query = (args.query || _clubs.metadata.query);
          return [];
        },
        normalise: function (_instance) {
          return _.p({
            _id: _instance._id,
            main: _instance.name,
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
                  return ui.states.call('club.single');
                });
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _clubs.get('search').setClasses('hidden');
    _clubs.get('pagination').setClasses('hidden');
    // _members.data.storage.compare = function (_d1, _d2) { // override
    //   if ((_d1.scores.first_name + _d1.scores.last_name) > (_d2.scores.first_name + _d2.scores.last_name)) {
    //     return -1;
    //   } else if ((_d1.scores.first_name + _d1.scores.last_name) === (_d2.scores.first_name + _d2.scores.last_name)) {
    //     if (_d1.normalised.email < _d2.normalised.email) {
    //       return -1;
    //     } else if (_d1.normalised.email === _d2.normalised.email) {
    //       return 0;
    //     } else {
    //       return 1;
    //     }
    //   } else {
    //     return 1;
    //   }
    // }
    // _members.metadata.query.score = function (_datum) {
    //   var _query = this;
    //   var _target = _datum.target;
    //   return _.p(function () {
    //     return _.map(_datum.normalised, function (_key, _value) {
    //       let results = {};
    //       let exclusive = (_members.metadata.exclusive || _target.exclusive);
    //       let noQuery = true;
    //       let _score = _.map(_query.buffer, function (_index, _partial) {
    //         noQuery = _partial === '';
    //         return _value.score(_partial);
    //       }).mean();
    //       results[_key] = (_score === 0 && !exclusive && noQuery) ? 1 : _score;
    //       return results;
    //     }).reduce(function (whole, part) {
    //       return _.merge(whole, part);
    //     }, {});
    //   });
    // }
    // _members.data.display.filter.condition = function (_datum) { // override
    //   return _.p(function () {
    //     _datum.accepted = _datum.scores.first_name > 0 || _datum.scores.last_name > 0 || _datum.scores.email > 0;
    //   });
    // }
    _clubs.setStates([
      ui._state('club', {
        fn: {
          before: function (_this) {
            return _this.data.load.local();
          },
          after: function (_this) {
            return _this.data.load.remote();
          },
        },
      }),
    ]);

    return _club;
  });
}
