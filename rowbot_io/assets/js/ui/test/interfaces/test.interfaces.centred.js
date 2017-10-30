var Test = (Test || {});
Test.interfaces = (Test.interfaces || {});
Test.interfaces.centred = function (args) {
  return ui._component('centred', {
    classes: ['centred'],
    style: {
      'height': '400px',
      'width': '400px',
    },
    children: [
      ui._component('container', {
        style: {
          'height': '400px',
          'width': '400px',
        },
        children: args.children,
      }),
    ],
  }).then(function (_centred) {
    return _centred;
  });
}
