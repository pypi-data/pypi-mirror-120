from unswamp.objects.checks.column.ColumnFunctionCheck import ColumnFunctionCheck


class CheckColumnStringMatchStrfFormat(ColumnFunctionCheck):
    def __init__(self, id, column, format, active=True, meta_data=None):
        function_key = "column_check_match_strftime_format"
        expectation_key = "result_eq_expectation"
        arguments = {"column": column,
                     "format": format,
                     "expectation" : True}

        ColumnFunctionCheck.__init__(
            self, id, function_key, expectation_key, arguments, active, meta_data)
