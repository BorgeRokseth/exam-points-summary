# Exam Points Summary Tool

This tool helps generate justifications ("begrunnelser") for student exam grades based on a CSV export from "Inspera". It supports both command-line and GUI usage.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/exam-points-summary.git
   cd exam-points-summary
   ```

2. **Install dependencies:**

   This tool requires `pandas` and `pyyaml`:

   ```bash
   pip install pandas pyyaml
   ```

3. **Prepare your files:**

   - Download exam results as CSV from inspera
   - Place your exam results CSV file in the repo directory and rename it `grades.csv` 
   - Update `grading_scheme.yaml` to suit your format, making sure the keys match the `QuestionNo` column in the CSV.

---

## Usage

Run:

```bash
python justify.py
```

You'll be prompted to enter a `CandidateExternalId`, and a justification will be printed for copy-pasting. You can then paste this directly in the appropriate textbox in Inspera.

It is highly recommended to double check correctness before submitting a justification

## License

MIT License
