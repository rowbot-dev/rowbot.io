
/*

Members: a list of members and their roles

*/

var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = function () {
  return ui._component('member', {
    classes: ['interface'],
    style: {
      'padding-left': '20px',
      ' .panel': {
        'float': 'left',
        'width': '410px',
        'height': '100%',
        'margin-right': '25px',
      },
    },
    children: [
      ui._component('all', {
        classes: ['panel'],
        children: [
          // title
          Components.text('title', {
            title: 'Members',
          }),

          // new
          App.components.new('member', {

          }),

          // list
          Components.list('members', {

          }),
        ],
      }),
      ui._component('single', {
        classes: ['panel', 'hidden'],
        children: [
          // member name
          Components.input('name'),

          // member email
          Components.input('email', {
            style: {
              'display': 'inline-block',
            },
          }),

          // member activation
          Components.text('activation', {
            style: {
              '.activated': {
                'color': 'green',
                'border': '1px solid green',
              },
              'color': 'red',
              'border': '1px solid red',
              'display': 'inline-block',
              'padding-left': '8px',
              'padding-right': '8px',
            },
          }),

          // member new role
          App.components.new('role', {

          }),

          // member role list
          Components.list('roles', {

          }),
        ],
      }),
    ],
  }).then(function (_members) {

    // vars
    var _list = _members.get('all.members');
    window.member_list = _list;
    var _input = _list.get('search.container.input');
    var _single = _members.get('single');
    var _activation = _single.get('activation');
    var _roles = _single.get('roles');

    // all.list
    _list.setTargets([
      _list._target('members', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Member.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          args = (args || {});
          var _target = this;
          var _query = (args.query || _list.metadata.query);
          var data = [];
          _.map(_query.buffer, function (_key, _value) {
            data.push({
              server: 'email__icontains',
              value: _value,
            });
            data.push({
              server: 'first_name__icontains',
              value: _value,
            });
            data.push({
              server: 'last_name__icontains',
              value: _value,
            });
          });
          return data;
        },
        normalise: function (_instance) {
          return _.p({
            _id: _instance._id,
            first_name: _instance.first_name,
            last_name: _instance.last_name,
            email: _instance.email,
          });
        },
        unit: function (name, args) {
          return ui._component(`${name}`, {
            style: {
              'width': '100%',
              'height': 'auto',
              'border-bottom': '1px solid black',
              'padding-left': '10px',
              'padding-right': '10px',
            },
            children: [
              Components.text('text', {
                classes: ['notouch'],
              }),
            ],
          }).then(function (_unit) {

            _unit.isHidden = false;
            _unit.update = function (_datum) {
              _unit.datum = _datum;
              return _unit.get('text').update({
                title: `${_datum.normalised.first_name} ${_datum.normalised.last_name}`,
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
            _unit.setBindings({
              'click': function (_this, event) {
                return _single.load(_this.datum.item._id).then(function () {
                  return ui.states.call('members.single');
                });
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _list.data.storage.compare = function (_d1, _d2) { // override
      if ((_d1.scores.first_name + _d1.scores.last_name) > (_d2.scores.first_name + _d2.scores.last_name)) {
        return -1;
      } else if ((_d1.scores.first_name + _d1.scores.last_name) === (_d2.scores.first_name + _d2.scores.last_name)) {
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
    _list.metadata.query.score = function (_datum) {
      var _query = this;
      var _target = _datum.target;
      return _.p(function () {
        return _.map(_datum.normalised, function (_key, _value) {
          let results = {};
          let exclusive = (_list.metadata.exclusive || _target.exclusive);
          let noQuery = true;
          let _score = _.map(_query.buffer, function (_index, _partial) {
            noQuery = _partial === '';
            return _value.score(_partial);
          }).mean();
          results[_key] = (_score === 0 && !exclusive && noQuery) ? 1 : _score;
          return results;
        }).reduce(function (whole, part) {
          return _.merge(whole, part);
        }, {});
      });
    }
    _list.data.display.filter.condition = function (_datum) { // override
      return _.p(function () {
        _datum.accepted = _datum.scores.first_name > 0 || _datum.scores.last_name > 0 || _datum.scores.email > 0;
      });
    }
    _list.setStates([
      ui._state('members', {
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
        return _list.data.load.local();
      });
    }

    // single
    _single.load = function (_id) {
      // loads a member id from the api buffer
      return api.get('Member', _id).then(function (_member) {
        return _.all([
          _single.get('name').setContent(`${_member.first_name} ${_member.last_name}`),
          _single.get('email').setContent(_member.email),
          _activation.load({activated: _member.is_activated}),
          _roles.load(_id),
        ]);
      });
    }
    _single.setStates([
      ui._state('members', {
        children: [
          ui._state('single', {
            fn: {
              before: function (_this) {
                return _this.removeClass('hidden');
              },
            },
          }),
        ],
      }),
    ]);

    // single.activation
    _activation.load = function (args) {
      args = (args || {});
      if (args.activated) {
        return _activation.update({value: 'Activated'}).then(function () {
          return _activation.setClasses('activated');
        });
      } else {
        return _activation.update({value: 'Not yet activated'}).then(function () {
          return _activation.removeClass('activated');
        });
      }
    }

    // single.roles
    _roles.load = function (_id) {
      return api.get('Member', _id).then(function (_member) {

      });
    }

    return _members;
  });
}
