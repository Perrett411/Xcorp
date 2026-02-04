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
pythonCopy code`def handle_multiply_speakers(conversation, speakers):
 for speaker in speakers:
 for input in conversation:
 if speaker['name'] == input['speaker']:
 speaker['inputs'].append(input)
 return speakers`
