
var Test = (Test || {});
Test.components = (Test.components || {});
Test.components.panel = function (name, args) {
  return ui._component(name, {
    style: _.merge({
      'height': '100%',
      'width': '100%',
      'overflow-y': 'hidden',
    }, args.style),
    children: [
      ui._component('container', {
        style: {
          'width': 'calc(100% + 20px)',
          'height': '100%',
          'border': '1px solid black',
          'overflow-y': 'scroll',
        },
        children: [
          ui._component('content', {
            style: _.merge({
              'width': 'calc(100% - 35px)',
              'height': 'auto',
              'border': '1px solid black',
              'padding': '10px',
            }, args.contentStyle),
            children: args.children,
          }),
        ],
      }),
      ui._component('scroll', {
        style: {
          'position': 'absolute',
          'height': '100%',
          'width': '15px',
          'right': '0px',
          'top': '0px',
          'border': '1px solid black',
        },
        children: [
          ui._component('bar', {
            style: {
              'position': 'relative',
              'height': '100px',
              'width': '100%',
              'border': '1px solid black',
              'top': '0%',
            },
          }),
        ],
      }),
    ],
  }).then(function (_panel) {

    var raf = window.requestAnimationFrame || window.setImmediate || function(c) { return setTimeout(c, 0); };
    var _container = _panel.get('container');
    var _scroll = _panel.get('scroll');
    var _bar = _scroll.get('bar');

    _panel.move = function (event) {
      var _containerElement = _container.element();
      _container.scrollRatio = _containerElement.clientHeight / _containerElement.scrollHeight;

      raf(function () {
        // Hide scrollbar if no scrolling is possible
        if (_container.scrollRatio >= 1) {
          return _container.setClasses(['hidden']);
        } else {
          return _.all([
            _container.removeClass('hidden'),
            _bar.setStyle({
              'height': `${Math.max(_container.scrollRatio * 100, 10)}%`,
              'top': `${(_containerElement.scrollTop / _containerElement.clientHeight) * 50}%`,
            }),
          ]);
        }
      });
    }
    _panel.drag = function (event) {
      _barElement = _bar.element();
      var delta = event.pageY - _bar.pageY;
      _bar.pageY = event.pageY;

      raf(function() {
        _container.scrollTop += delta / _container.scrollRatio;
      });
    }
    _panel.stop = function () {
      return _.all([
        _scroll.removeClass('active'),
        _.p(function () {
          document.removeEventListener('mousemove', _panel.drag);
          document.removeEventListener('mouseup', _panel.stop);
        }),
      ]);
    }

    _container.setBindings({
      'scroll': function (_this, event) {
        return _panel.move(event);
      },
      'mouseenter': function (_this, event) {
        return _panel.move(event);
      }
    });
    _bar.setBindings({
      'mousedown': function (_this, event) {
        _barElement = _this.element();
        _this.pageY = event.pageY;
        document.addEventListener('mousemove', _panel.drag);
        document.addEventListener('mouseup', _panel.stop);
        return false;
      },
    });

    return _panel;
  });
}
