
/*

The role interface should show a list of roles and any individual role.

What roles to display:
1. Admin: all users' roles
2. User: only their roles

*/

var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.role = function () {
  return ui._component('role', {
    classes: ['interface'],
    children: [
      ui._component('single', {
        classes: ['interface', 'hidden'],
      }),
      ui._component('new', {
        classes: ['interface', 'hidden'],
      }),
      ui._component('newModel', {
        classes: ['interface', 'hidden'],
      }),
      ui._component('all', {
        classes: ['interface'],
        style: {
          'padding-left': '10px',
        },
        children: [
          Components.text('title', {
            title: 'Roles',
          }),
          Components.list('list', {
            tramline: true,
            style: {
              'width': '600px',
              'height': '600px',
            },
          }),
        ],
      }),
    ],
  }).then(function (_role) {

    var _list = _role.get('all.list');
    var _input = _list.get('search.input');

    _list.setTargets([
      _list._target('roles', {
        exclusive: false,
        source: function (force) {
          var _target = this;
          return api.models.Role.objects.all();
        },
        normalise: function (_item) {
          return _.all([
            _item.relation('model'),
            _item.relation('member'),
          ]).then(function (results) {
            var [_model, _member] = results;
            return {
              _id: _item._id,
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
              'border': '1px solid black',
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
            // _.l(_partial, _value, _value.score(_partial, exclusive));
            return _value.score(_partial, exclusive);
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
            return _list.data.load();
          },
        },
      }),
    ]);
    _list.get('pagination').setClasses('hidden');
    _input.input = function (value, event) {
      return _.p(function () {
        value.split(' ').forEach(function (_value, index) {
          _list.metadata.query.buffer[index] = _value;
        });
        return _list.data.load();
      });
    }

    return _role;
  });
}
