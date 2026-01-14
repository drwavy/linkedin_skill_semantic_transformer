# Quick Reference

## Project Overview
**LinkedIn Skills Semantic Transformer** - A Python tool that uses semantic search (AI embeddings) to find related LinkedIn skills based on natural language queries.

## Key Files Reference

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `LICENSE` | MIT License |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `pyproject.toml` | Project configuration and dependencies |
| `pytest.ini` | Testing configuration |
| `.gitignore` | Git ignore rules |

## Quick Commands

### Installation
```bash
# Using pip
pip install -r requirements.txt

# Using poetry
poetry install
```

### Running the Application
```bash
cd src
python -m linkedin_skill_semantic_transformer.main
```

### Running Tests
```bash
pytest tests/ -v
```

### Installation with Development Dependencies
```bash
poetry install --with dev
```

## Project Structure
```
src/linkedin_skill_semantic_transformer/
├── main.py                 # Entry point
├── download_skills.py      # Data fetching
└── find_relevant_skills.py # Semantic search engine

tests/
├── test_main.py
├── test_download_skills.py
└── test_find_relevant_skills.py
```

## How It Works

1. **Data Acquisition**: `download_skills.py` fetches the LinkedIn skills database
2. **Model Loading**: `find_relevant_skills.py` loads the Sentence Transformer model
3. **Embedding Generation**: Creates vector embeddings for all skills
4. **Semantic Search**: User queries are matched against skills using cosine similarity
5. **Results**: Top 10 most relevant matches are displayed with similarity scores

## Technology Stack

- **Python 3.13+**
- **sentence-transformers** - Semantic search model
- **torch** - Deep learning framework
- **numpy** - Numerical computing
- **scikit-learn** - ML utilities
- **pytest** - Testing framework

## Model Details

- **Model**: `all-MiniLM-L6-v2`
- **Vector Dimension**: 384
- **Similarity Metric**: Cosine Similarity
- **Score Range**: 0.0 (no relation) to 1.0 (identical)

## Future Enhancements

- [ ] Add GitHub Actions for CI/CD
- [ ] Add code coverage tracking
- [ ] Add type checking (mypy) to pipeline
- [ ] Add API endpoint (FastAPI)
- [ ] Add web UI (Streamlit)
- [ ] Support for multiple languages
- [ ] Custom model fine-tuning

## Support & Questions

- Check the README.md for detailed information
- Review CONTRIBUTING.md for contribution guidelines
- Open an issue on GitHub for bugs or feature requests

---
Last Updated: January 14, 2025
