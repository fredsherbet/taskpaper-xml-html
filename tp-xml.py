#!/usr/bin/python

import sys
import argparse
import re
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

class ProjectOrTask(Element):
    def __init__(self, parentOrSibling, pot, name, indent):
        Element.__init__(self, pot)
        self.set('name', name)
        self.indent = indent
        self.notes = None
        parent = parentOrSibling
        while parent is not None:
            if parent.indent < indent:
                parent.addProject(self)
                break
            parent = parent.parent
        self.parent = parent

    def addTask(self, task):
        trace("addTask(%s, %s)" % (self.get('name'), task.get('name')))
        self.append(task)

    def addProject(self, proj):
        trace("addProject(%s, %s)" % (self.get('name'), proj.get('name')))
        self.append(proj)

    def addTextChild(self, name, text):
        ele = Element(name)
        ele.text = text
        self.append(ele)
        return ele

    def addTag(self, tag):
        self.addTextChild('tag', tag)

    def addNotes(self, notes):
        if self.notes is None:
            self.notes = self.addTextChild('notes', notes)
        else:
            self.notes.text = "%s\n%s" % (self.notes.text, notes)

    def markdownNotes(self):
        if self.notes is not None:
            self.notes.text = markdown.markdown(self.notes.text)

class Project(ProjectOrTask):
    def __init__(self, parentOrSibling, name, indent):
        ProjectOrTask.__init__(self, parentOrSibling, 'project', name, indent)

class Task(ProjectOrTask):
    def __init__(self, parentOrSibling, text, indent):
        ProjectOrTask.__init__(self, parentOrSibling, 'task', text, indent)

#def prettyprint(xml):
#    rough_string = tostring(xml, 'utf-8')
#    reparsed = minidom.parseString(rough_string)
#    return reparsed.toprettyxml(indent="  ")

def prettyprint(xml):
    rough_string = tostring(xml, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml()
    fix = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)')
    return re.sub(fix, '', pretty)

def trace(text):
    if traceEnabled:
        sys.stderr.write('%s\n' % text)

tagre = ' @[^ (]*(?:\([^)]*\))?'

def main(inputfile = None, outfile = None, markdown = False):
    root = Project(None, 'root', -1)
    current = root
    inNotes = False

    if inputfile is not None:
        inf = open(inputfile, 'r')
        trace("Opened %s" % inputfile)
    else:
        inf = sys.stdin

    for line in inf:
        trace("Reading line '%s'" % line)
        unindentedline = line.lstrip()
        indent = len(line) - len(unindentedline)
        notags = re.sub(tagre, '', line).strip()
        trace("notags: '%s'" % notags)
        tags = [tag[2:].strip() for tag in re.findall(tagre, line)]
        trace("tags: %s" % str(tags))
        if notags.startswith('-'):
            taskname = notags.lstrip('- ')
            trace("New task: '%s'" % taskname)
            if markdown:
                trace("markdown previous object's notes")
                current.markdownNotes()
            current = Task(current, taskname, indent)
            inNotes = False
        elif notags.endswith(':'):
            projname = notags.rstrip(': ')
            trace("New project: '%s'" % projname)
            if markdown:
                trace("markdown previous object's notes")
                current.markdownNotes()
            current = Project(current, projname, indent)
            inNotes = False
        elif (inNotes) or (len(line.strip()) > 0):
            if indent >= current.indent:
                notesline = line[indent:].rstrip()
            else:
                notesline = line.strip()
            trace("Notes: '%s'" % notesline)
            inNotes = True
            current.addNotes(notesline)
            tags = []

        # Add tags
        for tag in tags:
            current.addTag(tag)

    if outfile is not None:
        outf = open(outfile, 'w')
    else:
        outf = sys.stdout
    outf.write(prettyprint(root))

parser = argparse.ArgumentParser(description="Turn taskpaper text file into XML")
parser.add_argument("-i", "--input", action="store", dest="infile")
parser.add_argument("-o", "--output", action="store", dest="outfile")
parser.add_argument("-m", "--markdown", action="store_true", dest="markdown")
parser.add_argument("-d", "--debug", action="store_true", dest="debug")

results = parser.parse_args()

if results.debug:
    traceEnabled = True
else:
    traceEnabled = False

if results.markdown:
    trace("Importing markdown")
    try:
        import markdown
    except:
        sys.stderr.write("To use markdown, install the markdown module, from http://pypi.python.org/pypi/Markdown/")
        results.markdown = False

main(results.infile, results.outfile, results.markdown)

