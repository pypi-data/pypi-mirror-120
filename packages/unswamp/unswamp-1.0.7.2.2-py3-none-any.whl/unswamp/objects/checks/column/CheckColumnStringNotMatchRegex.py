from unswamp.objects.checks.column.ColumnFunctionCheck import ColumnFunctionCheck


class CheckColumnStringNotMatchRegex(ColumnFunctionCheck):
    def __init__(self, id, column, regex, active=True, meta_data=None):
        function_key = "column_check_not_match_regex"
        expectation_key = "result_eq_expectation"
        arguments = {"column": column,
                     "regex": regex,
                     "expectation" : True}

        ColumnFunctionCheck.__init__(
            self, id, function_key, expectation_key, arguments, active, meta_data)
