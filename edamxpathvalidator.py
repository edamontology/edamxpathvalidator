#!/usr/bin/env python
from lxml import etree
#parsing and declaring namespaces...
doc = etree.parse('EDAM_1.13_dev.owl')
namespaces = {'owl' : 'http://www.w3.org/2002/07/owl#', 'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#", 'rdfs':"http://www.w3.org/2000/01/rdf-schema#", 'oboInOwl': "http://www.geneontology.org/formats/oboInOwl#"}

def report(el, targets, error):
    sourceLabel = el.xpath('rdfs:label/text()', namespaces=namespaces)[0]
    sourceId = el.xpath('@rdf:about', namespaces=namespaces)[0]
    targetId = targets[0].xpath('@rdf:about', namespaces=namespaces)[0]
    try:
        targetLabel = targets[0].xpath('rdfs:label/text()', namespaces=namespaces)[0]
    except:
        targetLabel = "no label"
    print "Error: " + error + " - '" + sourceLabel + "' (" + sourceId + ") -> '" + targetLabel + "' (" + targetId + ")"
    

#listing obsolete terms pointing to other obsolete terms as consider or replacement...
els = doc.xpath("//owl:Class[owl:deprecated='true']", namespaces=namespaces)
for el in els:
    #try:
        considerIds = el.xpath('oboInOwl:consider/@rdf:resource', namespaces=namespaces)
        if considerIds:
            considerId = considerIds[0]
	    targets = doc.xpath("//owl:Class[@rdf:about='"+considerId+"' and owl:deprecated='true']", namespaces=namespaces)
            if targets:
	        report(el, targets, "obsolete consider obsolete")
        replacedByIds = el.xpath('oboInOwl:replacedBy/@rdf:resource', namespaces=namespaces)
        if replacedByIds:
            replacedById = replacedByIds[0]
	    targets = doc.xpath("//owl:Class[@rdf:about='"+replacedById+"' and owl:deprecated='true']", namespaces=namespaces)
            if targets:
	        report(el, targets,  "obsolete replacedBy obsolete")
            sourceId = el.xpath('@rdf:about', namespaces=namespaces)[0]
            sourceAxis = sourceId.split('/').pop().split('_')[0]
            targetAxis = replacedById.split('/').pop().split('_')[0]
            if sourceAxis != targetAxis:
                targets = doc.xpath("//owl:Class[@rdf:about='"+replacedById+"']", namespaces=namespaces)
                report(el, targets, "obsolete '" + sourceAxis + "' term replacedBy '" + targetAxis + "' term")
    #except Exception as e:
    #    print e
    #    pass
