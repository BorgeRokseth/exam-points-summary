import pandas as pd
import yaml
import math

def format_score(score):
    return int(score) if isinstance(score, (int, float)) and score == int(score) else score

def generate_begrunnelse_for_candidate(csv_file, grading_yaml, candidate_id):
    # Load CSV
    df = pd.read_csv(csv_file)
    # Load grading scheme
    with open(grading_yaml, "r") as f:
        grading_config = yaml.safe_load(f)
    grading_type = grading_config.get("grading_type", {})

    # Filter for candidate
    candidate_df = df[df["CandidateExternalId"] == candidate_id]

    if candidate_df.empty:
        return f"No data found for CandidateExternalId: {candidate_id}"

    texts = [f"You received the following points:"]
    for _, row in candidate_df.iterrows():
        task_no = str(int(row["QuestionNo"]))  # convert to int first to avoid decimals like 1.0, then to string
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


# Example usage:
csv_file = "data/result_export_775807818_300876129_2025-06-17.scores.csv"  # replace with your actual file
grading_yaml = "grading_scheme.yaml"
candidate_id = 10304  # replace with the actual CandidateExternalId you want

justification = generate_begrunnelse_for_candidate(csv_file, grading_yaml, candidate_id)
print(justification)