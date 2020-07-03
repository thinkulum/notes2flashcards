from bs4 import BeautifulSoup
import os
import re
import sys
from lxml import etree as et
import yaml

def main():
    """Run the main body of the module."""

    of = Outline2Flashcards()

    outline_fn = sys.argv[1]
    of.convert(outline_fn)


class Outline2Flashcards:
    """A class for converting outlines to flashcards.

    """

    dir_script = os.getcwd()
    dir_data   = os.path.dirname(dir_script) + '/data'
    dir_in     = dir_data + '/outlines'
    dir_out    = dir_data + '/flashcards'
    dir_xml    = dir_data + '/xml'

    outline_xml = et.ElementTree()
    outline_xml._setroot(et.Element('outline'))

    flashcards = []

    def convert(self, outline_fn):
        """Convert the given outline to a set of flashcards."""

        os.chdir(self.dir_in)
        infile = open(outline_fn)
        source = infile.read()
        infile.close()

        flashcards = ''

        format = self.detect_format(outline_fn)
        if format == 'yaml':
            flashcards = self.convert_yaml(outline_fn, source)
        elif format == 'html':
            flashcards = self.convert_html(outline_fn, source)

        root_xml = self.outline_xml.getroot()
        self.xml2flashcards(root_xml, outline_fn)


    def detect_format(self, outline_fn):
        """Detect the format of the input file."""

        format = ''
        if re.search('\.yml', outline_fn, re.X | re.M | re.S):
            format = 'yaml'
        elif re.search('\.htm', outline_fn, re.X | re.M | re.S):
            format = 'html'

        return format


    def convert_yaml(self, outline_fn, source):
        """Convert the source text from YAML to the flashcards format."""

        outline_yaml = yaml.safe_load(source)

        root_xml = self.outline_xml.getroot()
        self.process_yaml(root_xml, outline_yaml)

        return


    def process_yaml(self, parent_xml, elt_yaml):
        """Add an element from the YAML tree to the XML tree."""

        if type(elt_yaml) == type([]):
            parent_xml.set('list_type', 'ol')
            # last_child_xml = et.Element('ol')
            # parent_xml.append(last_child_xml)
            # parent_xml = last_child_xml

            for child_yaml in elt_yaml:
                last_child_xml = et.Element('li')
                parent_xml.append(last_child_xml)

                self.process_yaml(last_child_xml, child_yaml)

        elif type(elt_yaml) == type({}):
            is_heading = 1

            target_xml = parent_xml

            if len(elt_yaml.keys()) > 1:
                parent_xml.set('list_type', 'ul')
                # last_child_xml = et.Element('ul')
                # parent_xml.append(last_child_xml)
                # target_xml = last_child_xml

                is_heading = 0

            for key in elt_yaml.keys():
                if is_heading:
                    parent_xml.set('key', key)

                else:
                    last_child_xml = et.Element('li', { 'key': key })
                    parent_xml.append(last_child_xml)
                    target_xml = last_child_xml

                child_yaml = elt_yaml[key]

                self.process_yaml(target_xml, child_yaml)

        elif type(elt_yaml) == type(''):
            parent_xml.text = elt_yaml

        return parent_xml


    def convert_html(self, outline_fn, source):
        """Convert the source text from HTML to the flashcards format."""

        flaschards = ''

        return flashcards


    def xml2flashcards(self, root, outline_fn):
        """Convert the outline XML to the flaschards format."""

        flashcards_xsl_fn = 'xml2flashcards.xsl'
        xml_fn            = re.sub('\.[^\.]+\Z', '.xml', outline_fn)
        flashcards_fn     = re.sub('\.[^\.]+\Z', '.txt', outline_fn)

        xml_string = et.tostring(
            root, 
            method = 'xml', 
            encoding = 'unicode', 
            # pretty_print = True
        )

        os.chdir(self.dir_xml)
        xml_file = open(xml_fn, 'w', encoding = 'utf-8')
        xml_file.write(xml_string)
        xml_file.close()

        os.chdir(self.dir_script)
        options = r'-xsl:' + flashcards_xsl_fn + r' -s:..\data\xml\\' \
            + xml_fn + r' -o:..\data\flashcards\\' + flashcards_fn
        self.run_stylesheet(options)

        if 0:
            for elt in root.iter('li'):

                breadcrumb = [ self.elt_string(elt) ]
                for ancestor in elt.iterancestors('li'):
                    breadcrumb.insert(0, "'" + self.elt_string(ancestor) + "'")
                if len(breadcrumb) > 0:
                    breadcrumb_string = ' > '.join(breadcrumb)

                # parent

                parent = elt.getparent()
                if parent is not None and parent.tag == 'li':
                    self.add_flashcard('parent', parent, breadcrumb_string)

                # value

                value = self.elt_string(elt)
                if value is not None:
                    self.add_flashcard('value', value, breadcrumb_string)

                # first child

                first_child = elt.find('li')
                if first_child is not None:
                    self.add_flashcard(
                        'first child', 
                        first_child, 
                        breadcrumb_string
                    )

                # previous sibling

                prev_sib = elt.getprevious()
                if prev_sib is not None:
                    self.add_flashcard(
                        'previous sibling', 
                        prev_sib, 
                        breadcrumb_string
                    )

                # next sibling

                next_sib = elt.getnext()
                if next_sib is not None:
                    self.add_flashcard('next sibling', next_sib, breadcrumb_string)

            flashcards = '\n'.join(self.flashcards)

            return flashcards

        return


    def add_flashcard(self, axis, elt, breadcrumb_string):
        """Add an element to self.flashcards based on the axis, XML element, 
           and breadcrumb (the list of ancestor parent values)."""

        q = breadcrumb_string + ' ' + axis
        print('q: ' + str(q))
        a = self.elt_string(elt)
        print('a: ' + str(a))
        self.flashcards.append(q + '\t' + a)

        return


    def elt_string(self, elt):
        """Return the text value of the element, if available, or the key
           attribute."""

        string = ''

        print(type(elt))
        print(type(''))

        if type(elt) == type(''):
            string = elt
        elif len(elt) == 0:
            string = elt.text()
        else:
            string = elt.get('key')

        return string


    def run_stylesheet(self, options):
        """."""

        command = 'java net.sf.saxon.Transform ' + options
        os.system(command)


if __name__ == '__main__':
    main()
