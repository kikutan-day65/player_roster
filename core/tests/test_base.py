class TestBase:
    def assert_expected_fields(self, output, fields):
        for field in fields:
            assert (
                field in output
            ), f"Expected field '{field}' not found. Output fields: {list(output.keys())}"

    def assert_unexpected_fields(self, output, fields):
        for field in fields:
            assert (
                field not in output
            ), f"Unexpected field '{field}' found. Output fields: {list(output.keys())}"
