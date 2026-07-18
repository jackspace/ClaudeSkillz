# Advanced Integrations

Cloud and LLM integrations can improve extraction quality, but they send
document content to external services. Confirm authorization before use.

## Azure Document Intelligence

Install the optional extra and provide the endpoint through configuration or an
approved secret store:

```bash
pip install 'markitdown[az-doc-intel]'
```

```python
from markitdown import MarkItDown

converter = MarkItDown(
    docintel_endpoint="<document_intelligence_endpoint>",
)
result = converter.convert_local("documents/complex.pdf")
print(result.text_content)
```

## LLM Image Descriptions

Image descriptions currently apply to image and presentation conversion:

```python
from markitdown import MarkItDown
from openai import OpenAI

converter = MarkItDown(
    llm_client=OpenAI(),
    llm_model="gpt-4o",
    llm_prompt="Describe diagrams and charts precisely.",
)
result = converter.convert_local("slides/deck.pptx")
```

Never place credentials in a skill, script, or command example. Use environment
variables or an approved secret store, and avoid sending confidential documents
to services that are not authorized for them.

