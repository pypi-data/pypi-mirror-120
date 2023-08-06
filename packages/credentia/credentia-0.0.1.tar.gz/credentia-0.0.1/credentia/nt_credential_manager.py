from credentia.credential_manager.credential_manager import CredentialManager

from os import name

if name == 'nt':
  import winreg

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
