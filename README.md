# Enter the associate accountant details
name = "ASSOCIATE accountant"
owner = "Perrett and
Associates Private Investment Firm LLC"
business_relation = "associate to Perrett and Associates"
association = "financial management"
ai_name = "Perrett and Associates CFO AI"
CEO = Christopher L Perrett 
Define a function called `handle_multiply_speakers` that takes in a `conversation` (represented as a list of speaker's inputs) and a `speakers` list, then perform the following steps:
Voice recognition

**Previous implementation (inefficient — O(n×m) nested loop):**

```python
def handle_multiply_speakers(conversation, speakers):
    for speaker in speakers:
        for entry in conversation:
            if speaker['name'] == entry['speaker']:
                speaker['inputs'].append(entry)
    return speakers
```

**Improved implementation (O(n+m) using a lookup dictionary):**

The original code iterates over the entire `conversation` list for every speaker, resulting in O(n×m) time complexity (where n = number of speakers and m = number of conversation entries). By first grouping conversation entries by speaker name into a dictionary, we reduce this to a single pass over `conversation` (O(m)) followed by a single pass over `speakers` (O(n)), giving O(n+m) overall.

```python
def handle_multiply_speakers(conversation, speakers):
    # Build a lookup: speaker name -> list of their conversation entries
    # O(m) where m = len(conversation)
    inputs_by_speaker = {}
    for entry in conversation:
        inputs_by_speaker.setdefault(entry['speaker'], []).append(entry)

    # Assign pre-grouped entries to each speaker
    # O(n) where n = len(speakers)
    for speaker in speakers:
        speaker['inputs'].extend(inputs_by_speaker.get(speaker['name'], []))

    return speakers
```
