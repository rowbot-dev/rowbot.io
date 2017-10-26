var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    style: {

    },
    children: [
      Test.interfaces.centred({
        children: [
          Test.components.input('input', {
            
          }),
        ],
      }),
    ],
  }).then(function (_test) {
    return _test;
  });
}
