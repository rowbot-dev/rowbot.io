
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = (App.interfaces.role || {});
App.interfaces.role.root = (App.interfaces.role.root || {});
App.interfaces.role.root.main = function () {
  return ui._component('root', {
    classes: ['interface'],
    style: {
      ' .panel': {
        'position': 'relative',
        'float': 'left',
        'padding-left': '10px',
        'height': '100%',
      },
    },
    children: [
      // main list
      ui._component('all', {
        classes: ['panel'],
        children: [
          Components.text('title', {
            title: 'Roles',
          }),
          Components.button('new', {
            style: {
              'border': '1px solid black',
              'padding': '8px',
              'width': '385px',
              'margin-bottom': '10px',
            },
            html: 'Add a role to a member',
          }),
          Components.list('list', {
            tramline: true,
            style: {
              'width': '400px',
              'height': '600px',
            },
          }),
        ],
      }),

      // focus interface
      App.interfaces.role.root.focus(),
    ],
  }).then(function (_root) {

    var _list = _root.get('all.list');
    var _input = _list.get('search.input');

    _list.setTargets([
      _list._target('roles', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Role.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          args = (args || {});
          var _target = this;
          var _query = (args.query || _list.metadata.query);
          var data = [];
          _.map(_query.buffer, function (_key, _value) {
            data.push({
              server: 'member__email__icontains',
              value: _value,
            });
            data.push({
              server: 'model__verbose_name__icontains',
              value: _value,
            });
          });
          return data;
        },
        normalise: function (_instance) {
          return _.all([
            _instance.relation('model'),
            _instance.relation('member'),
          ]).then(function (results) {
            var [_model, _member] = results;
            return {
              _id: _instance._id,
              model: _model.verbose_name,
              email: _member.email,
            }
          });
        },
        unit: function (name, args) {
          return ui._component(`${name}`, {
            style: {
              'width': '100%',
              'height': 'auto',
              'border-bottom': '1px solid black',
              'padding': '10px',
            },
            children: [
              Components.text('text'),
            ],
          }).then(function (_unit) {

            _unit.isHidden = false;
            _unit.update = function (_datum) {
              _unit.datum = _datum;
              return _unit.get('text').update({
                title: _datum.normalised.model,
                value: _datum.normalised.email,
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

            return _unit;
          });
        },
      }),
    ]);
    _list.data.storage.compare = function (_d1, _d2) { // override
      if (_d1.scores.model > _d2.scores.model) {
        return -1;
      } else if (_d1.scores.model === _d2.scores.model) {
        if (_d1.normalised.email < _d2.normalised.email) {
          return -1;
        } else if (_d1.normalised.email === _d2.normalised.email) {
          return 0;
        } else {
          return 1;
        }
      } else {
        return 1;
      }
    }
    _list.metadata.exclusive = true;
    _list.metadata.query.score = function (_datum) {
      var _query = this;
      var _target = _datum.target;
      return _.p(function () {
        return _.map(_datum.normalised, function (_key, _value) {
          let results = {};
          let exclusive = (_list.metadata.exclusive || _target.exclusive);
          let _score = _.map(_query.buffer, function (_index, _partial) {
            return _value.score(_partial);
          }).mean();
          results[_key] = _score === 0 ? (exclusive ? 0 : 1) : _score;
          return results;
        }).reduce(function (whole, part) {
          return _.merge(whole, part);
        }, {});
      });
    }
    _list.data.display.filter.condition = function (_datum) { // override
      return _.p(function () {
        _datum.accepted = _datum.scores.model > 0 || _datum.scores.email > 0;
      });
    }
    _list.setStates([
      ui._state('roles', {
        fn: {
          after: function () {
            return _list.data.load.main();
          },
        },
      }),
    ]);
    _list.get('pagination').setClasses('hidden');
    _input.input = function (value, event) {
      return _.pmap(value.split(' '), function (_index, _value) {
        return _list.metadata.query.add(_index, _value);
      }).then(function () {
        if (value === '') {
          return _list.data.load.main();
        }
      });
    }

    return _root;
  });
}
