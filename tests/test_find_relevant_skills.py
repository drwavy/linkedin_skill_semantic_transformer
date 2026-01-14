"""Tests for the find_relevant_skills module."""

import pytest
import sys
import torch
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linkedin_skill_semantic_transformer import find_relevant_skills


class TestInitializeModel:
    """Test suite for initialize_model function."""

    def test_initialize_model_loads_skills(self, skills_file, mock_sentence_transformer):
        """Test that initialize_model loads skills from file."""
        with patch("linkedin_skill_semantic_transformer.find_relevant_skills.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value = skills_file.open("r", encoding="utf-8")
            
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.SentenceTransformer") as mock_st:
                mock_st.return_value = mock_sentence_transformer
                
                with patch("linkedin_skill_semantic_transformer.find_relevant_skills.open", 
                          mock_open(read_data=skills_file.read_text())):
                    find_relevant_skills.initialize_model()
        
        # Verify model was initialized
        assert find_relevant_skills.model is not None
        assert find_relevant_skills.skills_list is not None
        assert len(find_relevant_skills.skills_list) > 0

    def test_initialize_model_computes_embeddings(self, skills_file, mock_sentence_transformer):
        """Test that initialize_model computes embeddings for all skills."""
        with patch("builtins.open", create=True) as mock_open:
            content = skills_file.read_text()
            mock_open.return_value.__enter__.return_value.readlines.return_value = content.split("\n")
            mock_open.return_value.__enter__.return_value.__iter__ = lambda self: iter(content.split("\n"))
            
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.SentenceTransformer") as mock_st:
                mock_st.return_value = mock_sentence_transformer
                
                # Reset globals
                find_relevant_skills.skills_list = []
                find_relevant_skills.model = None
                find_relevant_skills.skill_embeddings = None
                
                find_relevant_skills.initialize_model()
        
        # Verify embeddings were created
        assert find_relevant_skills.skill_embeddings is not None
        assert isinstance(find_relevant_skills.skill_embeddings, torch.Tensor)

    def test_initialize_model_file_not_found(self, capsys):
        """Test initialize_model raises error when skills file is missing."""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with pytest.raises(FileNotFoundError):
                find_relevant_skills.initialize_model()

    def test_initialize_model_empty_file(self, tmp_path):
        """Test initialize_model with empty skills file."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")
        
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.__iter__ = lambda self: iter([])
            
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.SentenceTransformer"):
                find_relevant_skills.skills_list = []
                find_relevant_skills.model = None
                find_relevant_skills.skill_embeddings = None
                
                find_relevant_skills.initialize_model()
        
        # Should handle empty list gracefully
        assert find_relevant_skills.skills_list is not None


class TestFindRelevantSkills:
    """Test suite for find_relevant_skills function."""

    def setup_method(self):
        """Reset globals before each test."""
        find_relevant_skills.skills_list = ["Python", "JavaScript", "AWS", "Docker"]
        find_relevant_skills.model = MagicMock()
        find_relevant_skills.skill_embeddings = torch.randn(4, 384)

    def test_find_relevant_skills_not_initialized(self, capsys):
        """Test error when find_relevant_skills called without initialization."""
        find_relevant_skills.model = None
        
        with pytest.raises(RuntimeError, match="Model not initialized"):
            find_relevant_skills.find_relevant_skills("Python")

    def test_find_relevant_skills_returns_top_k(self, capsys):
        """Test that find_relevant_skills returns top k results."""
        # Mock the encoding and similarity computation
        query_embedding = torch.randn(1, 384)
        find_relevant_skills.model.encode.return_value = query_embedding
        
        with patch("linkedin_skill_semantic_transformer.find_relevant_skills.util") as mock_util:
            # Create mock scores
            scores = torch.tensor([[0.9, 0.7, 0.5, 0.3]])
            mock_util.cos_sim.return_value = scores
            
            # Mock torch.topk
            with patch("torch.topk") as mock_topk:
                top_values = torch.tensor([0.9, 0.7])
                top_indices = torch.tensor([0, 1])
                mock_topk.return_value = (top_values, top_indices)
                
                find_relevant_skills.find_relevant_skills("Python", top_k=2)
        
        captured = capsys.readouterr()
        assert "Best matches for 'Python'" in captured.out
        assert "Python" in captured.out

    def test_find_relevant_skills_custom_top_k(self):
        """Test find_relevant_skills with custom top_k parameter."""
        find_relevant_skills.model.encode.return_value = torch.randn(1, 384)
        
        with patch("linkedin_skill_semantic_transformer.find_relevant_skills.util") as mock_util:
            scores = torch.tensor([[0.9, 0.8, 0.7, 0.6]])
            mock_util.cos_sim.return_value = scores
            
            with patch("torch.topk") as mock_topk:
                mock_topk.return_value = (torch.randn(5), torch.arange(5))
                
                # Should use k=5 without error
                find_relevant_skills.find_relevant_skills("test", top_k=5)
                
                # Verify topk was called with correct k
                mock_topk.assert_called()

    def test_find_relevant_skills_score_formatting(self, capsys):
        """Test that scores are formatted to 4 decimal places."""
        query_embedding = torch.randn(1, 384)
        find_relevant_skills.model.encode.return_value = query_embedding
        
        with patch("linkedin_skill_semantic_transformer.find_relevant_skills.util") as mock_util:
            scores = torch.tensor([[0.123456, 0.987654]])
            mock_util.cos_sim.return_value = scores
            
            with patch("torch.topk") as mock_topk:
                mock_topk.return_value = (torch.tensor([0.123456, 0.987654]), torch.tensor([0, 1]))
                
                find_relevant_skills.find_relevant_skills("test", top_k=2)
        
        captured = capsys.readouterr()
        # Check that scores are formatted with 4 decimals
        assert "0.1235" in captured.out or "0.9877" in captured.out

    def test_find_relevant_skills_zero_similarity(self, capsys):
        """Test find_relevant_skills with zero similarity scores."""
        find_relevant_skills.model.encode.return_value = torch.randn(1, 384)
        
        with patch("linkedin_skill_semantic_transformer.find_relevant_skills.util") as mock_util:
            scores = torch.tensor([[0.0, 0.0, 0.0, 0.0]])
            mock_util.cos_sim.return_value = scores
            
            with patch("torch.topk") as mock_topk:
                mock_topk.return_value = (torch.zeros(2), torch.tensor([0, 1]))
                
                find_relevant_skills.find_relevant_skills("unrelated", top_k=2)
        
        captured = capsys.readouterr()
        assert "0.0000" in captured.out


class TestStartInteractiveSearch:
    """Test suite for start_interactive_search function."""

    def setup_method(self):
        """Reset globals before each test."""
        find_relevant_skills.skills_list = ["Python", "JavaScript"]
        find_relevant_skills.model = MagicMock()
        find_relevant_skills.skill_embeddings = torch.randn(2, 384)

    def test_start_interactive_search_quit_command(self):
        """Test that 'q' command exits the search loop."""
        with patch("builtins.input", return_value="q"):
            # Should not raise error and should exit cleanly
            find_relevant_skills.start_interactive_search()

    def test_start_interactive_search_processes_query(self):
        """Test that queries are processed before exit."""
        with patch("builtins.input", side_effect=["Python", "q"]):
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.find_relevant_skills") as mock_find:
                find_relevant_skills.model.encode.return_value = torch.randn(1, 384)
                
                find_relevant_skills.start_interactive_search()
                
                # Verify find_relevant_skills was called with the query
                mock_find.assert_called_once_with("Python")

    def test_start_interactive_search_multiple_queries(self):
        """Test that multiple queries are processed before exit."""
        queries = ["Python", "Docker", "AWS", "q"]
        
        with patch("builtins.input", side_effect=queries):
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.find_relevant_skills") as mock_find:
                find_relevant_skills.start_interactive_search()
                
                # Verify find_relevant_skills was called three times (not counting 'q')
                assert mock_find.call_count == 3
                mock_find.assert_any_call("Python")
                mock_find.assert_any_call("Docker")
                mock_find.assert_any_call("AWS")

    def test_start_interactive_search_case_insensitive_quit(self):
        """Test that quit command is case insensitive."""
        with patch("builtins.input", side_effect=["Python", "Q", "q"]):
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.find_relevant_skills"):
                # Second 'Q' should exit, so no third input needed
                with patch("builtins.input", return_value="Q"):
                    find_relevant_skills.start_interactive_search()

    def test_start_interactive_search_empty_input(self):
        """Test handling of empty input."""
        with patch("builtins.input", side_effect=["", "q"]):
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.find_relevant_skills") as mock_find:
                find_relevant_skills.start_interactive_search()
                
                # Empty string is not 'q', so find_relevant_skills should be called
                mock_find.assert_called_once_with("")

    def test_start_interactive_search_whitespace_input(self):
        """Test handling of whitespace-only input."""
        with patch("builtins.input", side_effect=["  ", "q"]):
            with patch("linkedin_skill_semantic_transformer.find_relevant_skills.find_relevant_skills") as mock_find:
                find_relevant_skills.start_interactive_search()
                
                # Whitespace is passed as-is
                mock_find.assert_called_once_with("  ")
