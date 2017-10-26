Test.application().then (function (app) {
  // render
  return app.render('hook');
}).then(function (app) {
  return _.all([
    
  ]).then(function () {

    // TODO: use beforeunload for actions
    // window.addEventListener("beforeunload", function (e) {
    //   ui.api.setup();
    // });

  });
}).catch(function (error) {
  console.log(error);
});
