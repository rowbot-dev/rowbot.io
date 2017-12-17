App.application().then(function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    return api.setup();
  }).then(function () {
    return _.all([
      api.models.EventModel.objects.all(),
      api.models.Event.objects.all(),
      api.models.Role.objects.all(),
    ]);
  });
}).catch(function (error) {
  console.log(error);
});
