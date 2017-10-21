ui.App('hook', [
  Auth.application({
    interface: {
      size: 50,
      margin: 10,
      corner: 5,
    },
  }),
]).then (function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    return ui.state('login');
  });
}).catch(function (error) {
  console.log(error);
});
