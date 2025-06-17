import pandas as pd
import yaml
import tkinter as tk
from tkinter import ttk, messagebox

def format_score(score):
    return int(score) if isinstance(score, (int, float)) and score == int(score) else score

def generate_begrunnelse_for_candidate(df, grading_type, candidate_id):
    candidate_df = df[df["CandidateExternalId"].astype(str) == str(candidate_id)]


    if candidate_df.empty:
        return f"No data found for CandidateExternalId: {candidate_id}"

    texts = [f"You received the following points:"]
    for _, row in candidate_df.iterrows():
        task_no = str(int(row["QuestionNo"]))
        grading = grading_type.get(task_no, "unknown")

        manual = row["ManuallyGradedScore"]
        auto = row["AutoGradedScore"]

        question = f"Task {task_no}:"

        if grading == "manual":
            if not pd.isna(manual):
                score_text = f"{format_score(manual)} points (manually graded)"
            else:
                score_text = "No score recorded (manual grading)"
        elif grading == "auto":
            if pd.isna(auto):
                score_text = "No score recorded (auto grading)"
            elif pd.isna(manual) or manual == auto:
                score_text = f"{format_score(auto)} points (automatically graded)"
            else:
                score_text = f"{format_score(manual)} points, manually corrected from {format_score(auto)}"
        else:
            score = manual if not pd.isna(manual) else auto
            if pd.isna(score):
                score_text = "No score recorded"
            else:
                score_text = f"{format_score(score)} points (grading type unknown)"

        texts.append(f"- {question} {score_text}")

    return "\n".join(texts)

# Load data
csv_file = "grades.csv"
grading_yaml = "grading_scheme.yaml"

df = pd.read_csv(csv_file)
with open(grading_yaml, "r") as f:
    grading_config = yaml.safe_load(f)

grading_type = grading_config.get("grading_type", {})

# GUI
def on_generate():
    candidate_id = entry.get().strip()
    if not candidate_id:
        messagebox.showwarning("Missing input", "Please enter a CandidateExternalId.")
        return
    result = generate_begrunnelse_for_candidate(df, grading_type, candidate_id)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)

def copy_to_clipboard():
    text = text_output.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Justification copied to clipboard.")


root = tk.Tk()
root.title("Exam Justification Generator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="NSEW")

ttk.Label(frame, text="CandidateExternalId:").grid(row=0, column=0, sticky="W")
entry = ttk.Entry(frame, width=30)
entry.grid(row=0, column=1, sticky="EW")
entry.focus()

generate_btn = ttk.Button(frame, text="Generate Justification", command=on_generate)
generate_btn.grid(row=0, column=2, padx=5)

text_output = tk.Text(frame, height=15, width=80, wrap="word")
text_output.grid(row=1, column=0, columnspan=3, pady=10, sticky="NSEW")

copy_btn = ttk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_btn.grid(row=2, column=2, sticky="E", pady=(0, 10))

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_output.yview)
scrollbar.grid(row=1, column=3, sticky="NS")
text_output["yscrollcommand"] = scrollbar.set

frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

root.mainloop()
