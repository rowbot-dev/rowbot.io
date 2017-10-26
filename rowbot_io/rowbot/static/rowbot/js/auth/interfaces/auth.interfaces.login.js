var Auth = (Auth || {});
Auth.interfaces = (Auth.interfaces || {});
Auth.interfaces.login = function () {
  return ui._component('login', {
    children: [
      ui._component('container', {
        children: [
          ui._component('text', {
            children: [

            ],
          }),
          ui._component('form', {
            children: [

            ],
          }),
        ],
      }),
    ],
  }).then(function (_login) {
    return _login;
  });
}
