"""Shared fixtures and configuration for all tests."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock
import numpy as np
import torch


@pytest.fixture
def sample_skills():
    """Fixture providing a list of sample LinkedIn skills."""
    return [
        "Python",
        "JavaScript",
        "AWS Certified Solutions Architect",
        "Cloud Computing",
        "Machine Learning",
        "Data Science",
        "Penetration Testing",
        "Network Security",
        "Docker",
        "Kubernetes",
    ]


@pytest.fixture
def skills_file(tmp_path, sample_skills):
    """Fixture providing a temporary skills file."""
    skills_path = tmp_path / "linkedin_skills.txt"
    skills_path.write_text("\n".join(sample_skills), encoding="utf-8")
    return skills_path


@pytest.fixture
def mock_sentence_transformer():
    """Fixture providing a mocked SentenceTransformer model."""
    mock_model = MagicMock()
    
    # Create deterministic embeddings for testing
    def encode_side_effect(texts, convert_to_tensor=False):
        """Generate embeddings with fixed dimensions."""
        if isinstance(texts, str):
            # Single string query
            embedding = torch.randn(384)
        else:
            # List of strings
            embedding = torch.randn(len(texts), 384)
        
        if convert_to_tensor:
            return embedding
        return embedding.numpy() if isinstance(embedding, torch.Tensor) else embedding
    
    mock_model.encode.side_effect = encode_side_effect
    return mock_model


@pytest.fixture
def mock_util():
    """Fixture providing a mocked util module for cosine similarity."""
    mock = MagicMock()
    
    def cos_sim_side_effect(query_embedding, skill_embeddings):
        """Return mock cosine similarity scores."""
        # Return random scores between 0 and 1
        num_skills = skill_embeddings.shape[0]
        scores = torch.rand(1, num_skills)
        return scores
    
    mock.cos_sim.side_effect = cos_sim_side_effect
    return mock


@pytest.fixture
def downloaded_skills_content():
    """Fixture providing sample downloaded skills content."""
    return """AWS
AWS Certified Solutions Architect
AWS Certified Developer
Cloud Computing
Azure
Docker
Kubernetes
Python
JavaScript
Java
C++
Machine Learning
Deep Learning
Data Science
Penetration Testing
Network Security
Cybersecurity
"""


@pytest.fixture
def monkeypatch_imports(monkeypatch, mock_sentence_transformer, mock_util):
    """Fixture to monkeypatch sentence_transformers and torch.util imports."""
    monkeypatch.setattr(
        "find_relevant_skills.SentenceTransformer",
        lambda x: mock_sentence_transformer
    )
    monkeypatch.setattr(
        "find_relevant_skills.util",
        mock_util
    )
    return monkeypatch
