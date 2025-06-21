# Task: CSV Report Generator

Your task is to create a Python script that reads a CSV file containing sales data, performs some calculations, and generates a formatted text file with a summary report.

## Requirements

1.  The input data is located at `tasks/csv-report-generator/initial_code/data.csv`. The file has the following columns: `product_id`, `price`, and `quantity`.
2.  Your script should be created at `tasks/csv-report-generator/solution/report_generator.py`.
3.  The script must calculate:
    -   The average price of all products.
    -   The total revenue from all sales (sum of `price * quantity` for each product).
4.  The script must generate a report file at `tasks/csv-report-generator/solution/report.txt`.
5.  The report must follow this format exactly, with values rounded to two decimal places:

    ```
    Sales Report
    ============
    Average Price: $12.81
    Total Revenue: $194.00
    ```

## Verification

To verify your solution, run the tests located in the verifier directory.

Execute the following command from the root of the `swe-basic-bench` directory:
`pytest tasks/csv-report-generator/verifier/test_report.py`

Your goal is to make all the tests pass. 