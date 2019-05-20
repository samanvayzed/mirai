import random
import re

bot_template = "BOT : {0}"
user_template = "USER : {0}"

# Define variables
name = "Greg"
weather = "cloudy"

# Define a dictionary with the predefined responses

responses = {
    "what's your name?": ["my name is {0}".format(name),
                          "they call me {0}".format(name),
                          "I go by {0}".format(name)],
                          
    "what's today's weather?": ["the weather is {0}".format(weather),
                                "it's {0} today".format(weather)],
                                
    "default": ["I am sorry, I couldn't understand you",
                "I won't be able to assist you with that",
                "Can you please be a little more clear with your question?"]
}

responses1 = {'question': ["I don't know :(",
                           'you tell me!'],
    
              'statement': ['tell me more!',
                            'why do you think that?',
                            'how long have you felt this way?',
                            'I find that extremely interesting',
                            'can you back that up?',
                            'oh wow!',
                            ':)']}

rules = {'I want (.*)': ['What would it mean if you got {0}',
                         'Why do you want {0}',
                         "What's stopping you from getting {0}"],

        'do you remember (.*)': ['Did you think I would forget {0}',
                                 "Why haven't you been able to forget {0}",
                                 'What about {0}',
                                 'Yes .. and?'],

        'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],

        'if (.*)': ["Do you really think it's likely that {0}",
                    'Do you wish that {0}',
                    'What do you think about {0}',
                    'Really--if {0}']}



def replace_pronouns(message):
    message = message.lower()
    
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me', 'you', message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my', 'your', message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your', 'my', message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)

    return message



def match_rule(rules, message):
    response, phrase = "default", None
    
    # Iterate over the rules dictionary
    for pattern, responses in rules.items():
        
        # Create a match object
        match = re.search(pattern,message)
        
        if match is not None:
            # Choose a random response
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    # Return the response and phrase
    return response.format(phrase),phrase




def respond(message):
    # Check if the message is in the responses
    if message in responses:
        # Return the matching message
        bot_message = random.choice(responses[message])
    else:
        # Return the "default" message
        bot_message = random.choice(responses["default"])
    return bot_message

def respond1(message):
    # Check for a question mark
    if message.endswith("?"):
        # Return a random question
        return random.choice(responses1["question"])
    # Return a random statement
    return random.choice (responses1["statement"])

# Define respond()
def respond3(message):
    print("here")
    # Call match_rule
    response, phrase = match_rule(rules,message)
    if '{0}' in response:
        # Replace the pronouns in the phrase
        phrase = replace_pronouns(phrase)
        # Include the phrase in the response
        response = response.format(phrase)
    return response






# Define a function that sends a message to the bot: send_message
def send_message(message):
    print("Here")
    # Print user_template including the user_message
    print(user_template.format(message))
    # Get the bot's response to the message
    #response = respond(message)
    response = respond3(message)
    # Print the bot template including the bot's response.
    print(bot_template.format(response))



# Test function
#print(respond("hello!"))
#name = input("Write something: ")
#print(name)
#send_message(name)

# Test match_rule
#print(match_rule(rules, "if you are happy"))


# Send the messages
send_message("do you remember your last birthday")
send_message("do you think humans should be worried about AI")
send_message("I want a robot friend")
send_message("what if you could be anything you wanted")


