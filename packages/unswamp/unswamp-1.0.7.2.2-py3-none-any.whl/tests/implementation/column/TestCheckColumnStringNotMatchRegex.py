from unittest import TestCase
from datetime import datetime
from tests.TestHelpers import TestHelpers
from unswamp.objects.checks import CheckColumnStringNotMatchRegex


class TestCheckColumnStringNotMatchRegex(TestCase):
    def setUp(self):
        key = TestHelpers.random_string()
        column = "Year"
        value = "^[0-9]{5}$"
        active = TestHelpers.random_bool()
        meta_data = {"Date": datetime.today()}
        self.check_pass = CheckColumnStringNotMatchRegex(
            key, column, value, active, meta_data)

        column = "Year"
        value = "^[0-9]{4}$"
        self.check_fail = CheckColumnStringNotMatchRegex(
            key, column, value, active, meta_data)

    def test_run_pass(self):
        check = self.check_pass
        expectation = True
        TestHelpers.test_run(self, check, expectation)

    def test_run_fail(self):
        check = self.check_fail
        expectation = False
        TestHelpers.test_run(self, check, expectation)
