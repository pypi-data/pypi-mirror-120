from os import remove
from os.path import exists

from funki.λ import nop_x

from credentia.credential_manager import names
from credentia.credential_manager import CredentialManager

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

class POSIXCredentialManager(CredentialManager):
  __init__ = lambda self: super().__init__()
  get_var = lambda self, name: if_ex_do(name, read_file)
  set_var = lambda self, name, val: write_file(name, val) if val else nop_x
  clear = lambda self: [if_ex_do(self.keys[name], remove) for name in names]
