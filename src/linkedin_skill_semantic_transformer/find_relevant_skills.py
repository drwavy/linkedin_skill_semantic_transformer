from sentence_transformers import SentenceTransformer, util # type: ignore
import torch

# Global variables initialized by initialize_model()
skills_list: list[str] = []
model: SentenceTransformer | None = None
skill_embeddings: torch.Tensor | None = None

def initialize_model() -> None:
    """Load skills, initialize model, and compute embeddings."""
    global skills_list, model, skill_embeddings
    
    with open('linkedin_skills.txt', 'r', encoding='utf-8') as f:
        skills_list = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(skills_list)} skills.")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Loading model, encoding skills database. This may take a moment...")
    skill_embeddings = model.encode(skills_list, convert_to_tensor=True) # type: ignore

def find_relevant_skills(certification_name: str, top_k: int = 10) -> None:
    """Find and display the top k matching skills for a given query."""
    if model is None or skill_embeddings is None:
        raise RuntimeError("Model not initialized. Call initialize_model() first.")
    
    query_embedding = model.encode(certification_name, convert_to_tensor=True) # type: ignore

    # Compute cosine similarity
    cos_scores = util.cos_sim(query_embedding, skill_embeddings)[0] # type: ignore

    # Find the top_k results
    top_results = torch.topk(cos_scores, k=top_k)

    print(f"\n--- Best matches for '{certification_name}' ---")
    for score, idx in zip(top_results[0], top_results[1]):
        idx_val = int(idx.item())
        print(f"{skills_list[idx_val]} (Score: {score:.4f})")

def start_interactive_search() -> None:
    """Start the interactive search loop."""
    while True:
        user_query = input("\nEnter certification name or 'q' for quit: ")
        if user_query.lower() == 'q':
            break
        find_relevant_skills(user_query)

if __name__ == "__main__":
    start_interactive_search()