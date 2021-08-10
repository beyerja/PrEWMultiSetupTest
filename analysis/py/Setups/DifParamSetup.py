class DifParamSetup:
  """ Storage class for the difermion parametrisation setup.
  """
  def __init__(self, name=None, s0_setup=None, Ae_setup=None, Af_setup=None, 
               ef_setup=None, k0_setup=None, dk_setup=None, constr_type=None):
    self.name = name
    self.s0_setup = s0_setup
    self.Ae_setup = Ae_setup
    self.Af_setup = Af_setup
    self.ef_setup = ef_setup
    self.k0_setup = k0_setup
    self.dk_setup = dk_setup
    self.constr_type = constr_type