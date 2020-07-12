from cement import Controller, ex
from bs4 import BeautifulSoup
import os
import re
import sys
from lxml import etree as et
import yaml


class Formats(Controller):
    class Meta:
        label = 'formats'
        stacked_type = 'embedded'
        stacked_on = 'base'

    outline_xml = et.ElementTree()
    outline_xml._setroot(et.Element('outline'))

    @ex(
        help='convert to another format',
        arguments=[
            (['input_file_path'],
            {'help': 'the input file path',
             'action': 'store'}),
            # (['output_format'],
            #  {'help': 'the output format',
            #   'action': 'store',
            #   'choices': ['tsv_traverse']}),
        ]
    )
    def convert(self):
        """Convert the given outline to a set of flashcards."""

        input_file_path = self.app.pargs.input_file_path
        infile = open(input_file_path)
        source = infile.read()
        infile.close()

        flashcards = ''

        format = self.detect_format(input_file_path)
        if format == 'yaml':
            flashcards = self.convert_yaml(input_file_path, source)
        elif format == 'html':
            flashcards = self.convert_html(input_file_path, source)

        root_xml = self.outline_xml.getroot()
        self.xml2flashcards(root_xml, input_file_path)

    def detect_format(self, input_file_path):
        """Detect the format of the input file."""

        format = ''
        if re.search('\.yml', input_file_path, re.X | re.M | re.S):
            format = 'yaml'
        elif re.search('\.htm', input_file_path, re.X | re.M | re.S):
            format = 'html'

        return format

    def convert_yaml(self, input_file_path, source):
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
                    last_child_xml = et.Element('li', {'key': key})
                    parent_xml.append(last_child_xml)
                    target_xml = last_child_xml

                child_yaml = elt_yaml[key]

                self.process_yaml(target_xml, child_yaml)

        elif type(elt_yaml) == type(''):
            parent_xml.text = elt_yaml

        return parent_xml

    def convert_html(self, input_file_path, source):
        """Convert the source text from HTML to the flashcards format."""

        flaschards = ''

        return flashcards

    def xml2flashcards(self, root, input_file_path):
        """Convert the outline XML to the flaschards format."""

        helpers_dir_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)),
            'helpers')
        flashcards_xsl_path = os.path.join(helpers_dir_path,
            'xml2flashcards.xsl')
        xml_path = re.sub('\.[^\.]+\Z', '.xml', input_file_path)
        flashcards_path = re.sub('\.[^\.]+\Z', '.txt', input_file_path)

        xml_string = et.tostring(
            root,
            method='xml',
            encoding='unicode',
            # pretty_print = True
        )

        xml_file = open(xml_path, 'w', encoding='utf-8')
        xml_file.write(xml_string)
        xml_file.close()

        options = r'-xsl:"' + flashcards_xsl_path + r'" -s:"' \
                  + xml_path + r'" -o:"' + flashcards_path + '"'
        self.run_stylesheet(options)

        return

    def run_stylesheet(self, options):
        """."""

        command = 'java net.sf.saxon.Transform ' + options
        os.system(command)
