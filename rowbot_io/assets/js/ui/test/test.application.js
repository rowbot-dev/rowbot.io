var Test = (Test || {});
Test.application = function (args) {
  return ui._component('test', {
    children: [
      ui._component('1', {

      }),
      ui._component('2', {

      }),
    ],
  }).then(function (_test) {
    return _test;
  });
}
//
// var AuthApplication = function (args) {
//   return UI.createComponent('auth', {
//     name: 'auth',
//     template: UI.template('div', 'ie'),
//     appearance: {
//       style: {
//         'height': '100%',
//       },
//     },
//     children: [
//       // header
//
//
//       // login form
//       AuthInterfaces.login(),
//
//       // signup form
//       AuthInterfaces.signup(),
//
//       // activation form
//       AuthInterfaces.activation(),
//     ],
//   }).then(function (base) {
//
//     // complete promises
//     return Promise.all([
//
//     ]).then(function () {
//       return base;
//     });
//   });
// }
