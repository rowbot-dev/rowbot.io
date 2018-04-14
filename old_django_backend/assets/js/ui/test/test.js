Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function (app) {
  return _.all([
    api.setup().then(function () {
      api.getToken();
    }),
  ]).then(function () {
    return ui.states.call('main');

    // TODO: use beforeunload for actions
    // window.addEventListener("beforeunload", function (e) {
    //   api.setup();
    // });

  });
}).catch(function (error) {
  console.log(error);
});
