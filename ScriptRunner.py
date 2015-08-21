#!/usr/bin/env python
# coding: utf-8
import sys
from metaseq import *
from mqo import *

class MQSystemClass:

  def __init__(self, filename):
    self.mqo_loadFile(filename)

  def mqo_loadFile(self, fname): # for ScriptRunner
    self.doc = MQOReader.load(fname)
  def mqo_saveFile(self, fname): # for ScriptRunner
    MQOWriter.save(fname, self.doc)

  def getDocument(self):
    return self.doc
  def newObject(self):
    return MQObject()
  def newMaterial(self):
    return MQMaterial()
  def newPoint(self, x,y,z):
    return MQPoint(x,y,z)
  def newCoordinate(self, u,v):
    return MQCoordinate(u,v)
  def newColor(self, r,g,b):
    return MQColor(r,g,b)
  def newAngle(self, head,pitch,bank):
    return MQAngle(head,pitch,bank)
  def newMatrix(self):
    return MQMatrix()
  def messageBox(self, msg):
    print("# messageBox" + msg + "\n")
  def println(self, s):
    print(s)
  def clearLog(self):
    print("# ****** clear log ******")

class Script:
  def __init__(self, script_path, mqsystem):
    self.script_path = script_path
    self.mqsystem = mqsystem
  def run(self):
    MQSystem = self.mqsystem
    print("# exec script: " + self.script_path)
    execfile(self.script_path)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("usage: {s} [-o OUTPUT.mqo] INPUT.mqo SCRIPT.py [SCRIPT2.py ...]".format(s = sys.argv[0]))
    exit(1)
  src_mqo_name = "in.mqo"
  dst_mqo_name = "out.mqo"
  scripts = []
  it = iter(sys.argv[1:])
  for f in it:
    if f == '-o' :
      dst_mqo_name = it.next()
      continue
    if f == '-i' :
      src_mqo_name = it.next()
      continue
    if f.endswith('.mqo'):
      src_mqo_name = f
    else:
      scripts.append(f)
  mq = MQSystemClass(src_mqo_name)
  for s in scripts:
    Script(s, mq).run()
  mq.mqo_saveFile(dst_mqo_name)
