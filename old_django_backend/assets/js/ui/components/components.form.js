
var Components = (Components || {});
Components.form = function (name, args) {
  return ui._component(name, _.merge({

  }, args)).then(function (_form) {

    _form.submit = (args.submit || 'submit');
    _form.send = function (results) {
      return _.p(results);
    }
    _form.error = function (messages) {

    },
    _form.export = function () {
      // for each child, call export function and return
      return _.pmap(_form._.children.rendered, function (name, child) {
        if (child.name !== _form.submit && child.export) {
          return child.export();
        }
      }).then(function (results) {

        // filter for undefined elements
        results = results.filter(function (result) {
          return result !== undefined;
        });

        // reduce for validated data
        var validated = results.every(function (result) {
          return result.validated;
        });

        // only continue if validated
        if (validated) {
          return _form.send(results.reduce(function (whole, part) {
            whole[part.name] = part.value;
            return whole;
          }, {}));
        }
      });
    }

    // bind submit button
    _form.get(_form.submit).click = function (event) {
      return _form.export();
    }

    // bind enter key in inputs to submit
    _form._.children.buffer.forEach(function (_child) {
      let _content = _child.get('content');
      if (_content !== undefined) {
        _child.keypress = function (value, event) {
          if (event.which === 13) {
            return _form.export();
          }
        }
      }
    });

    return _form;
  });
}
