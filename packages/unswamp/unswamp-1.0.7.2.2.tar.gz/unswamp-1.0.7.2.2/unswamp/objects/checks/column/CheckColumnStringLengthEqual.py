from unswamp.objects.checks.column.ColumnFunctionCheck import ColumnFunctionCheck


class CheckColumnStringLengthEqual(ColumnFunctionCheck):
    def __init__(self, id, column, value, active=True, meta_data=None):
        function_key = "column_check_string_length_min_max_tuple"
        expectation_key = "result_tuple_equals"
        arguments = {"column": column,
                     "expectation": value}

        ColumnFunctionCheck.__init__(
            self, id, function_key, expectation_key, arguments, active, meta_data)
