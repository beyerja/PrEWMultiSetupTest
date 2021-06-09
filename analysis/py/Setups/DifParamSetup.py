class DifParamSetup:
  """ Storage class for the difermion parametrisation setup.
  """
  def __init__(self, name, s0_setup, Ae_setup, Af_setup, ef_setup, kL_setup, kR_setup, constr_type=None):
    self.name = name
    self.s0_setup = s0_setup
    self.Ae_setup = Ae_setup
    self.Af_setup = Af_setup
    self.ef_setup = ef_setup
    self.kL_setup = kL_setup
    self.kR_setup = kR_setup
    self.constr_type = constr_type