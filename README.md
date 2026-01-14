# LinkedIn Skills Semantic Search

A Python-based semantic search tool that performs intelligent searches on a database of LinkedIn skills. Instead of relying on simple keyword matching, this project uses a pre-trained Sentence Transformer model to understand the meaning and context behind a query. This enables discovery of relevant skills even when the exact wording differs from the database.

The tool automates dataset retrieval, utilizes the `all-MiniLM-L6-v2` model to generate vector embeddings, and calculates cosine similarity to return the top 10 most relevant matches for any input.


## Semantic Search vs. Keyword Matching

Why use an AI model for a simple search? 

If you rely on simple string matching, you will miss obvious connections.

If you search for the "AWS Certified Solutions Architect" certification, a standard keyword search will miss "Cloud Computing" because the word "Cloud" does not appear in the certification title.

Semantic Search (Vector Embeddings) solves this by converting text into numerical vectors. It understands that "AWS" and "Cloud Computing" are conceptually identical in this context.


### Why this approach wins:

This approach wins because of conceptual matching, synonym recognition, and contextual granularity. If you query "Certified Ethical Hacker," the tool can identify related terms like "Penetration Testing" and "Network Security" as top matches, even though they share no common words. Effective recognition handles acronyms and industry jargon. 

The idea was to capture the weight behind a qualification, which is often more important than focusing solely on the specific keywords used.

---

### The Model

The project uses the `all-MiniLM-L6-v2` model. It's designed to map sentences and paragraphs to a 384-dimensional dense vector space and is specifically optimized for semantic search tasks.

### Cosine Similarity

To find matches, the query and every skill in the database are treated as vectors in multi-dimensional space. The relevance score is calculated using the Cosine Similarity of the angle between them:

$$\text{similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

Where:
* $\mathbf{A}$ is the vector of your query.
* $\mathbf{B}$ is the vector of a specific skill.
* A score of **1.0** implies identical meaning, while **0.0** implies no semantic relationship.

---

## Installation

### Prerequisites
- Python 3.13 or higher
- pip or poetry package manager

### Using pip

```bash
pip install -r requirements.txt
```

### Using poetry

```bash
poetry install
```

### Running the Application

```bash
cd src
python -m linkedin_skill_semantic_transformer.main
```

---

## Workflow

1. Data Check: The script checks for `linkedin_skills.txt`. If missing, it downloads it automatically.
2. Initialization: The AI model initializes. 
   
   *Note: This takes a moment as it computes embeddings for the entire skills list*.

3. Search: Enter a certification or skill name when prompted.
4. Results: View the top 10 matching skills with their similarity scores (0 to 1).

Example Output:

```text
Enter certification name or 'q' for quit: AWS Certified Solutions Architect

--- Best matches for 'AWS Certified Solutions Architect' ---
Amazon Web Services (AWS) (Score: 0.8123)
Cloud Computing (Score: 0.7456)
Solution Architecture (Score: 0.7120)
...

```

---

## Documentation

**1. `main.py`**

Role: Entry point & Orchestrator.

Manages the application flow and ensures data prerequisites are met before loading machine learning libraries.

* `main() -> None`
* Checks for the existence of `linkedin_skills.txt`.
* Calls `download_skills()` from `get_skills_list` if the file is missing.
* Imports `find_relevant_skills` inside a `try/except` block to prevent loading heavy ML libraries until data presence is confirmed.
* Initiates the interactive search loop.


**2. `download_skills.py`**

Role: Data Acquisition.

Handles fetching the raw dataset from a remote repository.

* Constants:
  * `URL`: Points to the raw content of the GitHub repository hosting the skills list.
  * `FILENAME`: Defaults to `linkedin_skills.txt`.
* `download_skills()`
  * Uses `urllib` to fetch data (requires no external `requests` dependency).
  * Writes content to disk with `utf-8` encoding.
  * Includes error handling for network issues (`URLError`) and file permissions (`OSError`).



**1. `find_relevant_skills.py`**


---

## Project Structure

```
.
├── src/
│   └── linkedin_skill_semantic_transformer/
│       ├── __init__.py
│       ├── main.py                 # Entry point
│       ├── download_skills.py      # Data acquisition module
│       └── find_relevant_skills.py # Core ML engine
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures and configuration
│   ├── test_main.py                # Tests for main module
│   ├── test_download_skills.py     # Tests for download module
│   └── test_find_relevant_skills.py # Tests for search module
├── pyproject.toml                   # Project configuration and dependencies
├── pytest.ini                       # Pytest configuration
├── .gitignore                       # Git ignore file
├── README.md                        # This file
└── LICENSE                          # MIT License

```

---

## Testing

Run the test suite using pytest:

```bash
pytest tests/ -v
```

For coverage reports:

```bash
pytest tests/ --cov=src/linkedin_skill_semantic_transformer --cov-report=html
```

---

## Development

### Setting up the development environment

```bash
poetry install --with dev
```

### Running linters and formatters

The project supports standard Python tools for code quality:
- Use `black` for code formatting
- Use `flake8` or `pylint` for linting
- Use `mypy` for type checking

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

Created by [Omair Khattak](https://omairkhattak.com)

---

## Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) for the semantic search model
- [LinkedIn Skills Dataset](https://github.com/maciejszewczyk/linkedin-skills) for the skills database
Role: Core Logic / ML Engine.

Handles the loading of the Neural Network and the computation of vector similarity.

Global Execution:
* Upon import, reads `linkedin_skills.txt` into memory.
* Initializes `SentenceTransformer('all-MiniLM-L6-v2')`.
* `skill_embeddings`: Pre-computes embeddings for the entire list of skills. This is the most computationally expensive step but ensures subsequent searches are instant.

`find_relevant_skills(certification_name: str, top_k: int = 10) -> None`
* Input: User query string.
* Process:
  1. Encodes the user query into a vector tensor.
  2. Calculates Cosine Similarity between the query vector and the database using `util.cos_sim`.
  3. Extracts the top `top_k` results using `torch.topk`.
* Output: Prints matching skills alongside similarity scores.

`start_interactive_search() -> None`
* A simple `while True` loop that accepts user input and calls the search function until the user types 'q'.