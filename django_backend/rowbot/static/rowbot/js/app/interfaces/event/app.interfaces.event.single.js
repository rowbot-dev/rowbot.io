
var App = (App || {});
App.interfaces = (App.interfaces || {});
App.interfaces.event = (App.interfaces.event || {});
App.interfaces.event.single = function () {
  return ui._component('single', {
    classes: ['hidden', 'panel'],
    style: {
      'position': 'relative',
      'padding': '20px',
      'left': '-100%',
    },
    children: [
      // title
      Components.text('title'),
    ],
  }).then(function (_single) {

    // vars

    return _single;
  });
}
