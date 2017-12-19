
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
    _models.Club.objects.get({name: 'TestClub0'}),

    // member
    _models.Member.objects.get({username: 'npiano'}),
  ]).then(function (results) {
    var [_club, _member] = results;

    return _.all([
      _models.RoleModel.objects.get({reference: 'admin'}),
      _models.EventModel.objects.get({reference: 'test'}),
    ]).then(function (results) {
      var [_roleModel, _eventModel] = results;

      return _.all([
        // event notification models
        _models.EventNotificationModel.objects.create({
          model: _eventModel._id,
          name: 'first',
          relative_duration: _.duration(6, 'seconds'),
          is_negative: true,
        }),
        _models.EventNotificationModel.objects.create({
          model: _eventModel._id,
          name: 'second',
          relative_duration: _.duration(3, 'seconds'),
          is_negative: true,
        }),
        _models.EventNotificationModel.objects.create({
          model: _eventModel._id,
          name: 'third',
          relative_duration: _.duration(0, 'seconds'),
        }),

        // event
        _models.Event.objects.create({
          model: _eventModel._id,
          name: 'TestEvent',
          description: 'test',
        }),

        // role
        _models.Role.objects.create({
          model: _roleModel._id,
          member: _member._id,
          nickname: 'admin',
        }),

      ]).then(function (results) {
        var [_first, _second, _third, _event, _role] = results;

        return _models.EventInstance.objects.create({
          event: _event._id,
          start_time: start_time._d,
          end_time: end_time._d,
          location: 'some location',
          description: 'a test',
          // roles: [], // test by creating role instance first and putting id here
        }).then(function (_eventInstance) {
          _.l(_role);
          return _models.RoleInstance.objects.create({
            role: _role._id,
            event: _eventInstance._id,
          });
        });
      });
    });
  });
}
