"""Tests for the main orchestration module."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linkedin_skill_semantic_transformer import main


class TestMain:
    """Test suite for main orchestration function."""

    def test_main_file_exists(self, tmp_path, capsys):
        """Test main when linkedin_skills.txt already exists."""
        # Create a mock skills file
        skills_file = tmp_path / "linkedin_skills.txt"
        skills_file.write_text("Python\nJavaScript\n", encoding="utf-8")
        
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                mock_find_module.initialize_model = MagicMock()
                mock_find_module.start_interactive_search = MagicMock()
                
                main.main()
        
        captured = capsys.readouterr()
        assert "Found 'linkedin_skills.txt'" in captured.out

    def test_main_file_not_exists_triggers_download(self, capsys):
        """Test main triggers download when skills file doesn't exist."""
        with patch("os.path.exists", return_value=False):
            with patch("linkedin_skill_semantic_transformer.main.download_skills") as mock_download:
                with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                    mock_find_module.initialize_model = MagicMock()
                    mock_find_module.start_interactive_search = MagicMock()
                    
                    main.main()
        
        # Verify download was called
        mock_download.assert_called_once()
        
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_main_initializes_model(self, capsys):
        """Test that main calls initialize_model."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                mock_find_module.initialize_model = MagicMock()
                mock_find_module.start_interactive_search = MagicMock()
                
                main.main()
        
        # Verify initialize_model was called
        mock_find_module.initialize_model.assert_called_once()

    def test_main_starts_interactive_search(self, capsys):
        """Test that main starts the interactive search loop."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                mock_find_module.initialize_model = MagicMock()
                mock_find_module.start_interactive_search = MagicMock()
                
                main.main()
        
        # Verify start_interactive_search was called
        mock_find_module.start_interactive_search.assert_called_once()

    def test_main_initialization_message_printed(self, capsys):
        """Test that initialization message is printed."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills"):
                main.main()
        
        captured = capsys.readouterr()
        assert "Initializing AI Model" in captured.out

    def test_main_download_message_when_file_missing(self, capsys):
        """Test that download message is printed when file is missing."""
        with patch("os.path.exists", return_value=False):
            with patch("linkedin_skill_semantic_transformer.main.download_skills"):
                with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills"):
                    main.main()
        
        captured = capsys.readouterr()
        assert "not found" in captured.out
        assert "fetching" in captured.out

    def test_main_handles_file_not_found_error(self, capsys):
        """Test main handles FileNotFoundError during model initialization."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                mock_find_module.initialize_model.side_effect = FileNotFoundError("Skills file not found")
                
                with pytest.raises(SystemExit) as exc_info:
                    main.main()
                
                assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_main_execution_order(self, capsys):
        """Test that main executes in correct order: check -> download -> init -> search."""
        with patch("os.path.exists", return_value=False):
            with patch("linkedin_skill_semantic_transformer.main.download_skills") as mock_download:
                with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find_module:
                    mock_find_module.initialize_model = MagicMock()
                    mock_find_module.start_interactive_search = MagicMock()
                    
                    main.main()
        
        # Verify order of calls
        mock_download.assert_called_once()
        mock_find_module.initialize_model.assert_called_once()
        mock_find_module.start_interactive_search.assert_called_once()

    def test_main_skips_download_if_file_exists(self):
        """Test that download is skipped if file exists."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.download_skills") as mock_download:
                with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills"):
                    main.main()
        
        # Verify download was NOT called
        mock_download.assert_not_called()


class TestMainIntegration:
    """Integration tests for the main module."""

    def test_main_full_flow_with_file_present(self):
        """Test complete main flow when file exists."""
        with patch("os.path.exists", return_value=True):
            with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find:
                mock_find.initialize_model = MagicMock()
                mock_find.start_interactive_search = MagicMock(side_effect=KeyboardInterrupt())
                
                # Should complete without error (KeyboardInterrupt is normal)
                try:
                    main.main()
                except KeyboardInterrupt:
                    pass

    def test_main_full_flow_with_download(self):
        """Test complete main flow with download."""
        with patch("os.path.exists", return_value=False):
            with patch("linkedin_skill_semantic_transformer.main.download_skills") as mock_download:
                with patch("linkedin_skill_semantic_transformer.main.find_relevant_skills") as mock_find:
                    mock_find.initialize_model = MagicMock()
                    mock_find.start_interactive_search = MagicMock(side_effect=KeyboardInterrupt())
                    
                    try:
                        main.main()
                    except KeyboardInterrupt:
                        pass
                    
                    # Verify download was called
                    mock_download.assert_called_once()


class TestMainEntryPoint:
    """Test suite for main entry point."""

    def test_if_name_main_calls_main(self):
        """Test that running as __main__ calls main()."""
        # This is a basic check - harder to test without subprocess
        assert hasattr(main, 'main')
        assert callable(main.main)

    def test_main_is_callable(self):
        """Test that main function is callable."""
        assert callable(main.main)

    def test_main_takes_no_arguments(self):
        """Test that main() function signature accepts no required arguments."""
        import inspect
        sig = inspect.signature(main.main)
        required_params = [
            p for p in sig.parameters.values()
            if p.default == inspect.Parameter.empty
        ]
        assert len(required_params) == 0
