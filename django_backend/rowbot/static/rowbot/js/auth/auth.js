Auth.application().then(function (app) {
  // render
  return app.render();
}).then(function () {
  return _.all([

  ]).then(function () {
    // return ui.states.call('login');
  });
}).catch(function (error) {
  console.log(error);
});
