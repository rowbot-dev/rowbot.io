
var api = require('./api');
var _ = require('./util');

api.setup().then(function () {
  return api.getToken('npiano', 'mach');
}).then(function () {
  return api.models.Member.objects.all({force: true});
}).then(function (results) {
  _.l(results);
});
