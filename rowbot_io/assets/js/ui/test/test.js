Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function () {
  return _.all([
    ui.api.setup().then(function () {
      return ui.api.getToken('npiano', 'mach1');
    }),
  ]).then(function () {

  });
}).catch(function (error) {
  console.log(error);
});
