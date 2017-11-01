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
          
        ],
      }),
    ],
  }).then(function (_test) {
    return _test;
  });
}
