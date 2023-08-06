from os import remove
from os.path import exists
from funki.λ import nop_x
from os import name

names = ['username', 'password']

if name == 'nt':
  import winreg

def read_file(filename): 
  with open(filename, 'r') as φ:
    return φ.read()

def write_file(name, value):
  with open(f'{name}.secret', 'w') as φ:
    return φ.write(value)

def if_ex_do(name, fn):
  filename = f'{name}.secret'
  if exists(filename):
    return fn(filename)

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

class POSIXCredentialManager(CredentialManager):
  __init__ = lambda self: super().__init__()
  get_var = lambda self, name: if_ex_do(name, read_file)
  set_var = lambda self, name, val: write_file(name, val) if val else nop_x
  clear = lambda self: [if_ex_do(self.keys[name], remove) for name in names]

class NTCredentialManager(CredentialManager):
  def __init__(self):
    super().__init__()

    self.reg_path=r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    self.root = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    self.policy_key = winreg.OpenKeyEx(self.root, self.reg_path)

  def get_var(self, name):
    try:
      return winreg.QueryValue(self.policy_key, str(name))
    except FileNotFoundError:
      return None

  set_var = lambda self, name, value, subkey="": winreg.SetValueEx(
    winreg.CreateKey(
      winreg.OpenKeyEx(self.root, self.reg_path, winreg.KEY_SET_VALUE),
      name
    ),
    subkey,
    0,
    winreg.REG_SZ,
    value
  )

  __del__ = lambda self: self.root.Close()

  def clear(self):
    for name in [self.keys['username'], self.keys['password']]:
      winreg.DeleteKey(self.policy_key, str(name))
