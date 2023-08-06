from unswamp.objects.checks.column.ColumnFunctionCheck import ColumnFunctionCheck


class CheckColumnDateutilParsable(ColumnFunctionCheck):
    def __init__(self, id, column, active=True, meta_data=None):
        function_key = "column_check_dateutil_parseable"
        expectation_key = "result_eq_expectation"
        arguments = {"column": column,
                     "expectation" : True}

        ColumnFunctionCheck.__init__(
            self, id, function_key, expectation_key, arguments, active, meta_data)
