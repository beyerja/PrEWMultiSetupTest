class RunSetup:
  """ Storage class for the a collider run setup.
  """
  def __init__(self, name, PeM, PeP, L_setup, P_setup):
    self.name = name
    self.PeM = PeM
    self.PeP = PeP
    self.L_setup = L_setup
    self.P_setup = P_setup