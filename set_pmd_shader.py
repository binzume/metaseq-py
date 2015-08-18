doc = MQSystem.getDocument()
for mat in doc.material:
  orgShaderName = mat.shaderName
  mat.shader = 5
  mat.shaderFilename = "pmd"
  if not mat.shaderNode is None:
    mat.shaderNode.setParameterIntValue("Toon", 5)
  if mat.textureMap != "":
    ar = mat.color.red * 60 / 100
    ag = mat.color.green * 60 / 100
    ab = mat.color.blue * 60 / 100
    mat.ambientColor = MQSystem.newColor(ar, ag, ab)
  MQSystem.println("mat: " + str(orgShaderName) + "->"+ str(mat.shaderName))
MQSystem.println("ok.")
