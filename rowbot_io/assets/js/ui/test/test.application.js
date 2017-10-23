var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    after: undefined,
    root: undefined,
    children: [
      ui._component('main', {
        style: {
          'height': '100px',
          'width': '100px',
          'border': '1px solid black',
          'div': {
            'height': '100%',
          },
        },
        states: [
          ui._state('main', {
            children: [
              ui._state('new', {
                children: [

                ],
              }),
            ],
          }),
        ],
        children: [
          ui._component('list', {
            style: {
              'height': '90%',
            },
            bindings: {
              'mouseover': function (_this, event) {
                _.l(_this.id, event);
              },
            },
            children: [
              ui._component('new', {
                style: {
                  'height': '80%',
                },
              }),
            ],
          }),
          ui._component('3', {

          }),
          ui._component('4', {
            before: '3',
          }),
        ],
      }),
      ui._component('2', {

      }),
    ],
  }).then(function (_test) {
    return _test;
  });
}
