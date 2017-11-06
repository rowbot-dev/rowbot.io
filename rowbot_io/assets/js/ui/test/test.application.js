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
          return ui.api.models.Member.objects.all(force);
          // return _.p([
          //   {
          //     _id: '1',
          //     name: 'Harry',
          //   },
          //   {
          //     _id: '2',
          //     name: 'Harrys',
          //   },
          //   {
          //     _id: '3',
          //     name: 'Har',
          //   },
          // ]);
        },
        unit: function () {

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
