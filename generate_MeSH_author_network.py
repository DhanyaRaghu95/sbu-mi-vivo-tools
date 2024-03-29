"""Connect researchers of a site to their MeSH aligned UMLS CUIs"""

from pyTripleSimple import SimpleTripleStore
from pyTripleSimple import ExtractGraphFromSimpleTripleStore
import sys

def main(vivo_abox_dump, vivo_aligned_mesh):
    fa = open(vivo_abox_dump,"r")
    fm = open(vivo_aligned_mesh)

    ts = SimpleTripleStore()

    print("Loading triples")
    ts.load_ntriples(fa)
    fa.close()

    ts.load_ntriples(fm)
    fm.close()
    print("Generating research network")

    graph_obj = ExtractGraphFromSimpleTripleStore(ts)
    graph_obj.register_label()

    base_patterns = [
        ('ar1','ds','sbj'),
        ("c1","p2","ar1"),
        ("a1","p1","c1"),
        ("a1","t","f")]

    base_restrictions = [("p1","in",["<http://vivoweb.org/ontology/core#authorInAuthorship>"]),
        ("p2", "in", ["<http://vivoweb.org/ontology/core#linkedInformationResource>"]),
        ("ds", "in", ["<http://purl.org/dc/elements/1.1/subject>"]),
        ("t","in", ["<http://vivoweb.org/ontology/core#hasMemberRole>"])]

    graph_obj.add_pattern_for_links(base_patterns,base_restrictions,["sbj","a1"],"shared_subjects")

    print("Writing results to a file")

    graphml_file_name = vivo_abox_dump + ".network.msr.graphml"
    fo = open(graphml_file_name,"w")
    graph_obj.translate_into_graphml_file(fo)
    fo.close()

if __name__ == '__main__':
    vivo_abox_dump = sys.argv[1]
    vivo_aligned_mesh = sys.argv[2]
    main(vivo_abox_dump,vivo_aligned_mesh)
