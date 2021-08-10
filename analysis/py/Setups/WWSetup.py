class WWSetup:
  """ Storage class for the WW physics setup.
  """
  def __init__(self, name=None, use_TGCs=None, use_s0=None, use_A=None):
    self.name = name
    self.use_TGCs = use_TGCs
    self.use_s0 = use_s0
    self.use_A = use_A