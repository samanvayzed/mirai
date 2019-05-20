import random
import re

bot_template = "BOT : {0}"
user_template = "USER : {0}"

patterns = {}

keywords = {
            'goodbye': ['bye', 'farewell'],
            'greet': ['hello', 'hi', 'hey'],
            'thankyou': ['thank', 'thx']
            }

responses = {
            'default': 'default message',
            'goodbye': 'goodbye for now',
            'greet': 'Hello you! :)',
            'thankyou': 'you are very welcome'
            }


# Iterate over the keywords dictionary
for intent, keys in keywords.items():
    # Create regular expressions and compile them into pattern objects
    patterns[intent] = re.compile('|'.join(keys))

# Print the patterns
#print(patterns)



# Define a function to find the intent of a message
def match_intent(message):
    matched_intent = None
    for intent, pattern in patterns.items():
        # Check if the pattern occurs in the message
        if pattern.search(message):
            matched_intent = intent
    return matched_intent

# Define a respond function
def respond(message):
    # Call the match_intent function
    intent = match_intent(message)
    # Fall back to the default response
    key = "default"
    if intent in responses:
        key = intent
    return responses[key]





# Define find_name()
def find_name(message):
    name = None
    # Create a pattern for checking if the keywords occur
    name_keyword = re.compile('"name"|"call"')#########################
    
    # Create a pattern for finding capitalized words
    name_pattern = re.compile('[A-Z]{1}[a-z]*')
    
    
    if name_keyword.search(message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words)
    return name


# Define respond()
def respond2(message):
    # Find the name
    name = find_name(message)
    if name is None:
        return "Hi there!"
    else:
        return "Hello, {0}!".format(name)













def send_message(message):
    print("Here")
    # Print user_template including the user_message
    print(user_template.format(message))
    response = respond2(message)

    print(bot_template.format(response))

# Send messages
#send_message("hello!")
#send_message("bye byeee")
#send_message("thanks very much!")

# Send messages
send_message("my name is David Copperfield")
send_message("call me Ishmael")
send_message("People call me Cassandra")

