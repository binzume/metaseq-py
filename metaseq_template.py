# coding: utf-8
import re
from collections import *

class AttrObj(object):
  def apply_or_def(_s, f, v, default):
    return f(v) if v is not None else default
  def attr_i(self, name, default = None):
    return self.apply_or_def((lambda v:int(v)), self._attrs.get(name), default)
  def attr_f(self, name, default = None):
    return self.apply_or_def((lambda v:float(v)), self._attrs.get(name), default)
  def attr_s(self, name, default = None):
    return self.apply_or_def((lambda v:str(v).strip("\"")), self._attrs.get(name), default)
  def attr_fa(self, name, num, default = None):
    f = (lambda v: [float(x) for x in re.split('\s+', v.strip(), num-1)] )
    return self.apply_or_def(f, self._attrs.get(name), default)
  def attr_p(self, name, default = None):
    return self.apply_or_def((lambda v: MQPoint(v[0],v[2],v[2])), self.attr_fa(name, 3), default)
  def attr_c(self, name, default = None):
    return self.apply_or_def((lambda v: MQColor(v[0],v[2],v[2])), self.attr_fa(name, 3), default)
  def attr_a(self, name, default = None):
    return self.apply_or_def((lambda v: MQAngle(v[0],v[2],v[2])), self.attr_fa(name, 3), default)

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
    self._line = None
    self._attrs = OrderedDict(attrs)
    col = self.attr_fa('col', 4, [0,0,0,0])
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
    self._line = None
    self._attrs = OrderedDict(attrs)
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
    self._attrs = OrderedDict(attrs)
    self._line = None
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


class MQOReader:
  @classmethod
  def load(cls, filename):
    lines = open(filename, 'rb').readlines()
    it = enumerate(lines)
    doc = MQDocument()
    doc._mqolines = lines
    doc._scene = []
    map = {
      "scene":    lambda it,ln,params: doc._scene.append(cls.scene(it)),
      "material": lambda it,ln,params: doc.material.extend(cls.materials(it, int(params[1]))),
      "object":   lambda it,ln,params: doc.object.append(cls.object(it, ln, params[1]))
    }
    cls.parse_chunk(it, map)
    return doc

  @classmethod
  def scene(cls, it):
    attrs = []
    map = {"_": lambda it,ln, line: attrs.append(tuple(re.split('\s+', line, 1)))}
    cls.parse_chunk(it, map)
    return MQScene(attrs)

  @classmethod
  def materials(cls, it, num):
    mats = []
    map = {"_": lambda it,ln, line: mats.append(cls.material(line, ln))}
    cls.parse_chunk(it, map)
    return mats

  @classmethod
  def material(cls, line, ln):
    s = re.split('\s+', line, 1)
    attrs = [x.strip().split('(', 1) for x in s[1].split(')')]
    m = MQMaterial(s[0].strip('"'), [(x[0], x[1]) for x in attrs if len(x)==2])
    m._line = ln
    return m

  @classmethod
  def object(cls, it, ln, name):
    attrs = []
    verts = []
    map = {
      "vertex": lambda it,ln,params: verts.extend(cls.vertex(it)),
      "_":      lambda it,ln,line: attrs.append(tuple(re.split('\s+', line, 1)))
    }
    cls.parse_chunk(it, map)
    obj = MQObject(name, attrs)
    obj._vertex = verts
    obj._line = ln
    return obj
  @classmethod

  def vertex(cls, it):
    verts = []
    map = {
      "_": lambda it,ln,line: verts.append(MQVertex(MQPoint(*[float(x) for x in re.split('\s+', line)])))
    }
    cls.parse_chunk(it, map)
    return verts

  @classmethod
  def parse_chunk(cls, line_iter, map):
    for ln,line in line_iter:
      line = line.strip()
      if line == '}': break
      if line.endswith('{'):
        s = re.split('\s+', line, 2)
        chunk = s[0].lower()
        if map.has_key(chunk):
          map[chunk](line_iter, ln, s)
        else:
          cls.parse_chunk(line_iter, {})
        continue
      if map.has_key('_'): map['_'](line_iter, ln, line)

class MQOWriter:
  @classmethod
  def save(cls, filename, doc):
    f = open(filename, 'wb')
    line_iter = enumerate(doc._mqolines)
    scenecount = 0
    objcount = 0
    for ln,line in line_iter:
      line2 = line.strip()
      if line2.endswith('{'):
        s = re.split('\s+', line2, 2)
        chunk = s[0].lower()
        f.write(line)
        if chunk == "material":
          cls.materials(line_iter, doc.material, f)
        if chunk == "scene":
          cls.scene(line_iter, doc.getScene(scenecount), f)
          scenecount+=1
        if chunk == "object":
          cls.object(line_iter, doc.object[objcount], f)
          objcount+=1
        continue
      f.write(line)
    return doc
  @classmethod
  def materials(cls, line_iter, mats, f):
    s = ["\t","\r\n"]
    for ln,line in line_iter:
      if line.strip() == '}' : break
      m = re.match(r'^(\s*).*?(\s+)$',line)
      s = [m.group(1), m.group(2)]
    for m in mats:
      f.write(s[0] + str(m) + s[1])
    f.write(line)
  @classmethod
  def scene(cls, line_iter, scene, f):
    s = ["\t","\n"]
    for ln,line in line_iter:
      line2 = line.strip()
      if line2 == '}': break
      if line2.endswith('{'):
        f.write(line)
        cls.copy(line_iter, f)
        continue
      s = re.split('\s+', line2, 1)
      if s[1] == str(scene._attrs.get(s[0])):
        f.write(line)
      else:
        m = re.match(r'^(\s*[^\s]+\s+).*?(\s+)$',line)
        f.write(m.group(1) + str(scene._attrs.get(s[0])) +  m.group(2))
    f.write(line)
  @classmethod
  def object(cls, line_iter, obj, f):
    s = ["\t","\n"]
    for ln,line in line_iter:
      line2 = line.strip()
      if line2 == '}': break
      if line2.endswith('{'):
        f.write(line)
        cls.copy(line_iter, f)
        continue
      s = re.split('\s+', line2, 1)
      if s[1] == str(obj._attrs.get(s[0])):
        f.write(line)
      else:
        m = re.match(r'^(\s*[^\s]+\s+).*?(\s+)$',line)
        f.write(m.group(1) + str(obj._attrs.get(s[0])) +  m.group(2))
    f.write(line)
  @classmethod
  def copy(cls, line_iter, f):
    for ln,line in line_iter:
      f.write(line)
      line = line.strip()
      if line == '}': break
      if line.endswith('{'):
        cls.copy(line_iter,f)
