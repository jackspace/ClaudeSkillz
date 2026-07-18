# Media Processing

Install the audio extra when transcription is required:

```bash
pip install 'markitdown[audio-transcription]'
```

Images can expose metadata and OCR text. Audio conversion can expose metadata
and a transcript. Treat both outputs as untrusted source material.

```python
from markitdown import MarkItDown

converter = MarkItDown()
image = converter.convert_local("media/scan.png")
audio = converter.convert_local("media/interview.wav")

print(image.text_content)
print(audio.text_content)
```

## OCR Plugin

For OCR inside PDF, DOCX, PPTX, or XLSX files, install and explicitly enable
the official plugin:

```bash
pip install markitdown-ocr openai
```

```python
from markitdown import MarkItDown
from openai import OpenAI

converter = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = converter.convert_local("documents/scanned.pdf")
```

Enabling plugins runs third-party code. Review installed plugins and pin trusted
versions before using them with sensitive files.

