names = ['username', 'password']

class CredentialManager:
  def __init__(self):
    self.keys = {'username': 'AWC_USER', 'password': 'AWC_PASS'}

    if not self.username or not self.password:
      _u, _p = prompt_user.to_enter_credentials_if_not_currently_stored(
        stored = {'username': self.username, 'password': self.password}
      )

      self.set_var(name=self.keys['username'], value=_u)
      self.set_var(name=self.keys['password'], value=_p)

  username = property(lambda self: self.get_var(self.keys['username']))
  password = property(lambda self: self.get_var(self.keys['password']))
  credentials = property(lambda self: (self.username, self.password))