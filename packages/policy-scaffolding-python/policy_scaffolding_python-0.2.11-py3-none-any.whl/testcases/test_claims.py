# Example script that

# import case
from testcases.testcase import InsightEngineTestCase, load_test_case
from testcases.serialization import toJSON

tc1 = load_test_case("testcases/TestInputs/TestNode200_No.json")

tc1.insight_engine_request.claim.id = "1"

tc1.save("tc1-new.json")
