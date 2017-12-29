var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
      '.hidden': {
        'display': 'none',
      },
    },
    children: [
      Test.interfaces.centred({
        style: {

        },
        children: [
          Components.list('list', {
            tramline: true,

          }),
        ],
      }),
    ],
  }).then(function (_test) {

    var _container = _test.get('centred.container');
    var _list = _container.get('list');

    _list.setTargets([
      _list._target('clubs', {
        exclusive: true,
        source: function (force) {
          var _target = this;
          return api.models.Club.objects.filter({force: force, data: _target.data()});
        },
        data: function () {
          var _target = this;
          var _main = _list.metadata.query.buffer.main;

          return [
            {
              server: 'name__icontains',
              value: _main,
              model: function (_instance) {
                return _.p(_instance.name.toLowerCase().contains(_main));
              },
            }
          ]
        },
        normalise: function (_instance) {
          return _.p({_id: _instance._id, main: _instance.name});
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
                title: _datum.item.name,
                value: _datum.item._id,
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

    _test.setStates([
      ui._state('main', {
        fn: {
          after: function () {
            return _list.data.load.main();
          },
        },
      }),
    ]);

    return _test;
  });
}
