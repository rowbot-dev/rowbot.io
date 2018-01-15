
/*

Util.js

Contains commonly used shortcuts and utilities

*/

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
    // return Promise.mapSeries()
    fnList = (fnList || []);
    var results = [];
    return fnList.reduce(function (whole, part) {
      return whole.then(function (value) {
        return _.is.f(part) ? part(value) : value;
      }).then(function (result) {
        results.push(result);
        return result;
      });
    }, _.p(input)).then(function () {
      return results;
    });
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
      if (_.is.array(part)) {
        whole = (whole || []);
        whole = [...new Set([...whole, ...part])]; // union
      } else {
        whole = (whole || {});
        part = (part || {});
        Object.keys(part).forEach(function (key) {
          if ((key in whole && _.is.object.all(whole[key]) && _.is.object.all(part[key])) || (_.is.array(whole[key]) && _.is.array(part[key]))) {
            whole[key] = _.merge(whole[key], part[key]); // objects go deeper again recursively
          } else {
            whole[key] = part[key]; // add if it does not exist
          }
        });
      }
      return whole;
    });
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

  // DOM
  dom: {
    get: function (_id) {
      return document.getElementById(_id);
    },
  },
  css: {
    create: function (selector, style) {
      if (!document.styleSheets) return;
      if (document.getElementsByTagName('head').length == 0) return;

      var styleSheet, mediaType;

      if (document.styleSheets.length > 0) {
        for (var i = 0, l = document.styleSheets.length; i < l; i++) {
          if (document.styleSheets[i].disabled)
          continue;
          var media = document.styleSheets[i].media;
          mediaType = typeof media;

          if (mediaType === 'string') {
            if (media === '' || (media.indexOf('screen') !== -1)) {
              styleSheet = document.styleSheets[i];
            }
          }
          else if (mediaType=='object') {
            if (media.mediaText === '' || (media.mediaText.indexOf('screen') !== -1)) {
              styleSheet = document.styleSheets[i];
            }
          }

          if (typeof styleSheet !== 'undefined')
          break;
        }
      }

      if (typeof styleSheet === 'undefined') {
        var styleSheetElement = document.createElement('style');
        styleSheetElement.type = 'text/css';
        document.getElementsByTagName('head')[0].appendChild(styleSheetElement);

        for (i = 0; i < document.styleSheets.length; i++) {
          if (document.styleSheets[i].disabled) {
            continue;
          }
          styleSheet = document.styleSheets[i];
        }

        mediaType = typeof styleSheet.media;
      }

      if (mediaType === 'string') {
        for (var i = 0, l = styleSheet.rules.length; i < l; i++) {
          if(styleSheet.rules[i].selectorText && styleSheet.rules[i].selectorText.toLowerCase()==selector.toLowerCase()) {
            styleSheet.rules[i].style.cssText = style;
            return;
          }
        }
        styleSheet.addRule(selector,style);
      }
      else if (mediaType === 'object') {
        var styleSheetLength = (styleSheet.cssRules) ? styleSheet.cssRules.length : 0;
        for (var i = 0; i < styleSheetLength; i++) {
          if (styleSheet.cssRules[i].selectorText && styleSheet.cssRules[i].selectorText.toLowerCase() == selector.toLowerCase()) {
            styleSheet.cssRules[i].style.cssText = style;
            return;
          }
        }
        styleSheet.insertRule(selector + '{' + style + '}', styleSheetLength);
      }
    }
  },

  // requests
  params: function (obj) {
    obj = (obj || {});
    return _.map(obj, function (key, value) {
      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
    }).reduce(function (whole, part) {
      return whole ? `${whole}&${part}` : part;
    }, '');
  },

  // duration formatting
  duration: function (number, string) {
    var data = moment.duration(number, string)._data;
    return `${data.days} ${data.hours}:${data.minutes}:${data.seconds}.${data.milliseconds * 1000}`;
  },

  // id
  id: function (length) {
    length = (length || 10);
    return Math.random().toString(36).substring(2, length+2);
  },
}
