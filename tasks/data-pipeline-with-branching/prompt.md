# Automated Data Pipeline with Conditional Branching and Error Recovery

## Prompt

You are tasked with building an automated data pipeline for a small company. The pipeline must:

1. **Download a CSV file from a given URL.**
2. **Validate the CSV file:**
   - If the file is missing required columns, log an error and halt.
   - If the file is valid, continue.
3. **Process the data:**
   - If a column "status" exists, filter rows where status is "active".
   - If not, process all rows.
4. **Generate two reports:**
   - A summary report (total rows, active rows, etc.)
   - A detailed report (all processed rows, with calculated fields)
5. **If any step fails, attempt to recover:**
   - If download fails, retry up to 3 times.
   - If validation fails, notify the user and stop.
   - If processing fails, log the error and skip to report generation with available data.
6. **At the end, output a log of all actions and errors.**

### Requirements
- Each step should be modular and only run if its prerequisites are met.
- The pipeline should be able to resume from the last successful step if interrupted.
- The code should be able to explain, at any point, which steps are completed, which are pending, and why.

---

**This task is designed to test multi-step reasoning, dependency tracking, error recovery, and reflection capabilities.** 