from .category import Cron, Secrets, User, Users
from .session import Session


class DroneApi(Session):

    @property
    def cron(self):
        return Cron(self)

    @property
    def secrets(self):
        return Secrets(self)

    @property
    def user(self):
        return User(self)

    @property
    def users(self):
        return Users(self)
