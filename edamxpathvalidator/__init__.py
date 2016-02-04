#!/usr/bin/env python
"""EDAM XPath validator module script"""

import argparse
from lxml import etree

#parsing and declaring namespaces...
EDAM_NS = {'owl' : 'http://www.w3.org/2002/07/owl#',
           'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           'rdfs':"http://www.w3.org/2000/01/rdf-schema#",
           'oboInOwl': "http://www.geneontology.org/formats/oboInOwl#"}

def report(element, targets, error):
    """ report a consistency error between a source and a target concept """
    source_label = element.xpath('rdfs:label/text()', namespaces=EDAM_NS)[0]
    source_id = element.xpath('@rdf:about', namespaces=EDAM_NS)[0]
    target_id = targets[0].xpath('@rdf:about', namespaces=EDAM_NS)[0]
    try:
        target_label = targets[0].xpath('rdfs:label/text()', namespaces=EDAM_NS)[0]
    except:
        target_label = "no label"
    print("Error: " + error + \
          " - '" + source_label + \
          "' (" + source_id + ") -> '" + \
          target_label + "' (" + target_id + ")")

def check_file(file_path):
    """ check the consistency of the EDAM file specified by a filesystem path """
    doc = etree.parse(file_path)
    #listing obsolete terms pointing to other obsolete terms as consider or replacement...
    els = doc.xpath("//owl:Class[owl:deprecated='true']", namespaces=EDAM_NS)
    for element in els:
        consider_ids = element.xpath('oboInOwl:consider/@rdf:resource', namespaces=EDAM_NS)
        if consider_ids:
            consider_id = consider_ids[0]
            targets = doc.xpath("//owl:Class[@rdf:about='" +\
                                consider_id+"' and owl:deprecated='true']", \
                                namespaces=EDAM_NS)
            if targets:
                report(element, targets, "obsolete consider obsolete")
        replaced_by_ids = element.xpath('oboInOwl:replacedBy/@rdf:resource', namespaces=EDAM_NS)
        if replaced_by_ids:
            replaced_by_id = replaced_by_ids[0]
            targets = doc.xpath("//owl:Class[@rdf:about='" +\
                                replaced_by_id + "' and owl:deprecated='true']",\
                                namespaces=EDAM_NS)
            if targets:
                report(element, targets, "obsolete replacedBy obsolete")
                source_id = element.xpath('@rdf:about', namespaces=EDAM_NS)[0]
                source_axis = source_id.split('/').pop().split('_')[0]
                target_axis = replaced_by_id.split('/').pop().split('_')[0]
                if source_axis != target_axis:
                    targets = doc.xpath("//owl:Class[@rdf:about='" +\
                                        replaced_by_id + "']",\
                                        namespaces=EDAM_NS)
                    report(element, targets, "obsolete '" + source_axis +\
                           "' term replacedBy '" + target_axis + "' term")

def main():
    """ function called by the module script """
    parser = argparse.ArgumentParser(description='Validate EDAM OWL/XML file')
    parser.add_argument('file', help="EDAM file")
    args = parser.parse_args()
    if args.file:
        check_file(args.file)

if __name__ == '__main__':
    main()
