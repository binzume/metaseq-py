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
    self._id = self.attr_i('uid',0)
    self._name = name
    self._color = MQColor(col[0],col[1],col[2])
    self._alpha = col[3]
    self._diffuse = self.attr_f('dif',0.0)
    self._ambient = self.attr_f('amb',0.0)
    self._ambientColor = self.attr_c('amb_col',None)
    self._emissive = self.attr_f('emi',0.0)
    self._emissiveColor = self.attr_c('emi_col',None)
    self._specular = self.attr_f('spc',0.0)
    self._specularColor = self.attr_c('spc_col',None)
    self._power = self.attr_f('power',0.0)
    self._reflection = 0.0
    self._refraction = 0.0
    self._shader = self.attr_i('shader',0)
    self._shaderFilename = ""
    self._mapType = self.attr_i('proj_type',0)
    self._textureMap = self.attr_s('tex',"")
    self._alphaMap = self.attr_s('aplane',"")
    self._bumpMap = self.attr_s('bump',"")
    self._shaderNode = None
    self._vertexColor = self.attr_i('vcol',0)
    self._doubleSided = self.attr_i('dbls',0)
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
  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name
  @name.setter
  def name(self, v):
    self._name = v

  @property
  def color(self):
    return self._color

  @property
  def alpha(self):
    return self._alpha

  @property
  def diffuse(self):
    return self._diffuse
  @diffuse.setter
  def diffuse(self, v):
    self._diffuse = v
    self._attrs['dif'] = str(v)

  @property
  def ambient(self):
    return self._ambient
  @ambient.setter
  def ambient(self, v):
    self._ambient = v
    self._attrs['amb'] = str(v)

  @property
  def ambientColor(self):
    return self._ambientColor
  @ambientColor.setter
  def ambientColor(self, v):
    self._ambientColor = v
    self._attrs['amb_col'] = str(v)

  @property
  def emissive(self):
    return self._emissive
  @emissive.setter
  def emissive(self, v):
    self._emissive = v
    self._attrs['emi'] = str(v)

  @property
  def emissiveColor(self):
    return self._emissiveColor
  @emissiveColor.setter
  def emissiveColor(self, v):
    self._emissiveColor = v
    self._attrs['emi_col'] = str(v)

  @property
  def specular(self):
    return self._specular
  @specular.setter
  def specular(self, v):
    self._specular = v
    self._attrs['spc'] = str(v)

  @property
  def specularColor(self):
    return self._specularColor
  @specularColor.setter
  def specularColor(self, v):
    self._specularColor = v
    self._attrs['spc_col'] = str(v)

  @property
  def power(self):
    return self._power
  @power.setter
  def power(self, v):
    self._power = v
    self._attrs['power'] = str(v)

  @property
  def reflection(self):
    return self._reflection
  @reflection.setter
  def reflection(self, v):
    self._reflection = v

  @property
  def refraction(self):
    return self._refraction
  @refraction.setter
  def refraction(self, v):
    self._refraction = v

  @property
  def shader(self):
    return self._shader
  @shader.setter
  def shader(self, v):
    self._shader = v
    self._attrs['shader'] = str(v)

  @property
  def shaderFilename(self):
    return self._shaderFilename
  @shaderFilename.setter
  def shaderFilename(self, v):
    self._shaderFilename = v

  @property
  def mapType(self):
    return self._mapType
  @mapType.setter
  def mapType(self, v):
    self._mapType = v
    self._attrs['proj_type'] = str(v)

  @property
  def textureMap(self):
    return self._textureMap
  @textureMap.setter
  def textureMap(self, v):
    self._textureMap = v
    self._attrs['tex'] = str(v)

  @property
  def alphaMap(self):
    return self._alphaMap
  @alphaMap.setter
  def alphaMap(self, v):
    self._alphaMap = v
    self._attrs['aplane'] = str(v)

  @property
  def bumpMap(self):
    return self._bumpMap
  @bumpMap.setter
  def bumpMap(self, v):
    self._bumpMap = v
    self._attrs['bump'] = str(v)

  @property
  def shaderNode(self):
    return self._shaderNode

  @property
  def vertexColor(self):
    return self._vertexColor
  @vertexColor.setter
  def vertexColor(self, v):
    self._vertexColor = v
    self._attrs['vcol'] = str(v)

  @property
  def doubleSided(self):
    return self._doubleSided
  @doubleSided.setter
  def doubleSided(self, v):
    self._doubleSided = v
    self._attrs['dbls'] = str(v)

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
    self._head = self.attr_f('head',0.0)
    self._pitch = self.attr_f('pitch',0.0)
    self._bank = self.attr_f('bank',0.0)
    self._fov = 60
    self._ortho = self.attr_f('ortho',0.0)
    self._globalDirectionalLight = MQPoint(0,0,1)
    self._globalAmbientColor = MQColor(1,1,1)
    self._camera_pos = self.attr_p('pos',MQPoint(0,0,0))
    self._look_at_pos = self.attr_p('lookat',MQPoint(0,0,0))
    self._camera_angle = MQAngle(self.attr_f('head',0),self.attr_f('pitch',0),self.attr_f('bank',0))
    self._rotation_center = MQPoint(0,0,0)
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
  @property
  def head(self):
    return self._head
  @head.setter
  def head(self, v):
    self._head = v
    self._attrs['head'] = str(v)

  @property
  def pitch(self):
    return self._pitch
  @pitch.setter
  def pitch(self, v):
    self._pitch = v
    self._attrs['pitch'] = str(v)

  @property
  def bank(self):
    return self._bank
  @bank.setter
  def bank(self, v):
    self._bank = v
    self._attrs['bank'] = str(v)

  @property
  def fov(self):
    return self._fov
  @fov.setter
  def fov(self, v):
    self._fov = v

  @property
  def ortho(self):
    return self._ortho

  @property
  def globalDirectionalLight(self):
    return self._globalDirectionalLight

  @property
  def globalAmbientColor(self):
    return self._globalAmbientColor





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
    self._id = self.attr_i('uid',0)
    self._name = name
    self._vertex = []
    self._face = []
    self._visible = self.attr_i('visible',1)
    self._lock = self.attr_i('locking',0)
    self._select = 0
    self._color = self.attr_c('color',None)
    self._shading = self.attr_i('shading',0)
    self._patchType = self.attr_i('patch',0)
    self._colorValid = 0
    self._depth = self.attr_i('depth',0)
    self._folding = self.attr_i('folding',0)
    self._scaling = self.attr_p('scale',MQPoint(1,1,1))
    self._rotation = self.attr_a('rotation',MQAngle(0,0,0))
    self._translation = self.attr_p('translation',MQPoint(0,0,0))
    #!! end

  #!! properties_begin
  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name
  @name.setter
  def name(self, v):
    self._name = v

  @property
  def vertex(self):
    return self._vertex

  @property
  def face(self):
    return self._face

  @property
  def visible(self):
    return self._visible
  @visible.setter
  def visible(self, v):
    self._visible = v
    self._attrs['visible'] = str(v)

  @property
  def lock(self):
    return self._lock
  @lock.setter
  def lock(self, v):
    self._lock = v
    self._attrs['locking'] = str(v)

  @property
  def select(self):
    return self._select
  @select.setter
  def select(self, v):
    self._select = v

  @property
  def color(self):
    return self._color

  @property
  def shading(self):
    return self._shading
  @shading.setter
  def shading(self, v):
    self._shading = v
    self._attrs['shading'] = str(v)

  @property
  def patchType(self):
    return self._patchType
  @patchType.setter
  def patchType(self, v):
    self._patchType = v
    self._attrs['patch'] = str(v)

  @property
  def colorValid(self):
    return self._colorValid
  @colorValid.setter
  def colorValid(self, v):
    self._colorValid = v

  @property
  def depth(self):
    return self._depth

  @property
  def folding(self):
    return self._folding
  @folding.setter
  def folding(self, v):
    self._folding = v
    self._attrs['folding'] = str(v)

  @property
  def scaling(self):
    return self._scaling
  @scaling.setter
  def scaling(self, v):
    self._scaling = v
    self._attrs['scale'] = str(v)

  @property
  def rotation(self):
    return self._rotation
  @rotation.setter
  def rotation(self, v):
    self._rotation = v
    self._attrs['rotation'] = str(v)

  @property
  def translation(self):
    return self._translation
  @translation.setter
  def translation(self, v):
    self._translation = v
    self._attrs['translation'] = str(v)

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
    self._id = self.attr_i('UID',0)
    self._index = self.attr_fa('V',[])
    self._material = self.attr_i('M',None)
    self._select = 0
    #!! end
  #!! properties_begin
  @property
  def id(self):
    return self._id

  @property
  def index(self):
    return self._index

  @property
  def material(self):
    return self._material

  @property
  def select(self):
    return self._select
  @select.setter
  def select(self, v):
    self._select = v

  #!! end
  @property
  def numVertex(self):
    return len(self._index)


class MQPoint:
  #!! begin_struct x y z
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
  def __str__(self):
    return ' '.join([ str(self.x),str(self.y),str(self.z) ])
  #!! end

class MQCoordinate:
  #!! begin_struct u v
  def __init__(self, u, v):
    self.u = u
    self.v = v
  def __str__(self):
    return ' '.join([ str(self.u),str(self.v) ])
  #!! end

class MQColor:
  #!! begin_struct red green blue
  def __init__(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
  def __str__(self):
    return ' '.join([ str(self.red),str(self.green),str(self.blue) ])
  #!! end

class MQAngle:
  #!! begin_struct head pitch bank
  def __init__(self, head, pitch, bank):
    self.head = head
    self.pitch = pitch
    self.bank = bank
  def __str__(self):
    return ' '.join([ str(self.head),str(self.pitch),str(self.bank) ])
  #!! end

class MQVertex:
  #!! begin_struct pos
  def __init__(self, pos):
    self.pos = pos
  def __str__(self):
    return ' '.join([ str(self.pos) ])
  #!! end
  def getPos(self):
    return self.pos
  def setPos(self, pos):
    self.pos = pos

class MQMatrix:
  def get(self, r,c):
    return 0.0 # dummy

