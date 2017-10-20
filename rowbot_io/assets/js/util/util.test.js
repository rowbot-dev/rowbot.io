
/*

Util.js

Contains commonly used shortcuts and utilities

*/

var _ = {

  // promises
  p: function (arg) {
    return new Promise(function (resolve, reject) {
      resolve(_.is.f(arg) ? arg() : arg);
    });
  },
  all: function (list) {
    return Promise.all((list || []));
  },
  map: function (object, fn) {
    return _.all(Object.keys(object).map(function (key) {
      let obj = object[key];
      return fn(key, obj);
    }));
  },

  // console
  l: console.log,

  // tests
  is: {
    f: function (obj) {
      return !!(obj && obj.constructor && obj.call && obj.apply);
    },
  },

  // DOM
  dom: {
    get: function (_id) {
      return document.getElementById(_id);
    },
  },

  // requests
  request: function (url, data) {
    return new Promise(function (resolve, reject) {
      var http = new XMLHttpRequest();
      http.open('POST', url, true);
      http.setRequestHeader('Content-Type', 'application/json');
      http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
          resolve(JSON.parse(http.responseText));
        }
      }
      http.send(JSON.stringify(data));
    });
  },
}
