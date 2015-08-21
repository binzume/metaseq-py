# coding: utf-8
from metaseq import *

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
    face = []
    map = {
      "vertex": lambda it,ln,params: verts.extend(cls.vertex(it)),
      "face":   lambda it,ln,params: face.extend(cls.face(it)),
      "_":      lambda it,ln,line: attrs.append(tuple(re.split('\s+', line, 1)))
    }
    cls.parse_chunk(it, map)
    obj = MQObject(name, attrs)
    obj._vertex = verts
    obj._face = face
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
  def face(cls, it):
    f = []
    map = {"_": lambda it,ln, line: f.append(cls.face2(line, ln))}
    cls.parse_chunk(it, map)
    return f

  @classmethod
  def face2(cls, line, ln):
    s = re.split('\s+', line, 1)
    attrs = [x.strip().split('(', 1) for x in s[1].split(')')]
    m = MQFace(s[0].strip('"'), [(x[0], x[1]) for x in attrs if len(x)==2])
    m._line = ln
    return m

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

