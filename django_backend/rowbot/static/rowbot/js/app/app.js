App.application().then(function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    return api.setup();
  }).then(function () {
    return _.all([
      ui.states.call('clubs'),
      // api.models.EventModel.objects.all(),
      // api.models.Event.objects.all(),
      api.models.Club.objects.all(),
      api.models.Role.objects.all(),
      api.models.RoleModel.objects.all(),
      api.models.Member.objects.all(),
    ]);
  });
}).catch(function (error) {
  console.log(error);
});
