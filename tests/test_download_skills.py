"""Tests for the download_skills module."""

import pytest
import urllib.error
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linkedin_skill_semantic_transformer.download_skills import download_skills


class TestDownloadSkills:
    """Test suite for download_skills function."""

    def test_successful_download(self, tmp_path, downloaded_skills_content, capsys):
        """Test successful download of skills file."""
        output_file = tmp_path / "linkedin_skills.txt"
        
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = downloaded_skills_content.encode("utf-8")
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            # Patch the filename in the module
            with patch("linkedin_skill_semantic_transformer.download_skills.FILENAME", str(output_file)):
                download_skills()
        
        # Verify file was created
        assert output_file.exists()
        
        # Verify content
        content = output_file.read_text(encoding="utf-8")
        assert "AWS" in content
        assert "Python" in content
        
        # Verify printed output
        captured = capsys.readouterr()
        assert "Downloading" in captured.out
        assert "Saved" in captured.out

    def test_download_preserves_encoding(self, tmp_path, downloaded_skills_content):
        """Test that downloaded file preserves UTF-8 encoding."""
        output_file = tmp_path / "linkedin_skills.txt"
        
        # Add unicode characters to test encoding
        unicode_content = downloaded_skills_content + "\nC# / C Sharp\nC++\n日本語スキル"
        
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = unicode_content.encode("utf-8")
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            with patch("linkedin_skill_semantic_transformer.download_skills.FILENAME", str(output_file)):
                download_skills()
        
        # Read back and verify encoding is preserved
        content = output_file.read_text(encoding="utf-8")
        assert "日本語スキル" in content

    def test_download_counts_lines_correctly(self, tmp_path, capsys):
        """Test that download correctly counts lines in output message."""
        output_file = tmp_path / "linkedin_skills.txt"
        skills_content = "Skill1\nSkill2\nSkill3\nSkill4\nSkill5"
        
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = skills_content.encode("utf-8")
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            with patch("linkedin_skill_semantic_transformer.download_skills.FILENAME", str(output_file)):
                download_skills()
        
        captured = capsys.readouterr()
        assert "Saved 5 lines" in captured.out

    def test_network_error_handling(self, tmp_path, capsys):
        """Test handling of network errors."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.URLError("Network error")
            
            with patch("linkedin_skill_semantic_transformer.download_skills.FILENAME", str(tmp_path / "test.txt")):
                with pytest.raises(SystemExit) as exc_info:
                    download_skills()
                assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Network error" in captured.out

    def test_file_system_error_handling(self, capsys):
        """Test handling of file system errors."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b"test content"
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            with patch("builtins.open", side_effect=OSError("Permission denied")):
                with pytest.raises(SystemExit) as exc_info:
                    download_skills()
                assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "File system error" in captured.out

    def test_empty_response_handling(self, tmp_path):
        """Test handling of empty response from URL."""
        output_file = tmp_path / "linkedin_skills.txt"
        
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b""
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            
            with patch("linkedin_skill_semantic_transformer.download_skills.FILENAME", str(output_file)):
                download_skills()
        
        # File should be created even if empty
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == ""
