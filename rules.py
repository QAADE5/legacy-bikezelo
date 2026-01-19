"""
Great Expectations rules for the orders table.

orders schema:
row_id, timestamp, customer_id, order_amount, status

Timestamp format: 2026-03-05T23:54:31
"""
import great_expectations as gx


def get_failures(suite):
    """FAIL rules - rows that break these turn RED on the dashboard."""

    # Every order must be linked to a customer
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
    )

    # Negative amounts mean corrupted data; very high amounts are likely entry errors
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="order_amount",
            min_value=0,
            max_value=999.99
        )
    )

    # Status must be one the downstream pipeline knows how to process
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="status",
            value_set=["NEW", "PAID", "SHIPPED", "REFUNDED"]
        )
    )

    # A valid ID like CUST1234 is 8 characters
    suite.add_expectation(
        gx.expectations.ExpectColumnValueLengthsToBeBetween(
            column="customer_id",
            min_value=4,
            max_value=12
        )
    )

    return suite


def get_warnings(suite):
    """WARNING rules - rows that break these turn AMBER on the dashboard."""

    # Malformed timestamps don't stop the pipeline, but break anything that sorts or filters by time
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column="timestamp",
            regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"
        )
    )

    return suite
