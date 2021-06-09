class MuAccSetup:
  """ Storage class for the muon acceptance setup.
  """
  def __init__(self, name, costh, c_setup, w_setup):
    self.name = name
    self.costh = costh
    self.c_setup = c_setup
    self.w_setup = w_setup