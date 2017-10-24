var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    style: {
      'div.main': {
        'background-color': '#cc0',
      },
      'div.new': {
        // 'background-color': '#cc8',
      },
    },
    children: [
      ui._component('main', {
        style: {
          'position': 'relative',
          'float': 'left',
          'height': '100px',
          'width': '100px',
          'border': '1px solid black',
          'div': {
            'height': '100%',
          },
        },
        states: [
          ui._state('main', {
            style: {
              'left': '100px',
            },
            classes: ['main'],
            fn: {
              before: function (_this) {
                _.l('0');
                return _.p();
              },
            },
            children: [
              ui._state('new', {
                style: {
                  'left': '100px',
                  'top': '100px',
                },
                classes: ['new'],
                fn: {
                  // before: function (_this) {
                  //   _.l('1');
                  //   return _.p();
                  // },
                  after: function (_this) {
                    _.l('2');
                    return _.p();
                  },
                },
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
              'mousemove': function (_this, event) {
                _.l(_this, event.target.id);
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
