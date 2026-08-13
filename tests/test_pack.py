from pathlib import Path
from rdflib import Graph, Namespace, RDF

ROOT=Path(__file__).parents[1]; PACK=ROOT/"ggen/claudecode-gymact-pack"
SOSA=Namespace("http://www.w3.org/ns/sosa/"); DCT=Namespace("http://purl.org/dc/terms/")

def graph(): return Graph().parse(PACK/"ontology.ttl",format="turtle")

def test_pack_capabilities_have_required_single_values_and_classes():
    g=graph(); caps=list(g.subjects(RDF.type,SOSA.Procedure)); assert len(caps)==5
    for cap in caps:
        titles=list(g.objects(cap,DCT.title)); types=list(g.objects(cap,DCT.type)); assert len(titles)==1; assert len(types)==1; assert str(types[0]) in {"urn:gymact:consequence:read","urn:gymact:consequence:do"}

def test_ggen_gate_queries_return_zero_violations():
    g=graph()
    for path in sorted((PACK/"gates").glob("*.rq")):
        assert list(g.query(path.read_text()))==[], path.name

def test_shape_copy_digest_is_bound_to_upstream_commit():
    import hashlib
    data=(PACK/"shapes/profile.shacl.ttl").read_bytes(); digest=hashlib.sha256(data).hexdigest(); lock=(PACK/"shapes/DIGESTS.txt").read_text(); assert digest in lock; assert "5a40c8f402aeb14699e216e17b2ef7aae9f0bc8f" in lock
