
# Local
from apps.rowbot.models.asset import AssetModel, Asset, AssetInstance
from apps.rowbot.models.club import Club
from apps.rowbot.models.event import EventModel, EventNotificationModel, Event, EventInstance, EventNotification
from apps.rowbot.models.member import Member
from apps.rowbot.models.role import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from apps.rowbot.models.team import TeamModel, Team, TeamInstance, TeamRecord

'''

--- Model-Object-Instance Structure ---

Most objects find themselves with a Model-Object-Instance kind of structure. This allows for common elements of different objects to be abstracted out, and time-dependent aspects of similar events to be tracked in a consistent way.

"Model": A general category when you need to create a new object, e.g. {EventModel: Race}
"Object": A specific implementation of a general category, but with no time-dependence, e.g. {Event: Emma Sprints}
"Instance": A time-dependent unit of the event, e.g. {EventInstance: Emma Sprints 2017}

This allows instances of the same event to be compared easily across a timescale. This is especially useful with Roles and other objects. A Role can encode a set of responsabilities that a member currently has in a club, but the RoleInstances attached to that Role can allow progress such as weight or power-to-weight ratio to be recorded over time. It can also allow attendance in events to be recorded by creating a new RoleInstance for an event for example.

'''
