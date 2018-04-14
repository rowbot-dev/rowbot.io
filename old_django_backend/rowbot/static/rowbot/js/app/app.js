App.application().then(function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    return api.setup();
  }).then(function () {
    return ui.states.call('load');
  });
}).catch(function (error) {
  console.log(error);
});
