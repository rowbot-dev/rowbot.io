var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
    },
    children: [
      Test.interfaces.centred({
        style: {

        },
        children: [
          Test.components.list('list', {

          }),
        ],
      }),
    ],
  }).then(function (_test) {

    var _container = _test.get('centred.container');
    var _list = _container.get('list');

    _list.setTargets([
      _list._target('members', {
        source: function (force) {
          var _target = this;
          return ui.api.models.Member.objects.all().then(function (items) {
            return items;
          });
        },
        unit: function (name, args) {
          return ui._component(`unit-${name}`, {
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
              return _unit.get('text').update({
                title: _datum.item.username,
                value: _datum.item.email,
              }).then(function () {
                return _unit;
              });
            }
            _unit.hide = function () {
              _unit.isHidden = true;
              return _unit;
            }
            _unit.show = function () {
              _unit.isHidden = false;
              return _unit;
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
            return _list.data.load();
          },
        },
      }),
    ]);

    return _test;
  });
}
