
/*

List component
1. Search/filter/sort bar
2. Results list
3. Filter list
4. Pagination bar
5.

*/

var Components = (Components || {});
Components.list = function (name, args) {
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
        tramline: args.tramline,
        style: {
          'height': '300px',
          'div.hidden': {
            'display': 'none',
          },
        },
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
    var _input = _list.get('search.input');
    var _wrapper = _list.get('list.container.content.wrapper');

    /*

    Input bindings

    */
    _input.input = function (value, event) {
      return _.p(function () {
        _list.metadata.query.buffer.main = value;
        return _list.data.load();
      });
    }

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
          var _query = this;
          var _target = _datum.target;
          var _normalised = _datum.normalised;
          return _.p(function () {
            return _.map(_normalised, function (_key, _value) {
              let results = {};
              let exclusive = (_list.metadata.exclusive || _target.exclusive);
              if (_key in _query.buffer) {
                let _partial = _query.buffer[_key];
                results[_key] = _value.score(_partial, exclusive);
              } else {
                results[_key] = exclusive ? 0 : 1;
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
          return _._all(_data.map(function (_item, i) {
            return function () {
              return _list.data.display.main({target: _target, item: _item, normalised: _target.normalise(_item)});
            }
          }));
        }).then(function () {
          return _target.force().then(function (_data) {
            return _._all(_data.map(function (_item, i) {
              return function () {
                return _list.data.display.main({target: _target, item: _item, normalised: _target.normalise(_item)});
              }
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
      _target.normalise = function (_item) {
        return _item;
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
      return ui._component(`${name}`, _.merge({
        style: {
          'width': '100%',
          'height': 'auto',
        },
      }, args)).then(function (_block) {

        _block.isReleased = true;
        _block.types = {};
        _block.unit = function (_datum) {
          // get or create unit
          _block.datum = _datum;
          _block.isReleased = false;
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
            return _.all(_block.children().map(function (_rest) {
              if (_rest.name !== _unit.name) {
                return _rest.hide();
              }
            })).then(function () {
              if (!_block.isReleased) {
                return _unit.show();
              } else {
                return _unit;
              }
            });
          });
        }
        _block.release = function () {
          // hide all units except the active one
          _block.isReleased = true;
          // _.l(9, 'block.release', _block.name);
          return _.all(_block.children().map(function (_unit) {
            return _unit.hide();
          }));
        }

        return _block;
      });
    }

    /*

    Data contains a series of methods and buffers to handle intermediate processing and storage for incoming data.

    */
    window._list = _list;
    _list.data = {
      load: function () {
        // for each target
        // _list.data.storage.sorted = [];
        return _list.data.storage.garbage().then(function () {
          // _.l(0, _list.data.storage.sorted);
          return _._all(_list.targets.map(function (_target) {
            return _target.load;
          }));
        });
      },
      storage: {
        buffer: {}, // needed as an intermediate for sorting
        sorted: [], // a list of ids present in the storage object, sorted by the current method
        add: function (_datum) { // basic implementation of a binary search function
          var _storage = this;
          return _.p(function () {
            // add to buffer
            _datum.sorted = false;
            _storage.buffer[_datum.item._id] = _datum;

            // run sorting
            var direction, previous;
            var searchLength = Math.floor(_storage.sorted.length / 2); // halving distance moved each time from centre
            var index = searchLength; // start index at centre
            if (!_storage.sorted.contains(_datum.item._id)) {
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
                if (direction === 1 && previous === -1 || direction === 0) {
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
              _datum.sorted = true;
            }
            // _.l(6, 'storage.add', _datum.item.name, _datum.index);
          });
        },
        compare: function (_d1, _d2) { // override
          if (_d1.scores.main > _d2.scores.main) {
            return -1;
          } else if (_d1.scores.main === _d2.scores.main) {
            if (_d1.normalised.main < _d2.normalised.main) {
              return -1;
            } else if (_d1.normalised.main === _d2.normalised.main) {
              return 0;
            } else {
              return 1;
            }
          } else {
            return 1;
          }
        },
        garbage: function () {
          var _storage = this;
          return _._all(_wrapper.children().map(function (_child, i) {
            // for each child, if released, remove from storage list
            return function () {
              return _.p(function () {
                if (_child.isReleased) {
                  let index = _storage.sorted.indexOf(_child.datum.item._id);
                  _storage.sorted.splice(index, 1);
                }
              });
            }
          }));
        },
      },
      display: {
        main: function (_datum) {
          var _display = _list.data.display;
          var _storage = _list.data.storage;

          // run datum through filter
          _datum.accepted = false;
          // _.l(2, 'display.main', _datum.item._id);
          return _display.filter.main(_datum).then(function () {
            // _.l(7, 'display.main', _datum.item._id, _datum.sorted, _datum.accepted);
            if (_datum.sorted && _datum.accepted) {
              return _display.render.main(_datum);
            } else if (!_datum.sorted && !_datum.accepted) {
              return _display.remove(_datum);
            }
          });
        },
        filter: {
          main: function (_datum) {
            // calls common filter method based on metadata
            var _filter = _list.data.display.filter;

            // get query score
            // _.l(3, 'filter.main', _datum.item._id);
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
              // _.l(4, 'filter.score', _datum.item._id, _scores);
              _datum.scores = _scores;
            });
          },
          condition: function (_datum) { // override
            return _.p(function () {
              _datum.accepted = _datum.scores.main > 0;
              // _.l(4, 'filter.condition', _datum.item._id, _datum.accepted);
            });
          },
          sort: function (_datum) { // override
            return _.p(function () {
              // modify scores here based on current sorting order or other condition
              // _.l(5, 'filter.sort', _datum.item._id, _datum.accepted);
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
            // _.l(8, 'render.main', _datum.item._id);
            return _.p(function () {
              if (_datum.sorted) {
                return _render.block(_datum).then(function (_block) {
                  return _block.unit(_datum);
                });
              }
            });
          },
          block: function (_datum) {
            var _render = this;
            // get or create unit
            var _current = _wrapper.get(_render.buffer[_datum.index]);
            if (_current && _current.isReleased) {
              return _.p(_current);
            }

            var _before = _wrapper.get(_render.buffer[_datum.index+1]);

            var _blockName = _.id();
            _render.buffer.splice(_datum.index, 0, _blockName);
            return _list.block(_blockName, {before: (_before || {}).name}).then(function (_block) {
              return _wrapper.setChildren(_block);
            });
          },
        },
        remove: function (_datum) {
          return _.p(function () {
            var index = _list.data.storage.sorted.indexOf(_datum.item._id);
            if (index !== -1) {
              var _release = _wrapper.get(_list.data.display.render.buffer[index]);
              // _.l(8, 'remove', _datum.item._id, _list.data.storage.sorted.length, index, _release.name);
              return _release.release();
            }
          });
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
