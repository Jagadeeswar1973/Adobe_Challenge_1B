def format_output(input_documents, persona, job, ranked_sections, refined_snippets, timestamp):
    output = {
        "metadata": {
            "input_documents": input_documents,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": timestamp
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    for sec in ranked_sections:
        output["extracted_sections"].append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "page_number": sec["page_number"],
            "importance_rank": sec["importance_rank"]
        })

    for ref in refined_snippets:
        output["sub_section_analysis"].append({
            "document": ref["document"],
            "section_title": ref["section_title"],
            "refined_text": ref["refined_text"],
            "page_number": ref["page_number"]
        })

    return output
