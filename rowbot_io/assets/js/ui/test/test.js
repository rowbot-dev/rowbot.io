Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function () {
  return _.all([

  ]).then(function () {
    // return ui.states.call('main.new');
  });
}).catch(function (error) {
  console.log(error);
});
