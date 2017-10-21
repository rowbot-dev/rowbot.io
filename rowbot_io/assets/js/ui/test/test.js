Test.application({
  interface: {
    size: 50,
    margin: 10,
    corner: 5,
  },
}).then (function (app) {
  // render
  return app.render('hook');
}).then(function () {
  return _.all([

  ]).then(function () {
    // return ui.state();
  });
}).catch(function (error) {
  console.log(error);
});
