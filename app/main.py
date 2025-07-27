# Step 1: Basic scaffold
# This is the main entry point for Challenge 1B.
# We'll build it up step-by-step from this foundation.

import os
import json
from datetime import datetime

# These will be implemented next
from pdf_segmenter import extract_sections_from_pdf
from ranker import rank_sections
from extractor import extract_refined_snippets
from output_formatter import format_output



def run_pipeline(input_dir, persona, job_to_be_done, output_path):
    # Step 1: Gather all PDFs
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    pdf_paths = [os.path.join(input_dir, f) for f in pdf_files]

    # Step 2: Extract sections from all PDFs
    all_sections = []
    for path in pdf_paths:
        sections = extract_sections_from_pdf(path)
        all_sections.extend(sections)

    # Step 3: Rank the sections by semantic relevance
    ranked_sections = rank_sections(all_sections, persona, job_to_be_done)

    # Step 4: Extract refined sub-section snippets from top-ranked sections
    refined = extract_refined_snippets(ranked_sections, persona, job_to_be_done, top_n=3)

    # Step 5: Format everything into the final output
    result_json = format_output(
        input_documents=pdf_files,
        persona=persona,
        job=job_to_be_done,
        ranked_sections=ranked_sections,
        refined_snippets=refined,
        timestamp=datetime.utcnow().isoformat()
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_json, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Folder with PDF files")
    parser.add_argument("--persona", required=True, help="Persona description")
    parser.add_argument("--job", required=True, help="Job-to-be-done description")
    parser.add_argument("--output_file", default="challenge1b_output.json")
    args = parser.parse_args()

    run_pipeline(args.input_dir, args.persona, args.job, args.output_file)
