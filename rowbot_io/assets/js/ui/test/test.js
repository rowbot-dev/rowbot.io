Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function () {
  return _.all([
    ui.api.setup().then(function () {
      return ui.api.getToken('npiano', 'mach1');
    }),
  ]).then(function () {
    var Member = ui.api.models.Member;
    return Member.objects.filter({force: true}).then(function (result) {
      _.l(result);
      return Member.objects.get('2464f22f4fbb42f38a1f2bf7ce81c6c5');
    }).then(function (_member) {
      _.l(_member);
      return _member.get();
      // return _member.method('change_password', 'POST', {password: 'mach1'}).then(function (response) {
      //   _.l(response);
      // });
    });
    // return ui.states.call('main.new');
  });
}).catch(function (error) {
  console.log(error);
});
