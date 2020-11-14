import unittest
import importlib
import logging
import json
from aws_xray_sdk.core import xray_recorder

logger = logging.getLogger()
xray_recorder.configure(context_missing="LOG_ERROR")
# function = importlib.import_module(lambda_function)

xray_recorder.begin_segment("test_init")
function = __import__("lambda_function")
handler = function.lambda_handler
xray_recorder.end_segment()


class TestFunction(unittest.TestCase):
    def test_function(self):
        xray_recorder.begin_segment("test_function")
        file = open("event.json", "rb")
        try:
            event = file.read()
            logger.warning("## EVENT")
            context = {"requestid": "1234"}
            result = handler(event, context)
            print(str(result))
            self.assertRegex(json.loads(result)["id"], "cs_test_.*", "Should match")
        finally:
            file.close()
        file.close()
        xray_recorder.end_segment()


if __name__ == "__main__":
    unittest.main()
