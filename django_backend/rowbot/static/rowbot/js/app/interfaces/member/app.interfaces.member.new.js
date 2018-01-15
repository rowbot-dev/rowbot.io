
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = (App.interfaces.member || {});
App.interfaces.member.new = function () {
  return ui._component('new', {
    classes: ['panel', 'hidden'],
    children: [

      // title
      Components.text('title', {
        title: 'Invite a new member',
      }),

      // form
      Components.form('form', {
        children: [
          // member email
          Components.input('email', {
            placeholder: 'Email...',
            type: 'email',
            style: {
              'border-left': '0px',
              'border-right': '0px',
            },
          }),

          // member role models
          Components.text('title', {
            title: 'Available roles',
          }),
          Components.list('models', {
            style: {
              'height': '40px',
            },
          }),

          // submit button
          Components.button('submit', {
            style: {
              'height': '40px',
              'width': '100px',
              'border': '1px solid black',
              'float': 'left',
            },
            html: 'Create',
          }),

          // information
          Components.button('info', {
            classes: ['hidden'],
            style: {
              'height': '40px',
              'border': '1px solid black',
              'margin-left': '10px',
              'padding': '10px',
              'float': 'left',
              '.error': {
                'border': '1px solid red',
                'color': 'red',
              },
              '.success': {
                'border': '1px solid green',
                'color': 'green',
              },
            },
            html: 'Loading...',
          }),

          // member list
          Components.list('members', {
            style: {
              'height': '200px',
            },
          }),
        ],
      }),
    ],
  }).then(function (_new) {

    // vars
    var _form = _new.get('form');
    var _email = _form.get('email');
    var _members = _form.get('members');
    var _models = _form.get('models');
    var _info = _form.get('info');

    // new
    _new.setStates([
      ui._state('members', {
        children: [
          ui._state('single', {
            fn: {
              before: function (_this) {
                return _this.setClasses('hidden');
              },
            },
          }),
          ui._state('new', {
            fn: {
              before: function (_this) {
                return _this.removeClass('hidden');
              },
            },
          }),
        ],
      }),
    ]);

    // form
    _form.send = function (results) {
      // 1. first stage, check whether member exists
      return api.models.Member.objects.get({
        data: [
          {q: 'AND', key: 'first_name', value: results.first},
          {q: 'AND', key: 'last_name', value: results.last},
          {q: 'AND', key: 'email', value: results.email},
        ],
      }).then(function (_member) {
        if (_member) {
          // already exists, notify user in info button

        } else {
          // 2. does not exist, continue with the creation
          return api.models.Member.objects.create({
            username: _.id(), // temp
            email: results.email,
            first_name: results.first,
            last_name: results.last,
          }).then(function (_member) {
            // 3. with the member created, send activation email and wait for response
            return _member.send_activation_email().then(function (result) {
              if (result.success) {
                // 4. create roles
                return _.pmap(results.rolemodels, function (_id, _value) {
                  if (_value) { // should add role
                    return api.models.Role.objects.create({
                      model: _id,
                      member: _member._id,
                    }).then(function (_role) {
                      _.l(_role);
                    });
                  }
                }).then(function () {
                  // 5. finally, make changes to the interface and reload lists, etc.
                  // move to single state containing newly created member.
                });
              } else {
                // notify the user and send message to delete member
              }
            });
          });
        }
      });
    }

    // email
    _email.input = function (value, event) {
      return _members.metadata.query.add('main', value).then(function () {
        return _members.data.load.local();
      });
    }

    // members
    _members.setTargets([
      _members._target('members', {
        exclusive: true,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Member.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          var _target = this;
          return [
            {
              key: 'email__icontains',
              value: _members.metadata.query.main,
              q: 'OR',
            }
          ];
        },
        normalise: function (_instance) {
          return _.p({
            _id: _instance._id,
            first_name: _instance.first_name,
            last_name: _instance.last_name,
            main: _instance.email,
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
                value: _datum.normalised.main,
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
                _.l('click');
              },
            });

            return _unit;
          });
        },
      }),
    ]);
    _members.get('search').setClasses('hidden');
    _members.get('pagination').setClasses('hidden');
    _members.setStates([
      ui._state('members.new', {
        fn: {
          after: function () {
            return _members.data.load.main();
          },
        },
      }),
    ]);

    // models
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
              'margin-right': '10px',
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
    _models.get('search').setClasses('hidden');
    _models.get('pagination').setClasses('hidden');
    _models.setStates([
      ui._state('members', {
        children: [
          ui._state('new', {
            fn: {
              after: function () {
                return _models.data.load.main();
              },
            },
          }),
        ],
      }),
    ]);
    _models.export = function () {
      var active = _models.active().map(function (_active) {
        return {
          rolemodel: _active.datum.item._id,
          active: _active.isActive,
        }
      });

      var isValid = active.some(function (_active) {
        return _active.active;
      });

      return _.p(function () {
        if (!isValid) {
          return _models.error();
        }
      }).then(function () {
        return active.reduce(function (whole, part) {
          whole.value[part.rolemodel] = part.active;
          return whole;
        }, {name: 'rolemodels', validated: isValid, value: {}});
      });
    }
    _models.error = function () {
      return _.p();
    }

    // info
    _info.display = function (args) {
      args = (args || {});

    }

    return _new;
  });
}
