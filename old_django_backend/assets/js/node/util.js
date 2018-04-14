
/*

Util.js

Contains commonly used shortcuts and utilities

*/

var http = require('http');

var _ = {

  // promises
  p: function (arg) {
    if (arg !== undefined && arg.then !== undefined) {
      return arg.then(function (final) {
        return final;
      });
    } else {
      return new Promise(function (resolve, reject) {
        resolve(_.is.f(arg) ? arg() : arg);
      });
    }
  },
  all: function (list) {
    return Promise.all((list || []));
  },
  pmap: function (object, fn) {
    return _.all(Object.keys(object).map(function (key) {
      let obj = object[key];
      return fn(key, obj);
    }));
  },
  _all: function (fnList, input) {
    fnList = (fnList || []);
    return fnList.reduce(function (whole, part) {
      return whole.then(function (value) {
        return part(value);
      });
    }, _.p(input));
  },
  _pmap: function (object, fn) {
    return _._all(Object.keys(object).map(function (key) {
      return function () {
        let obj = object[key];
        return fn(key, obj);
      }
    }));
  },

  // objects
  merge: function (...objects) {
    return objects.reduce(function (whole, part) {
      part = (part || {});
      Object.keys(part).forEach(function (key) {
        if (key in whole) {
          if (_.is.object.all(whole[key]) && _.is.object.all(part[key])) {
            whole[key] = _.merge(whole[key], part[key]); // objects go deeper again recursively
          } else if (_.is.array(whole[key]) && _.is.array(part[key])) {
            whole[key] = [...new Set([...whole[key], ...part[key]])]; // arrays union
          } else {
            whole[key] = part[key]; // strings and "other" replace
          }
        } else {
          whole[key] = part[key]; // add if it does not exist
        }
      });
      return whole;
    }, {});
  },
  map: function (object, fn) {
    return Object.keys(object).map(function (key) {
      let obj = object[key];
      return fn(key, obj);
    });
  },

  // console
  l: console.log,

  // tests
  is: {
    f: function (obj) {
      return !!(obj && obj.constructor && obj.call && obj.apply);
    },
    object: {
      empty: function (e) {
        for (var t in e) {
          return false;
        }
        return true;
      },
      all: function (obj) {
        return obj !== null && typeof obj === 'object' && !_.is.array(obj);
      },
    },
    array: function (obj) {
      return Object.prototype.toString.call(obj) === '[object Array]';
    },
    number: function (n) {
      return typeof n === 'number' && (n % 1) === 0;
    },
  },

  // requests
  request: function (url, type, data) {
    type = (type || 'GET');
    return new Promise(function (resolve, reject) {
      // make a request
      // const options = ;
      const request = http.request({
        port: 8000,
        hostname: 'localhost',
        path: type === 'GET' ? `${url}?${_.params(data)}` : url,
        method: type,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': _.token ? `Token ${_.token}` : '',
        }
      });
      // request.write();
      request.on('response', function(response) {
        var text = '';
        response.on('data', function (chunk) {
          text += chunk;
        });
        response.on('end', function () {
          resolve(JSON.parse(text));
        });
      });
      request.end(JSON.stringify(data || {}));
    });
  },
  params: function (obj) {
    obj = (obj || {});
    return _.map(obj, function (key, value) {
      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
    }).reduce(function (whole, part) {
      return whole ? `${whole}&${part}` : part;
    }, '');
  },
}

module.exports = _;
