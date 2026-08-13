from claudecodegym.scenarios import ScenarioFactory

def test_scenario_manufacture_is_deterministic_and_nonvacuous():
    a=ScenarioFactory().all(); b=ScenarioFactory().all(); assert a==b; assert len(a)>500; assert len({x.scenario_id for x in a})==len(a); assert {x.expected for x in a} >= {"EXPECTED_SUCCESS","REFUSED","UNSUPPORTED","BLOCKED"}
