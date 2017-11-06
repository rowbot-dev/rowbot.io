
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
        children: [

        ],
      }),
    ],
  }).then(function (_list) {

    // component variables


    /*

    Metadata includes boolean statements about the list's condition as well as values that affect display or processing.

    */
    _list.metadata = {
      limit: 10,
      query: {
        buffer: {
          id: '2',
          name: 'Har',
        },
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
                results[key] = 1; // can be zero for exclusive list
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

      // methods
      _target.update = function (args) {
        return _.p(function () {
          args = (args || {});
          _target.source = args.source;
          _target.force = (args.force || _target.force);
          _target.normalise = (args.normalise || _target.normalise);
          return _target;
        });
      }
      _target.load = function () {

        // from here, each individual item makes its way down into the display function, accruing
        // modifications as it goes. It will eventually have a normalised version,
        return _.all([
          _target.source().then(function (_data) {
            return _._all(_data.map(function (_item) {
              return _list.data.display.main({target: _target, item: _item, normalised: _target.normalise(_item)});
            }));
          }),
          _target.force().then(function (_data) {
            return _._all(_data.map(function (_item) {
              return _list.data.display.main({target: _target, item: _item, normalised: _target.normalise(_item)});
            }));
          }),
        ]);
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

    Group object

    */
    _list.group = function () {

    }

    /*

    Unit object

    */
    _list.unit = function () {

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
            var previous;
            var searchLength = Math.floor(_storage.sorted.length / 2)
            var index = searchLength;
            while (previous !== index) {
              if (index === _storage.sorted.length) {
                break;
              }
              searchLength = Math.max(Math.floor(searchLength / 2), 1);
              previous = index
              index += _storage.compare(_datum, _storage.buffer[_storage.sorted[index]]) * searchLength;

              // boundary conditions
              index = Math.max(index, 0);
              index = Math.min(index, _storage.sorted.length);
            }

            // add to sorted
            _storage.sorted.splice(index, 0, _datum.item._id);
          }
        },
        remove: function (_datum) {

        },
        compare: function (_d1, _d2) { // override
          // returns 1 if _d1 >= _d2
          // return -1 if _d1 < _d2
          if (_d1.scores.name > _d2.scores.name) {
            return -1;
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
              return _display.render(_datum);
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
              return _filter.sort(_datum);
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
        render: function (_item) {
          return _.p();
        },
        remove: function (_item) {
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
