#!/usr/bin/env ruby
# coding: utf-8

lines = File.readlines('metaseq_template.py').each

open('metaseq.py', 'wb'){|f|
  skip = false
  props = []
  lines.each{|line|
    if line=~/^(\s*)#!!\s*(\w+)\s*(.*)/
      f.write(line)
      cmd = $2
      params = $3
      props = [] if cmd == 'init'
      skip = false if cmd == 'end'
      skip = true if cmd.end_with?('_begin') || cmd.start_with?('begin_')
      if cmd == 'attr'
        props << params.split(/\s+/)
      elsif cmd == 'vars_begin'
        props.each{|prop|
          if prop[3] == '-'
            f.puts($1 + params.strip() + "._" + prop[2] + " = " + prop[4])
          else
            f.puts($1 + params.strip() + "._" + prop[2] + " = self.attr_" + prop[1] + "('" + prop[3] + "'," + prop[4] +")")
          end
        }
      elsif cmd == 'properties_begin'
        props.each{|prop|
          if prop[0].include?('r')
            f.puts($1 + "@property")
            f.puts($1 + "def " + prop[2] + "(self):")
            f.puts($1 + "  return self._" + prop[2])
          end
          if prop[0].include?('w')
            f.puts($1 + "@"+ prop[2] +".setter")
            f.puts($1 + "def " + prop[2] + "(self, v):")
            f.puts($1 + "  self._" + prop[2] + " = v")
            f.puts($1 + "  self._attrs['" + prop[3] + "'] = str(v)") if prop[3] != '-'
          end
          f.puts("")
        }
      elsif cmd == 'begin_struct'
        ind = $1
        fields = params.split(/\s+/)
        f.puts(ind + "def __init__(self, " + fields.join(', ')  + "):")
        fields.each{|field|
          f.puts(ind + "  self.#{field} = #{field}")
        }
        f.puts(ind + "def __str__(self):")
        f.puts(ind + "  return ' '.join([ " + fields.map{|f| "str(self.#{f})"}.join(',') + " ])")
      end
      next
    end
    next if skip
    f.write(line)
  }
}

