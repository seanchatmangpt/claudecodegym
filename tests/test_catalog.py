from claudecodegym.catalog import Catalog

def test_official_index_lock_is_nontrivial_and_unique():
    c=Catalog(); docs=c.documents(); assert len(docs)==187; assert len({d.url for d in docs})==187; assert len(c.index_sha256)==64

def test_tool_surface_is_source_locked_and_partitioned():
    tools=Catalog().tools(); assert len(tools)==44; assert {t.consequence for t in tools}=={"READ","DO"}; assert len({t.name for t in tools})==44
