Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function () {
  return _.all([
    ui.api.setup().then(function () {
      return ui.api.getToken('npiano', 'mach');
    }),
  ]).then(function () {
    var Member = ui.api.models.Member;
    return Member.objects.all({force: true}).then(function (result) {
      _.l(result);
      return Member.objects.all();
    }).then(function (result) {
      _.l(result);
    });
    // return ui.states.call('main.new');
  });
}).catch(function (error) {
  console.log(error);
});
