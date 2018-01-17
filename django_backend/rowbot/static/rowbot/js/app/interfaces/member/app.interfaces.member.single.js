
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.member = (App.interfaces.member || {});
App.interfaces.member.single = function () {
  return ui._component('single', {
    classes: ['panel', 'hidden'],
    children: [
      // member name
      Components.text('name'),

      // member email
      Components.text('email', {
        style: {
          'display': 'inline-block',
        },
      }),

      // member activation
      Components.text('activation', {
        style: {
          '.activated': {
            'color': `${Color.green.dark}`,
            'border': `1px solid ${Color.green.dark}`,
          },
          'color': 'red',
          'border': '1px solid red',
          'display': 'inline-block',
          'padding-left': '5px',
          'padding-right': '5px',
          'margin-left': '8px',
          'height': '24px',
          ' p': {
            'margin-top': '4px',
          },
        },
      }),

      // member role list
      Components.list('roles', {

      }),
    ],
  }).then(function (_single) {

    // vars
    var _activation = _single.get('activation');
    var _roles = _single.get('roles');

    // single
    _single.load = function () {
      // loads a member id from the api buffer
      var _member = api.active.Member;
      return _.all([
        _single.get('name').update({value: `${_member.first_name} ${_member.last_name}`}),
        _single.get('email').update({value: _member.email}),
        _activation.load({activated: _member.is_activated}),
        _roles.data.load.main(),
      ]);
    }
    _single.setStates([
      ui._state('members', {
        children: [
          ui._state('single', {
            fn: function (_this) {
              return _this.removeClass('hidden');
            },
          }),
          ui._state('new', {
            fn: function (_this) {
              return _this.setClasses('hidden');
            },
          }),
        ],
      }),
    ]);

    // activation
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

    // roles
    _roles.get('search').setStyle({'display': 'none'});
    _roles.setTargets([
      _roles._target('roles', {
        exclusive: false,
        _source: function (args) {
          args = (args || {});
          var _target = this;
          return api.models.Role.objects.filter({force: args.force, data: (args.data || _target.data())});
        },
        data: function (args) {
          args = (args || {});
          return [
            {
              key: 'member__id',
              value: api.active.Member._id,
              q: 'AND',
            },
            {
              key: 'model__club__id',
              value: api.active.Club._id,
              q: 'AND',
            }
          ];
        },
        normalise: function (_instance) {
          return _.all([
            _instance.related('model'),
            _instance.related('member'),
          ]).then(function (results) {
            var [_model, _member] = results;
            return _model.related('club').then(function (_club) {
              return {
                _id: _instance._id,
                member: _member._id,
                main: _model.verbose_name,
                club: _club.name,
              }
            });
          });
        },
        unit: function (name, args) {
          return ui._component(name, {
            style: {

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
                title: _datum.normalised.main,
                value: _datum.normalised.club,
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
    _roles.data.display.filter.condition = function (_datum) { // override
      return _.p(function () {
        _datum.accepted = _datum.normalised.member === api.active.Member._id;
      });
    }

    return _single;
  })
}
