# coding: utf-8
# MQO file Reader/Writer.
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
    # DOTO dirlights
    cls.parse_chunk(it, {"_": lambda it,ln, line: attrs.append(tuple(re.split('\s+', line, 1)))})
    return MQScene(attrs)

  @classmethod
  def materials(cls, it, num):
    mats = []
    cls.parse_chunk(it, {"_": lambda it,ln, line: mats.append(cls.material(line, ln))})
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
    # TODO vertexattr
    map = {
      "vertex": lambda it,ln,params: verts.extend(cls.vertex(it)),
      "face":   lambda it,ln,params: face.extend(cls.faces(it)),
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
  def faces(cls, it):
    f = []
    cls.parse_chunk(it, {"_": lambda it,ln, line: f.append(cls.face(line, ln))})
    return f

  @classmethod
  def face(cls, line, ln):
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
    scenes_it = iter(doc._scene)
    objs_it = iter(doc.object)

    map = {
      "scene":    lambda it,ln,l,f: cls.scene(it, scenes_it.next(), f),
      "material": lambda it,ln,l,f: cls.materials(it, doc.material, f),
      "object":   lambda it,ln,l,f: cls.object(it, objs_it.next(), f)
    }
    cls.write_chunk(line_iter, map, f)
    return doc
  @classmethod
  def materials(cls, line_iter, mats, f):
    s = ["\ta","\r\n"]
    for ln,line in line_iter:
      if line.strip() == '}' : break
      m = re.match(r'^(\s*).*?(\s+)$',line)
      s = [m.group(1), m.group(2)]
    for m in mats:
      f.write(s[0] + str(m) + s[1])
    f.write(line)
  @classmethod
  def scene(cls, line_iter, scene, f):
    def write_attr(it,ln,line,f):
      line2 = line.strip()
      s = re.split('\s+', line2, 1)
      if s[1] == str(scene._attrs.get(s[0])):
        f.write(line)
      else:
        m = re.match(r'^(\s*[^\s]+\s+).*?(\s+)$',line)
        f.write(m.group(1) + str(scene._attrs.get(s[0])) +  m.group(2))
    map = {
      "_":    write_attr
    }
    cls.write_chunk(line_iter, map, f)
  @classmethod
  def object(cls, line_iter, obj, f):
    def write_attr(it,ln,line,f):
      line2 = line.strip()
      s = re.split('\s+', line2, 1)
      if s[1] == str(obj._attrs.get(s[0])):
        f.write(line)
      else:
        m = re.match(r'^(\s*[^\s]+\s+).*?(\s+)$',line)
        f.write(m.group(1) + str(obj._attrs.get(s[0])) +  m.group(2))
    map = {
      "vertex": lambda it,ln,l,f: cls.object_verts(it, obj, f),
      "face"  : lambda it,ln,l,f: cls.object_faces(it, obj, f),
      "_"     : write_attr
    }
    cls.write_chunk(line_iter, map, f)

  @classmethod
  def object_verts(cls, line_iter, obj, f):
    varts_it = iter(obj.vertex)
    def write_vert(it,ln,line,f):
      line2 = line.strip()
      s = re.split('\s+', line2, 1)
      p = varts_it.next().getPos()
      if [float(x) for x in re.split('\s+', line2)] == [p.x, p.y, p.z]:
        f.write(line)
      else:
        m = re.match(r'^(\s*).*?(\s+)$', line)
        f.write(m.group(1) + str(p) +  m.group(2))
    map = {
      "_":      write_vert
    }
    cls.write_chunk(line_iter, map, f)

  @classmethod
  def object_faces(cls, line_iter, obj, f):
    faces_it = iter(obj.face)
    def write_face(it,ln,line,f):
      line2 = line.strip()
      s = re.split('\s+', line2, 1)
      face = faces_it.next()
      m = re.match(r'^(\s*).*?(\s+)$', line)
      f.write(m.group(1) + str(face) +  m.group(2))
    map = {
      "_":      write_face
    }
    cls.write_chunk(line_iter, map, f)

  @classmethod
  def write_chunk(cls, line_iter, map, f):
    for ln,line in line_iter:
      line2 = line.strip()
      if line2 == '}':
        if map.has_key('_close'): map['_end_chunk'](line_iter, ln, line, f)
        f.write(line)
        break
      if line2.endswith('{'):
        f.write(line) # TODO: write in chunk.
        s = re.split('\s+', line2, 2)
        chunk = s[0].lower()
        (map.get(chunk) or (lambda i,ln,l,f: cls.write_chunk(i, {}, f)))(line_iter, ln, line, f)
        continue
      (map.get('_') or (lambda i,ln,l,f: f.write(l)))(line_iter, ln, line, f)
