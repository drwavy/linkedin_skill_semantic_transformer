# Testing Documentation

This directory contains comprehensive tests for the LinkedIn Skill Semantic Transformer project.

## Test Structure

### Fixtures (`conftest.py`)
Shared pytest fixtures used across all test modules:
- `sample_skills`: Provides a list of sample LinkedIn skills
- `skills_file`: Temporary file containing sample skills with UTF-8 encoding
- `mock_sentence_transformer`: Mock SentenceTransformer model for testing
- `mock_util`: Mock cosine similarity utility functions
- `downloaded_skills_content`: Sample content that would be downloaded from the remote URL
- `monkeypatch_imports`: Fixture to patch sentence_transformers imports

### Test Modules

#### `test_download_skills.py`
Tests for the `download_skills` module which handles remote file acquisition.

**Coverage:**
- ✅ Successful file download with correct content
- ✅ UTF-8 encoding preservation (including unicode characters)
- ✅ Line counting in status messages
- ✅ Network error handling (URLError)
- ✅ File system error handling (OSError, permission denied)
- ✅ Empty response handling

**Key Tests:**
- `test_successful_download`: Verifies file is created with correct content
- `test_download_preserves_encoding`: Tests unicode character handling
- `test_network_error_handling`: Verifies graceful exit on URLError
- `test_file_system_error_handling`: Verifies handling of permission errors

#### `test_find_relevant_skills.py`
Tests for the `find_relevant_skills` module - the ML core of the application.

**Coverage:**
- ✅ Model initialization and skill loading
- ✅ Embedding computation for entire skill database
- ✅ Semantic search functionality
- ✅ Top-k result filtering
- ✅ Score formatting and display
- ✅ Interactive search loop with user input handling
- ✅ Case-insensitive quit command
- ✅ Edge cases (empty input, whitespace, zero similarity)

**Key Tests:**
- `test_initialize_model_loads_skills`: Verifies skills are loaded into memory
- `test_initialize_model_computes_embeddings`: Confirms embeddings are computed
- `test_find_relevant_skills_not_initialized`: Tests error handling when model isn't initialized
- `test_find_relevant_skills_returns_top_k`: Verifies correct number of results
- `test_start_interactive_search_multiple_queries`: Tests multi-query handling
- `test_start_interactive_search_case_insensitive_quit`: Verifies case-insensitive quit

#### `test_main.py`
Tests for the `main` orchestration module.

**Coverage:**
- ✅ File existence checking
- ✅ Download triggering when file is missing
- ✅ Model initialization
- ✅ Interactive search startup
- ✅ Error handling (FileNotFoundError)
- ✅ Execution order verification
- ✅ Integration testing of full application flow

**Key Tests:**
- `test_main_file_exists`: Verifies happy path when skills file exists
- `test_main_file_not_exists_triggers_download`: Tests auto-download on missing file
- `test_main_handles_file_not_found_error`: Verifies error handling
- `test_main_execution_order`: Ensures correct execution sequence
- `test_main_full_flow_with_download`: Integration test with download step

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_download_skills.py
```

### Run specific test class
```bash
pytest tests/test_find_relevant_skills.py::TestInitializeModel
```

### Run specific test function
```bash
pytest tests/test_main.py::TestMain::test_main_file_exists
```

### Run tests by marker
```bash
# Run only download tests
pytest -m download

# Run only unit tests
pytest -m unit

# Run all except slow tests
pytest -m "not slow"
```

### Run with coverage report
```bash
pip install pytest-cov
pytest --cov=src/linkedin_skill_semantic_transformer --cov-report=html
```

### Run with detailed output on failures
```bash
pytest -vv --tb=long
```

## Mocking Strategy

### External Dependencies Mocked
1. **URL Downloads**: `urllib.request.urlopen` is mocked to simulate remote file fetching
2. **ML Model**: `SentenceTransformer` is mocked to avoid loading heavy neural networks
3. **Similarity Computation**: `util.cos_sim` and `torch.topk` are mocked for predictable results
4. **File I/O**: File operations are mocked to avoid filesystem dependencies

### Why Mock?
- **Speed**: Tests run in milliseconds instead of seconds
- **Isolation**: Tests don't depend on external services
- **Reliability**: No network failures or file permission issues
- **Determinism**: Results are predictable and repeatable

## Test Organization

```
tests/
├── conftest.py                    # Shared fixtures
├── test_download_skills.py        # Download module tests
├── test_find_relevant_skills.py   # ML core tests
└── test_main.py                   # Orchestration tests
```

## Coverage Goals

- **Overall Coverage**: > 85%
- **Critical Paths**: 100% (download, search initialization, error handling)
- **Edge Cases**: All major edge cases tested
- **Error Handling**: All error paths verified

## Test Conventions

1. **Naming**: `test_<function>_<scenario>` (e.g., `test_download_skills_network_error`)
2. **Setup/Teardown**: `setup_method()` for per-test initialization
3. **Assertions**: Clear, specific assertions with helpful messages
4. **Fixtures**: Used for common test data and mocks
5. **Parametrization**: Multiple similar tests use `@pytest.mark.parametrize`

## Adding New Tests

When adding new functionality:
1. Add fixtures to `conftest.py` if reusable
2. Create test class in appropriate module
3. Use descriptive test names
4. Mock external dependencies
5. Test both success and failure paths
6. Update this documentation

## Dependencies

Test dependencies (in `pyproject.toml`):
- `pytest`: Test framework
- `pytest-cov` (optional): Coverage reporting
- Mock objects use Python's built-in `unittest.mock`

## Known Limitations

1. **Integration Tests**: Full integration tests require actual skills file (not mocked)
2. **Performance Tests**: Not currently included
3. **API Tests**: No API testing (CLI only)
4. **Concurrency**: No concurrent execution tests

## Future Improvements

- [ ] Add performance benchmarks
- [ ] Add integration tests with real ML model (slow tests)
- [ ] Add parametrized tests for multiple skill datasets
- [ ] Add memory usage tests
- [ ] Add logging verification tests
