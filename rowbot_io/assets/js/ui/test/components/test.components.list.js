
/*

List component
1. Search/filter/sort bar
2. Results list
3. Filter list
4. Pagination bar
5.

*/

var Test = (Test || {});
Test.components = (Test.components || {});
Test.components.list = function (name, args) {
  return ui._component(name, {
    children: [
      ui._component('search', {
        children: [
          // toggle filter
          Components.button('filter', {

          }),

          // search field
          Components.input('input', {

          }),
        ],
      }),
      ui._component('pagination', {
        children: [

          // previous set
          Components.button('back', {

          }),

          // XX of XXX
          ui._component('count', {

          }),

          // next set (load more)
          Components.button('forward', {

          }),
        ],
      }),
      Components.panel('list', {
        children: [

          // contains list items
          ui._component('wrapper', {

          }),

          // "load more" and spinner
          ui._component('load', {

          }),
        ],
      }),
      Components.panel('filter', {
        style: {
          'top': '0px',
          'position': 'absolute',
        },
        children: [

        ],
      }),
    ],
  }).then(function (_list) {

    // component variables
    var _wrapper = _list.get('list.container.content.wrapper');

    /*

    Metadata includes boolean statements about the list's condition as well as values that affect display or processing.

    */
    _list.metadata = {
      limit: 10,
      exclusive: false,
      query: {
        buffer: {},
        score: function (_datum) {
          // normalised is an object with categories as keys and corresponding values.
          // for each category, check against query.buffer
          var query = _list.metadata.query;
          var _target = _datum.target;
          var _normalised = _datum.normalised;
          return _.p(function () {
            return _.map(_normalised, function (key, value) {
              var results = {};
              if (key in query.buffer) {
                let _query = query.buffer[key];
                results[key] = value.score(_query);
              } else {
                results[key] = (_list.metadata.exclusive || _target.exclusive) ? 0 : 1;
              }
              return results;
            }).reduce(function (whole, part) {
              return _.merge(whole, part);
            }, {});
          });
        },
      },
      filter: {},
    }

    /*

    Target object stores and processes data origins

    */
    _list.targets = [];
    _list.Target = function (name) {
      var _target = this;
      _target.name = name;
      _target.exclusive = false;

      // methods
      _target.update = function (args) {
        return _.p(function () {
          args = (args || {});
          _target.source = args.source;
          _target.force = (args.force || _target.force);
          _target.normalise = (args.normalise || _target.normalise);
          _target.exclusive = (args.exclusive || _target.exclusive);
          _target.unit = (args.unit || _target.unit);
          return _target;
        });
      }
      _target.load = function () {

        // from here, each individual item makes its way down into the display function, accruing
        // modifications as it goes. It will eventually have a normalised version,
        return _target.source().then(function (_data) {
          return _._all(_data.map(function (_unit) {
            return _list.data.display.main({target: _target, item: _unit, normalised: _target.normalise(_unit)});
          }));
        }).then(function () {
          return _target.force().then(function (_data) {
            return _._all(_data.map(function (_unit) {
              return _list.data.display.main({target: _target, item: _unit, normalised: _target.normalise(_unit)});
            }));
          });
        });
      }
      _target.delay = 100;
      _target.force = function () {
        var _query = '';
        return new Promise(function (resolve, reject) {
          setTimeout(function () {
            if (true) {
              _target.source(true).then(function (_data) {
                resolve(_data);
              });
            }
          }, _target.delay);
        });
      }

      // normalised objects should contain a list of properties to be compared with the queries
      _target.normalise = function (_unit) {
        return _unit;
      }
      _target.unit = function (name, args) {
        return ui._component(name, {

        }).then(function (_block) {
          return _block;
        });
      }
    }
    _list._target = function (name, args) {
      return new _list.Target(name).update(args);
    }
    _list.setTargets = function (targets) {
      return _._all(targets.map(function (target) {
        return _.p(target).then(function (_target) {
          _list.targets.push(_target);
        });
      }));
    }

    /*

    Block object: holds units of different types

    */
    _list.block = function (name, args) {
      return ui._component(`block-${name}`, {
        style: {
          'width': '100%',
          'height': 'auto',
        },
      }).then(function (_block) {

        _block.types = {};
        _block.unit = function (_datum) {
          // get or create unit
          var _unit = _block.get(_block.types[_datum.target.name]);
          return _.p(function () {
            if (_unit) {
              return _unit.update(_datum);
            } else {
              var _unitName = _.id();
              _block.types[_datum.target.name] = _unitName;
              return _datum.target.unit(_unitName).then(function (_unit) {
                return _block.setChildren(_unit);
              }).then(function (_unit) {
                return _unit.update(_datum);
              });
            }
          }).then(function (_unit) {
            // hide all units except the active one
            return _.all(_block._.children.rendered.map(function (_rest) {
              if (_rest.name !== _unit.name) {
                return _rest.hide();
              }
            })).then(function () {
              return _unit.show();
            });
          });
        }

        return _block;
      });
    }

    /*

    Data contains a series of methods and buffers to handle intermediate processing and storage for incoming data.

    */
    window._list = _list;
    _list.data = {
      storage: {
        buffer: {}, // needed as an intermediate for sorting
        sorted: [], // a list of ids present in the storage object, sorted by the current method
        add: function (_datum) { // basic implementation of a binary search function
          var _storage = this;

          // add to buffer
          _storage.buffer[_datum.item._id] = _datum;

          // run sorting
          if (!_storage.sorted.contains(_datum.item._id)) {
            var direction, previous;
            var searchLength = Math.floor(_storage.sorted.length / 2); // halving distance moved each time from centre
            var index = searchLength; // start index at centre
            while (true) {

              // most likely, the array length is zero, but could be placed at end.
              if (index === _storage.sorted.length) {
                break;
              }

              // calculate new direction
              previous = direction;
              direction = _storage.compare(_datum, _storage.buffer[_storage.sorted[index]]);

              // calculate new search length and get new index
              searchLength = Math.max(Math.floor(searchLength / 2), 1); // halve
              index += direction * searchLength; // move up or down

              // if flip-flop, leave high because of how indexes work
              if (direction === 1 && previous === -1) {
                break;
              }

              // must go around if zero to compare with zero element
              if (index === -1) {
                index = 0;
                break;
              }
            }

            // add to sorted
            _storage.sorted.splice(index, 0, _datum.item._id);
            _datum.index = index;
          } else {
            _datum.accepted = false;
          }
        },
        remove: function (_datum) {

        },
        compare: function (_d1, _d2) { // override
          if (_d1.scores.name > _d2.scores.name) {
            return -1;
          } else if (_d1.scores.name === _d2.scores.name) {
            return 0;
          } else {
            return 1;
          }
        },
      },
      load: function () {
        // for each target
        return _._all(_list.targets.map(function (_target) {
          return _target.load;
        }));
      },
      display: {
        main: function (_datum) {
          var _display = _list.data.display;
          var _storage = _list.data.storage;

          // run datum through filter
          _datum.accepted = false;
          return _display.filter.main(_datum).then(function () {
            if (_datum.accepted) {
              return _display.render.main(_datum);
            } else {
              return _display.remove(_datum);
            }
          });
        },
        filter: {
          main: function (_datum) {
            // calls common filter method based on metadata
            var _filter = _list.data.display.filter;

            // get query score
            return _filter.score(_datum).then(function () {
              return _filter.condition(_datum);
            }).then(function () {
              return _.p(function () {
                if (_datum.accepted) {
                  return _filter.sort(_datum);
                }
              });
            });
          },

          // https://github.com/atom/fuzzaldrin
          // fuzzy sorting
          score: function (_datum) {
            return _list.metadata.query.score(_datum).then(function (_scores) {
              return _.p(function () {
                _datum.scores = _scores;
              });
            });
          },
          condition: function (_datum) { // override
            return _.p(function () {
              _datum.accepted = true;
            });
          },
          sort: function (_datum) { // override
            return _.p(function () {
              // modify scores here based on current sorting order or other condition

              if (_datum.accepted) {
                return _list.data.storage.add(_datum);
              }
            });
          },
        },
        render: {
          buffer: [],
          main: function (_datum) {
            var _render = this;
            // 1. does a unit exist with this index?
            // 2. is the unit at this index hidden?
            // 3. (create and update) or (update and show)
            return _render.block(_datum).then(function (_block) {
              return _block.unit(_datum);
            });
          },
          block: function (_datum) {
            var _render = this;
            // get or create unit
            var _current = _wrapper.get(_render.buffer[_datum.index]);
            if (_current && !_current.isHidden) {
              return _current;
            }

            var _blockName = _.id();
            _render.buffer.splice(_datum.index, 0, _blockName);
            return _list.block(_blockName).then(function (_block) {
              return _wrapper.setChildren(_block);
            });
          },
        },
        remove: function (_unit) {
          return _.p();
        },
      },
    }

    /*

    Control contains methods and flags for manipulating the list.

    */
    _list.control = {

    }

    /*

    States are methods for changing the layout of the list to display different views

    */
    _list.states = {
      showFilter: function () {
        // hide the list to show the filter panel
      },
      showDisplay: function () {
        // hide the filter panel to show the list
      },
      showSingleDisplay: function () {
        // with the filter panel showing, show the list displaying only a maximum of two items
      }
    }

    // override component methods


    return _list;
  });
}
