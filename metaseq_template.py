# coding: utf-8
import re
from collections import *

class AttrObj(object):
  def __init__(self, attrs=[], line = None):
    self._attrs = OrderedDict(attrs)
    self._line = line
  def apply_or_def(_s, f, v, default):
    return f(v) if v is not None else default
  def attr_i(self, name, default = None):
    return self.apply_or_def((lambda v:int(v)), self._attrs.get(name), default)
  def attr_f(self, name, default = None):
    return self.apply_or_def((lambda v:float(v)), self._attrs.get(name), default)
  def attr_s(self, name, default = None):
    return self.apply_or_def((lambda v:str(v).strip("\"")), self._attrs.get(name), default)
  def attr_fa(self, name, default = None, num = 1):
    f = (lambda v: [float(x) for x in re.split('\s+', v.strip(), num-1)] )
    return self.apply_or_def(f, self._attrs.get(name), default)
  def attr_p(self, name, default = None):
    return self.apply_or_def((lambda v: MQPoint(v[0],v[2],v[2])), self.attr_fa(name, None, 3), default)
  def attr_c(self, name, default = None):
    return self.apply_or_def((lambda v: MQColor(v[0],v[2],v[2])), self.attr_fa(name, None, 3), default)
  def attr_a(self, name, default = None):
    return self.apply_or_def((lambda v: MQAngle(v[0],v[2],v[2])), self.attr_fa(name, None, 3), default)

class MQDocument:
  def __init__(self):
    self.object = []
    self.material = []
    self.currentObjectIndex = -1
    self.currentMaterialIndex = -1
    self._scene = [MQScene()]
    self._mqolines = []
  def getScene(self, idx):
    return self._scene[idx]
  def addObject(self, object, parent):
    self.object.append(object)
  @property
  def numObject(self):
    return len(self.object)
  @property
  def numMaterial(self):
    return len(self.material)


class MQMaterial(AttrObj):
  #!! init
  #!! attr r  i id uid 0
  #!! attr rw s name - name
  #!! attr r_ c color - MQColor(col[0],col[1],col[2])
  #!! attr r_ f alpha - col[3]
  #!! attr rw f diffuse dif 0.0
  #!! attr rw f ambient amb 0.0
  #!! attr rw c ambientColor amb_col None
  #!! attr rw f emissive emi 0.0
  #!! attr rw c emissiveColor emi_col None
  #!! attr rw f specular spc 0.0
  #!! attr rw c specularColor spc_col None
  #!! attr rw f power power 0.0
  #!! attr rw f reflection - 0.0
  #!! attr rw f refraction - 0.0
  #!! attr rw i shader shader 0
  #!! attr rw s shaderFilename - ""
  #!! attr rw i mapType proj_type 0
  #!! attr rw s textureMap tex ""
  #!! attr rw s alphaMap aplane ""
  #!! attr rw s bumpMap bump ""
  #!! attr r  - shaderNode - None
  #!! attr rw i vertexColor vcol 0
  #!! attr rw i doubleSided dbls 0
  def __init__(self, name, attrs = []):
    AttrObj.__init__(self, attrs)
    col = self.attr_fa('col', [0,0,0,0], 4)
    #!! vars_begin self
    #!! end

  def getTextureMapPath(self):
    return self._textureMap
  def getAlphaMapPath(self):
    return self._alphaMap
  def getBumpMapPath(self):
    return self._bumpMap

  def __str__(self):
    return '"' + self._name + '" ' + ' '.join([ x+"(" + str(self._attrs[x]) + ")" for x in self._attrs if x is not None])

  #!! properties_begin
  #!! end

  @property
  def shaderName(self):
    return ['Classic','Constant','Lambert','Phong','Blinn','HLSL', '?'][self._shader]

  @color.setter
  def color(self, v):
    self._color = v
    self._attrs['col'] = str(self.color) + " " + str(self.alpha)

  @alpha.setter
  def alpha(self, v):
    self._alpha = v
    self._attrs['col'] = str(self.color) + " " + str(self.alpha)

class MQScene(AttrObj):
  #!! init
  #!! attr rw f head head 0.0
  #!! attr rw f pitch pitch 0.0
  #!! attr rw f bank bank 0.0
  #!! attr rw f fov - 60
  #!! attr r  f ortho ortho 0.0
  #!! attr r  p globalDirectionalLight - MQPoint(0,0,1)
  #!! attr r  c globalAmbientColor - MQColor(1,1,1)
  #!! attr -  p camera_pos pos MQPoint(0,0,0)
  #!! attr -  p look_at_pos lookat MQPoint(0,0,0)
  #!! attr -  a camera_angle - MQAngle(self.attr_f('head',0),self.attr_f('pitch',0),self.attr_f('bank',0))
  #!! attr -  p rotation_center - MQPoint(0,0,0)
  def __init__(self, attrs = []):
    AttrObj.__init__(self, attrs)
    #!! vars_begin self
    #!! end

  def getCameraPos(self):
    return self._camera_pos
  def setCameraPos(self, pos):
    self._camera_pos = pos
    self._attrs['pos'] = str(pos)
  def getCameraAngle(self):
    return self._camera_angle
  def getLookAtPos(self):
    return self._look_at_pos
  def getLookAtUpVec(self):
    return None
  def setLookAtPos(self, pos, v):
    self._look_at_pos = pos
    self._attrs['lookat'] = str(pos)
  def getRotationCenter(self):
    return self._rotation_center

  #!! properties_begin
  #!! end

class MQObject(AttrObj):
  #!! init
  #!! attr r  i  id uid 0
  #!! attr rw s  name - name
  #!! attr r  -  vertex - []
  #!! attr r  -  face - []
  #!! attr rw i  visible visible 1
  #!! attr rw i  lock locking 0
  #!! attr rw i  select - 0
  #!! attr r_ c  color color None
  #!! attr rw i  shading shading 0
  #!! attr rw i  patchType patch 0
  #!! attr rw i  colorValid - 0
  #!! attr r  i  depth depth 0
  #!! attr rw i  folding folding 0
  #!! attr rw p  scaling scale MQPoint(1,1,1)
  #!! attr rw a  rotation rotation MQAngle(0,0,0)
  #!! attr rw p  translation translation MQPoint(0,0,0)
  def __init__(self, name = "", attrs=[]):
    AttrObj.__init__(self, attrs)
    #!! vars_begin self
    #!! end

  #!! properties_begin
  #!! end
  @property
  def numVertex(self):
    return len(self._vertex)
  @property
  def numFace(self):
    return len(self._face)


class MQFace(AttrObj):
  #!! init
  #!! attr r  i  id UID 0
  #!! attr r  fa index V []
  #!! attr r  i  material M None
  #!! attr rw i  select - 0
  def __init__(self, name = "", attrs=[]):
    AttrObj.__init__(self, attrs)
    #!! vars_begin self
    #!! end
  #!! properties_begin
  #!! end
  @property
  def numVertex(self):
    return len(self._index)


class MQPoint:
  #!! begin_struct x y z
  #!! end

class MQCoordinate:
  #!! begin_struct u v
  #!! end

class MQColor:
  #!! begin_struct red green blue
  #!! end

class MQAngle:
  #!! begin_struct head pitch bank
  #!! end

class MQVertex:
  #!! begin_struct pos
  #!! end
  def getPos(self):
    return self.pos
  def setPos(self, pos):
    self.pos = pos

class MQMatrix:
  def get(self, r,c):
    return 0.0 # dummy

