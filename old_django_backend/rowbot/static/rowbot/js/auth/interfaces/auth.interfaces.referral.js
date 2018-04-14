var Auth = (Auth || {});
Auth.interfaces = (Auth.interfaces || {});
Auth.interfaces.referral = function () {
  return ui._component('referral', {

  }).then(function (_referral) {
    return _referral;
  });
}
