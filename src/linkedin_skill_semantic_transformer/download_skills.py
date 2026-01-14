import urllib.request
import urllib.error
import sys

URL = "https://raw.githubusercontent.com/maciejszewczyk/linkedin-skills/master/linkedin_skills.txt"
FILENAME = "linkedin_skills.txt"

def download_skills():
    print(f"Downloading {FILENAME} from:\n{URL}")
    
    try:
        with urllib.request.urlopen(URL) as response:
            data = response.read()
            
            text_content = data.decode('utf-8')
            
            with open(FILENAME, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
        print(f"Saved {len(text_content.splitlines())} lines to '{FILENAME}'")
        
    except urllib.error.URLError as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"File system error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_skills()