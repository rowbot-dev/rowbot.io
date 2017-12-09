App.application().then(function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    return ui.api.setup().then(function () {
      return ui.api.getToken();
    });
  });
}).catch(function (error) {
  console.log(error);
});
