import os
import sys
from linkedin_skill_semantic_transformer.download_skills import download_skills

def main() -> None:
    filename = "linkedin_skills.txt"

    if not os.path.exists(filename):
        print(f"'{filename}' not found. Downloading skills database...")
        download_skills()
    else:
        print(f"Found '{filename}'.")

    try:
        print("Initializing AI Model...")
        from linkedin_skill_semantic_transformer import find_relevant_skills
        find_relevant_skills.initialize_model()
    except FileNotFoundError:
        print("ERROR: Could not read skills file during import.")
        sys.exit(1)

    find_relevant_skills.start_interactive_search()

if __name__ == "__main__":
    main()