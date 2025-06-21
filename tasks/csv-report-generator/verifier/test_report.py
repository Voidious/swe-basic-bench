import pytest
import re
import os

def get_report_values():
    """Reads the generated report and extracts the values."""
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../solution/report.txt'))
    
    if not os.path.exists(report_path):
        pytest.fail(f"Report file not found at: {report_path}")

    with open(report_path, 'r') as f:
        content = f.read()

    avg_price_match = re.search(r"Average Price: \$([\d\.]+)", content)
    total_revenue_match = re.search(r"Total Revenue: \$([\d\.]+)", content)

    if not avg_price_match:
        pytest.fail("Could not find 'Average Price' in the report.")
    if not total_revenue_match:
        pytest.fail("Could not find 'Total Revenue' in the report.")

    return {
        "avg_price": float(avg_price_match.group(1)),
        "total_revenue": float(total_revenue_match.group(1))
    }

def test_report_exists():
    """Tests if the report file was created."""
    report_path = os.path.join(os.path.dirname(__file__), '../solution/report.txt')
    assert os.path.exists(report_path), "The report file 'report.txt' was not found in the solution directory."

def test_average_price():
    """Tests if the average price in the report is correct."""
    values = get_report_values()
    # Expected: (10.00 + 15.50 + 5.75 + 20.00) / 4 = 12.8125
    expected_avg_price = 12.81
    assert abs(values["avg_price"] - expected_avg_price) < 0.01

def test_total_revenue():
    """Tests if the total revenue in the report is correct."""
    values = get_report_values()
    # Expected: (10*5) + (15.50*3) + (5.75*10) + (20*2) = 50 + 46.5 + 57.5 + 40 = 194.00
    expected_total_revenue = 194.00
    assert abs(values["total_revenue"] - expected_total_revenue) < 0.01 