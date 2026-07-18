# Web Content

MarkItDown can convert HTML, EPUB, RSS, and YouTube transcript sources.

```bash
pip install 'markitdown[youtube-transcription]'
markitdown 'https://www.youtube.com/watch?v=VIDEO_ID' -o transcript.md
```

## Safer Remote Fetching

Do not pass an untrusted URL directly to permissive `convert()`. Validate the
scheme and destination, bound redirects and response size, then provide the
response to `convert_response()`.

```python
import requests
from markitdown import MarkItDown

url = "https://docs.example.com/guide.html"
if not url.startswith("https://docs.example.com/"):
    raise ValueError("URL is outside the approved host")

response = requests.get(url, timeout=15, allow_redirects=False)
response.raise_for_status()
if len(response.content) > 5_000_000:
    raise ValueError("Response exceeds 5 MB")

result = MarkItDown().convert_response(response)
print(result.text_content)
```

For production systems, also reject private, loopback, link-local, and metadata
service destinations after DNS resolution.

