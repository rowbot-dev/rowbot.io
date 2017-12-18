
// create an event 20 seconds in the future and have it scheduled.
function create_and_schedule_event () {

  // steps
  // get club
  // get member
  // get or create event model
  // get or create event notification models
  // get or create role
  // create event instance
  // create role instance

  var _models = api.models;
  var start_time = moment();
  var end_time = start_time.clone().add(20, 'seconds');

  return _.all([
    // club
    _models.Club.objects.get({}),

    // member
    _models.Member.objects.get({}),
  ]).then(function (results) {
    var [_club, _member] = results;

    return _.all([
      _models.Role.objects.create({}),
      _models.EventModel.objects.create({}),
    ]).then(function (results) {
      var [_role, _eventModel] = results;

      return _.all([
        // event notification models
        _models.EventNotificationModel.objects.create({}),
        _models.EventNotificationModel.objects.create({}),
        _models.EventNotificationModel.objects.create({}),

        // event
        _models.Event.objects.create({}),
      ]).then(function (results) {
        var [_first, _second, _third, _event] = results;

        return _models.EventInstance.objects.create({
          event: _event._id,
          start_time: start_time._d,
          end_time: end_time._d,
          location: 'some location',
          description: 'a test',
          roles: [], // test by creating role instance first and putting id here
        }).then(function (_eventInstance) {
          return _models.RoleInstance.objects.create({});
        });
      });
    });
  });
}
