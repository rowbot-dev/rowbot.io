
// create an event 20 seconds in the future and have it scheduled.
function create_and_schedule_event () {
  return _.all([
    api.models.Event.objects.get({name: 'Test 1'}),
    api.models.Role.objects.get({name: 'Test 1'}),
  ]).then(function (result) {

    var start_time = moment();
    var end_time = start_time.clone().add(20, 'seconds');

    return api.models.EventInstance.objects.create({
      event: result._id,
      start_time: start_time._d,
      end_time: end_time._d,
      location: 'some location',
      description: 'a test',
      roles: [],
    });
  });
}
