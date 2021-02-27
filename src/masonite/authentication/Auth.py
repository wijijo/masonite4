import pendulum
import uuid

class Auth:
    def __init__(self, application, guard_config=None):
        self.application = application
        self.guards = {}
        self._guard = None
        self.guard_config = guard_config or {}
        self.options = {}

    def add_guard(self, name, guard):
        self.guards.update({name: guard})

    def set_configuration(self, config):
        self.guard_config = config
        return self

    def guard(self, guard):
        self._guard = guard
        return self

    def get_guard(self, name=None):
        if name is None and self._guard is None:
            return self.guards[self.guard_config.get("default")]

        return self.guards[self._guard]

    def get_config_options(self, guard=None):
        if guard is None:
            options = self.guard_config.get(self.guard_config.get("default"), {})
            options.update(self.options)
            return options

        options = self.guard_config.get(guard, {})
        options.update(self.options)
        return options

    def attempt(self, email, password, once=False):
        auth_config = self.get_config_options()
        auth_config.update({"once": once})
        return self.get_guard().set_options(auth_config).attempt(email, password)

    def attempt_by_id(self, user_id, once=False):
        auth_config = self.get_config_options()
        auth_config.update({"once": once})
        return self.get_guard().set_options(auth_config).attempt_by_id(user_id)

    def logout(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        self.application.make("request").remove_user()
        return self.application.make("request").delete_cookie("token")

    def user(self):
        """Logout the current authenticated user.

        Returns:
            self
        """
        auth_config = self.get_config_options()
        return self.get_guard().set_options(auth_config).user()

    def register(self, dictionary):
        """Logout the current authenticated user.

        Returns:
            self
        """
        auth_config = self.get_config_options()
        return self.get_guard().set_options(auth_config).register(dictionary)

    def password_reset(self, email):
        """Logout the current authenticated user.

        Returns:
            self
        """
        token = str(uuid.uuid4())
        try:
            self.application.make('builder').table(self.guard_config.get('password_reset_table')).create({
                "email": email,
                "token": token,
                "expires_at": pendulum.now().add(minutes=self.guard_config.get('password_reset_expiration')).to_datetime_string() if self.guard_config.get('password_reset_expiration') else None,
                "created_at": pendulum.now().to_datetime_string()
            })
        except Exception:
            return False

        self.application.make('event').fire("auth.password_reset", email, token)
        return token

    def reset_password(self, password, token):
        """Logout the current authenticated user.

        Returns:
            self
        """
        #  Get the token
        #  Check the token from the database
        #  Check the expiration of the token
        #  Delete the expiration from the token

        reset_record = self.application.make('builder').table(self.guard_config.get('password_reset_table')).where('token', token).first()
        auth_config = self.get_config_options()
        print('guard reset', reset_record.get("email"), password)
        return self.get_guard().set_options(auth_config).reset_password(reset_record.get("email"), password)
        # {'email': 'jmancuso.mil%40gmail.com', 'token': '651e67a7-8526-4614-9415-15f3561c5cff', 'expires_at': '2021-02-28 12:22:19', 'created_at': '2021-02-27 12:22:19'}


