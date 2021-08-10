class MuAccSetup:
  """ Storage class for the muon acceptance setup.
  """
  def __init__(self, name=None, costh=None, c_setup=None, w_setup=None):
    self.name = name
    self.costh = costh
    self.c_setup = c_setup
    self.w_setup = w_setup