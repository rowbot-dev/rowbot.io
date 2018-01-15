
/*

Members: a list of members and their roles

*/

var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = (App.interfaces.member || {});
App.interfaces.member.main = function () {
  return ui._component('member', {
    classes: ['interface', 'hidden'],
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

          // search
          ui._component('search', {
            style: {
              'border-top': '1px solid black',
              'border-bottom': '1px solid black',
              'height': '120px',
              'width': '100%',
            },
            children: [
              ui._component('fields', {
                style: {
                  'position': 'relative',
                  'width': 'calc(100% - 50px)',
                  'float': 'left',
                },
                children: [
                  Components.input('name', {
                    placeholder: 'Search name...',
                    style: {
                      'border': '0px',
                      ' input': {
                        'font-weight': 'bold',
                      },
                    },
                  }),
                  Components.input('email', {
                    placeholder: 'Search email...',
                    style: {
                      'border': '0px',
                    },
                  }),
                ],
              }),
              ui._component('buttons', {
                style: {
                  'position': 'relative',
                  'width': '40px',
                  'float': 'left',
                  'margin-left': '10px',
                },
                children: [
                  Components.button('new', {
                    style: {
                      'width': '40px',
                      'height': '40px',
                    },
                    children: [
                      Components.glyph('glyph', {
                        glyph: 'plus',
                      }),
                    ],
                  }),
                  Components.button('reload', {
                    style: {
                      'width': '40px',
                      'height': '40px',
                    },
                    children: [
                      Components.glyph('glyph', {
                        glyph: 'repeat',
                      }),
                    ],
                  }),
                ],
              }),
              Components.list('models', {
                style: {
                  'height': '40px',
                },
              }),
            ],
          }),

          // list of members
          Components.list('members', {
            style: {
              'height': 'calc(100% - 127px)'
            },
          }),
        ],
      }),
      App.interfaces.member.single(),
      App.interfaces.member.new(),
    ],
  }).then(function (_members) {

    // vars
    var _models = _members.get('all.search.models');
    var _newButton = _members.get('all.search.buttons.new');
    var _list = _members.get('all.members');
    var _input = _list.get('search.container.input');

    // interfaces
    var _single = _members.get('single');
    var _new = _members.get('new');

    // members
    _members.setStates([
      ui._state('members', {
        classes: {remove: ['hidden']},
      }),
    ]);

    // all.search.models
    _models.setTargets([
      _models._target('models', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.RoleModel.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          return [{
            key: 'club__id',
            value: api.active.Club._id,
          }];
        },
        normalise: function (_instance) {
          return _.p({
            _id: _instance._id,
            main: _instance.verbose_name,
          });
        },
        unit: function (name, args) {
          return Components.button(name, {
            style: {
              'border': '1px solid black',
              'padding': '6px',
              'margin-left': '10px',
              '.active': {
                'border': '1px solid green',
                'color': 'green',
              },
            }
          }).then(function (_unit) {

            _unit.isHidden = false;
            _unit.isActive = false; // on or off
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
                _this.isActive = !_this.isActive;
                if (_this.isActive) {
                  return _this.setClasses('active');
                } else {
                  return _this.removeClass('active');
                }
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _models.block = function (name, args) {
      return ui._component(`${name}`, _.merge({
        style: {
          'display': 'inline-block',
          'height': '40px',
        },
      }, args)).then(function (_block) {

        _block.isReleased = true;
        _block.types = {};
        _block.unit = function (_datum) {
          // get or create unit
          _block.datum = _datum;
          _block.isReleased = false;
          var _unit = _block.get(_block.types[_datum.target.name]);
          return _.p(function () {
            if (_unit) {
              return _unit.update(_datum);
            } else {
              var _unitName = _.id();
              _block.types[_datum.target.name] = _unitName;
              return _datum.target.unit(_unitName).then(function (_unit) {
                return _block.setChildren(_unit).then(function () {
                  return _unit.update(_datum);
                });
              });
            }
          }).then(function (_unit) {
            // hide all units except the active one
            return _.all(_block.children().map(function (_rest) {
              if (_rest.name !== _unit.name) {
                return _rest.hide();
              }
            })).then(function () {
              if (!_block.isReleased) {
                return _unit.show();
              } else {
                return _unit;
              }
            });
          });
        }
        _block.release = function () {
          // hide all units except the active one
          _block.isReleased = true;
          _block.datum = undefined;
          return _.all(_block.children().map(function (_unit) {
            return _unit.hide();
          }));
        }

        return _block;
      });
    }
    _models.get('search').setStyle({'display': 'none'});
    _models.get('pagination').setClasses('hidden');
    _models.setStates([
      ui._state('members', {
        fn: {
          after: function () {
            return _models.data.load.main();
          },
        },
      }),
    ]);

    // all.search.buttons.new
    _newButton.setBindings({
      'click': function (_this) {
        return ui.states.call('members.new');
      },
    });

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
          var data = [{
            key: 'roles__model__club__id',
            value: api.active.Club._id,
            q: 'AND',
          }];
          _.map(_query.buffer, function (_key, _value) {
            data.push({
              key: 'email__icontains',
              value: _value,
              q: 'OR',
            });
            data.push({
              key: 'first_name__icontains',
              value: _value,
              q: 'OR',
            });
            data.push({
              key: 'last_name__icontains',
              value: _value,
              q: 'OR',
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
          return ui._component(name, {
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
                return _this.datum.item.activate().then(function () {
                  return _single.load();
                }).then(function () {
                  return ui.states.call('members.single');
                });
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _list.get('search').setStyle({'display': 'none'});
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

    return _members;
  });
}
