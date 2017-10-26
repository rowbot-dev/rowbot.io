var Test = (Test || {});
Test.interfaces = (Test.interfaces || {});
Test.interfaces.centred = function (args) {
  return ui._component('centred', {
    style: {

    },
    children: [
      ui._component('container', {
        style: {

        },
        children: args.children,
      }),
    ],
  }).then(function (_centred) {
    return _centred;
  });
}
