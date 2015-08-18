#!/usr/bin/env python
# coding: utf-8
import sys
from metaseq import *

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
    print("usage: {s} SCRIPT.py INPUT.mqo".format(s = sys.argv[0]))
    exit(1)
  src_mqo_name = "in.mqo"
  if len(sys.argv) > 2:
    src_mqo_name = sys.argv[2]
  mq = MQSystemClass(src_mqo_name)
  Script(sys.argv[1], mq).run()
  mq.mqo_saveFile("out.mqo")
