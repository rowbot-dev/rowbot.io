var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    style: {

    },
    children: [
      Test.interfaces.centred({
        style: {
          
        },
        children: [
          Test.components.panel('panel', {

          }),
        ],
      }),
    ],
  }).then(function (_test) {
    return _test;
  });
}
