# Day 5 - Test file
# Run this to test the brochure builder functions

import json
from day5_brochure_builder import select_relevant_links, stream_brochure

# TEST 1 - does AI correctly filter out privacy/email links?
dummy_links = [
    "https://huggingface.co/about",
    "https://huggingface.co/careers",
    "https://huggingface.co/privacy",    # should be removed
    "mailto:contact@huggingface.co",     # should be removed
]

result = select_relevant_links("https://huggingface.co", dummy_links)
print(json.dumps(result, indent=2))

# TEST 2 - does brochure generate correctly?
dummy_content = """
HuggingFace builds open source AI tools.
They are hiring engineers and researchers.
Customers include Google and Microsoft.
"""

stream_brochure("HuggingFace", dummy_content)