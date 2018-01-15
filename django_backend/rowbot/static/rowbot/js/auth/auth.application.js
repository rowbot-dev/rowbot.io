var Auth = (Auth || {});
Auth.application = function () {
  return ui._component('auth', {
    style: {
      'height': '100%',
      'width': '100%',
      'top': '0%',
      'top': '0%',
      ' .interface': {
        'position': 'absolute',
        'height': '100%',
        'width': '100%',
        'top': '0%',
        'top': '0%',
      },
    },
    children: [
      Auth.interfaces.activation(),
      Auth.interfaces.login(),
      Auth.interfaces.referral(),
      Auth.interfaces.signup(),
    ],
  });
}
