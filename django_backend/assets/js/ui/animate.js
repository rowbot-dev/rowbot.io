// To eventually replace jquery.animate

// animate with duration
// var frameLength = 10; // 10ms steps
// var steps = duration / frameLength;
//
// // difference for each parameter
// var _diffs = {};
// _.map(_style, function (key, value) {
//   if (['left', 'top', 'width', 'height'].contains(key)) {
//     _diffs[key] = parseInt(value) - parseInt(_original[key] || 0);
//   }
// });
//
// return new Promise(function (resolve, reject) {
//   Array.range(steps).map(function (step) {
//     setTimeout(function () {
//       if (step == steps - 1) {
//         resolve();
//       } else {
//         _.map(_style, function (key, value) {
//           if (key in _diffs) {
//             let value = parseInt(_original[key] || 0) + _diffs[key] / steps * step;
//             _.l(element.id);
//             element.style[key] = `${value}px`;
//           }
//         });
//       }
//     }, step * frameLength);
//   });
// });
