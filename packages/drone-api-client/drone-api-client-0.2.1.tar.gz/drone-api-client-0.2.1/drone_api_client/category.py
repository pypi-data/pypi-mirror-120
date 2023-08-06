import json

from drone_api_client.model.cron import DroneCron
from .model.secrets import DroneSecret
from .model.user import DroneUser
from .session import Session


class Base:
    def __init__(self, session):
        self._session: Session = session


class Cron(Base):
    def create_cron(self, name: str, expr: str, branch: str = 'master') -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_create/

        Create cron in repository
        :param name: name of cron job
        :param expr: cron expression
        :param branch: branch were cron will be runs
        :return: DroneCron object with created cron job
        """
        data = json.dumps({
            'name': name,
            'expr': expr,
            'branch': branch
        })
        return DroneCron(self._session.post('/cron', data=data))

    def delete_cron(self, cron_name: str) -> None:
        """
        https://docs.drone.io/api/cron/cron_delete/

        Delete existing cron in repository
        :param cron_name: existing cron in repository
        :return: None
        """
        return self._session.delete(f'/cron/{cron_name}')

    def get_cron_info(self, cron_name: str) -> [] or DroneCron:
        """
        https://docs.drone.io/api/cron/cron_info/

        :param cron_name: existing cron name
        :return: DroneCron object if cron exists
        """
        result = self._session.get(f'/cron/{cron_name}')
        return [] if 'message' in result else DroneCron(result)

    def get_cron_list(self) -> [DroneCron]:
        """
        https://docs.drone.io/api/cron/cron_list/

        :return: Returns list of all cron jobs in repository
        """
        return list(DroneCron(cron) for cron in self._session.get('/cron'))

    def execute(self, cron_name: str) -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_trigger/

        Execute existing cron expression
        :param cron_name: existing cron name
        :return: executed cron
        """
        return DroneCron(self._session.post(f'/cron/{cron_name}'))

    def update_cron(self, name: str, expr: str = None, branch: str = 'master') -> DroneCron:
        """
        https://docs.drone.io/api/cron/cron_update/

        :param name: existing crone name
        :param expr: new cron expression. Optional
        :param branch: new branch. Optional. Default - master
        :return: Updated cron
        """
        cron = self.get_cron_info(name)
        if isinstance(cron, (list, tuple)):
            return "Cron expression with given name doesn't found"
        cron.expr = expr if expr else cron.expr
        cron.branch = branch
        return DroneCron(self._session.patch(f'/cron/{cron.name}', cron.to_json()))


class Secrets(Base):
    def create(self, name: str, data: str, pull_request: bool = True) -> DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_create/

        Create secret in repository
        :param name: new secret name
        :param data: data for secret
        :param pull_request:
        :return: DroneSecret object with created secret
        """

        secret = json.dumps({'name': name, 'data': data, 'pull_request': pull_request})
        return DroneSecret(self._session.post('/secrets', data=secret))

    def delete(self, secret_name: str) -> None:
        """
        https://docs.drone.io/api/secrets/secret_delete/

        Delete secret from repository
        :param secret_name:
        :return: None
        """

        self._session.delete(f'/secrets/{secret_name}')

    def get_secret_info(self, secret_name: str) -> [] or DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_info/

        Returns DroneSecret object if secrets found in repository
        :param secret_name: existing secret name
        :return:
        """

        result = self._session.get(f'/secrets/{secret_name}')
        return [] if 'message' in result else DroneSecret(result)

    def get_secrets(self) -> [DroneSecret]:
        """
        https://docs.drone.io/api/secrets/secret_list/

        Returns list of all secrets in repository
        :return: List of DroneSecret in repo
        """

        return [DroneSecret(secret) for secret in self._session.get('/secrets')]

    def update_secret(self, secret_name: str, data: str = None, pull_request: bool = None) -> DroneSecret:
        """
        https://docs.drone.io/api/secrets/secret_update/

        Returns updated drone secret
        :param secret_name: existing secret
        :param data: new data in secret
        :param pull_request: bool value
        :return: DroneSecret object
        """

        secret = self.get_secret_info(secret_name)
        if isinstance(secret, (list, tuple)):
            return "Secret with given name doesn't found"
        secret.data = data
        secret.pull_request = pull_request
        return DroneSecret(self._session.patch(f'/secrets/{secret.name}', data=secret.to_json()))


class User(Base):
    def get_user_builds(self):
        return self._session.get('/user/builds', add_repo=False)

    def get_user_info(self) -> DroneUser:
        """
        https://docs.drone.io/api/user/user_info/

        :return: Current dron user
        """
        return DroneUser(self._session.get('/user', add_repo=False))

    def get_user_repos(self):
        return self._session.get('/user/repos', add_repo=False)

    def sync_user_repos_list(self):
        return self._session.post('/user/repos', add_repo=False)


class Users(Base):
    def create_user(self, login: str, email: str, active: bool = True, avatar_url: str = '') -> DroneUser:
        """
        https://docs.drone.io/api/users/users_create/

        :param login: login for new user
        :param email: email for new user
        :param active: is active user. Default is True
        :param avatar_url: link to user avatar. Default is ''
        :return: created user
        """
        new_user = DroneUser(
            {key: value for key, value in locals().items() if key != 'self' and '__py' not in key}).to_create()
        return DroneUser(self._session.post('/users', data=new_user, add_repo=False))

    def delete_user(self, login: str) -> None:
        """
        https://docs.drone.io/api/users/users_delete/

        Delete existing user
        :param login: existing user login
        :return: None
        """
        self._session.delete(f'/users/{login}', add_repo=False)

    def get_user_info(self, login: str) -> [] or DroneUser:
        """
        https://docs.drone.io/api/users/users_info/

        :param login: existing user login
        :return: DroneUser object with user
        """
        result = self._session.get(f'/users/{login}', add_repo=False)
        return [] if 'message' in result else DroneUser(result)

    def get_users_list(self) -> [DroneUser]:
        """
        https://docs.drone.io/api/users/users_list/

        :return: List of users
        """
        return [DroneUser(user) for user in self._session.get('/users', add_repo=False)]
