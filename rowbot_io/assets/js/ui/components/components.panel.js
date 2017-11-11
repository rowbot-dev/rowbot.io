
/*

The panel component wraps content in two containers. An outer one of fixed size that also houses a scroll bar and an inner one of scaling size.
The inner holds the content and scrolls within the outer container.

*/

var Components = (Components || {});
Components.panel = function (name, args) {
  return ui._component(name, {
    style: _.merge({
      'width': '100%',
      'overflow-y': 'hidden',
      'position': 'relative',
    }, args.style),
    children: [
      ui._component('container', {
        style: {
          'width': 'calc(100% + 20px)',
          'height': 'auto',
          'overflow-y': 'scroll',
        },
        children: [
          ui._component('content', {
            style: _.merge({
              'width': `calc(100% - ${args.tramline ? 35 : 20}px)`,
              'height': 'auto',
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
        },
        children: [
          ui._component('bar', {
            style: {
              'position': 'relative',
              'height': '10%',
              'width': '15px',
              'border': '1px solid black',
              'top': '0%',
              'opacity': '0',
            },
          }),
        ],
      }),
    ],
  }).then(function (_panel) {

    var raf = window.requestAnimationFrame || window.setImmediate || function(c) { return setTimeout(c, 0); };
    var _container = _panel.get('container');
    var _content = _container.get('content');
    var _scroll = _panel.get('scroll');
    var _bar = _scroll.get('bar');

    _panel.isActive = false;
    _panel.isDragging = false;
    _panel.move = function (event) {
      var _barElement = _bar.element();
      var _containerElement = _container.element();
      var _contentElement = _content.element();
      _container.scrollRatio = _containerElement.clientHeight / _contentElement.clientHeight;

      raf(function () {
        // Hide scrollbar if no scrolling is possible
        if (_container.scrollRatio >= 1) {
          return _container.setClasses(['hidden']);
        } else {
          var height = Math.max(_container.scrollRatio * 100, 10);
          var top = (_containerElement.scrollTop / (_contentElement.clientHeight - _containerElement.clientHeight)) * (100 - height);

          $(_barElement).css({
            'height': `${height}%`,
            'top': `${top}%`,
          }, {queue: false});
          if (!_panel.isActive) {
            _panel.isActive = true;
            $(_barElement).animate({
              'opacity': '1',
            }, {duration: 300, queue: false});
          }
        }
      });
    }
    _panel.drag = function (event) {
      _panel.isActive = true;
      _panel.isDragging = true;
      var _containerElement = _container.element();
      var _barElement = _bar.element();
      var delta = event.pageY - _bar.pageY;
      _bar.pageY = event.pageY;

      raf(function() {
        _containerElement.scrollTop += delta / _container.scrollRatio;
      });
      event.preventDefault();
    }
    _panel.stop = function () {
      _panel.isActive = false;
      _panel.isDragging = false;
      var _barElement = _bar.element();
      return _.all([
        _.p(function () {
          setTimeout(function () {
            $(_barElement).animate({
              'opacity': '0',
            }, {duration: 300, queue: false});
          }, 300);
        }),
        _.p(function () {
          document.removeEventListener('mousemove', _panel.drag);
          document.removeEventListener('mouseup', _panel.stop);
        }),
      ]);
    }

    _panel.setBindings({
      'mouseleave': function (_this, event) {
        if (!_panel.isDragging) {
          return _panel.stop(event);
        }
      },
    });
    _container.setBindings({
      'scroll': function (_this, event) {
        return _panel.move(event);
      },
    });
    _bar.setBindings({
      'mousedown': function (_this, event) {
        _barElement = _this.element();
        _this.pageY = event.pageY;
        document.addEventListener('mousemove', _panel.drag);
        document.addEventListener('mouseup', _panel.stop);
        event.preventDefault();
      },
    });

    return _panel;
  });
}
