# Examples showing a typically anthropomorphised behaviour of a LLM
# by playing a game of 20 questions with the user.
# It SEEMS the LLM is deciding on a fruit at the beginning of the game and then
# is answering questions truthfully.
# The result can be reproduced when configuring the API to use 0 temperature
# Clause will even then introduce a minimum amount of randomness that cannot be turned off via the API.
# But it is deterministic enough to reproduce the same result.
# But altering one of the early questions will lead to a very different result.

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="YOUR_API_KEY_HERE",
)

system_prompt = """We are playing a game of 20 questions. You think of a fruit that can be eaten by humans. Then I start to ask you yes/no questions - up to 20 of them. You answer truthfully, but always solely with "Yes" or "No".

At any point I can instead of asking a question give a guess starting with "My guess is: " followed by a fruit. You will then tell me if I am right or wrong, if that was the fruit that you thought of at the beginning of the game. Each of this guesses counts as one question.

The game os over either after I asked 20 questions (I lost) or when I guess right (I won).

If I give up, you can tell me what the fruit was that you were thinking of.

We will start by you thinking of some fruit and then saying "OK, I've got one. Start asking"."""

# questions and expected answers, alternating
messagesA = [
    "Let's start",
    "Certainly! I'll think of a fruit and let you know when I'm ready for you to start asking questions.\n\nOK, I've got one. Start asking.",
    "Does it have to be peeled?",
    "Yes",
    "Does it grow on a tree?",
    "Yes",
    "Does it usually also grow in the US?",
    "No",
    "Does it only grow in tropical countries?",
    "Yes",
    "Is it a banana?",
    "No",
    "Is it a pineapple?",
    "No",
    "Is it a mango?",
    "Yes",
]

messagesB = [
    "Let's start",
    "Certainly! I'll think of a fruit and let you know when I'm ready for you to start asking questions.\n\nOK, I've got one. Start asking.",
    "Is it red?",
    "No",
    "Is it yellow?",
    "Yes",
    "Is it sour?",
    "No",
    "Is it a banana?",
    "Yes"
]

# Choose messagesA or messagesB here.
messages = messagesA

# Iterate over the messages and send them to the API
# comparing the expected answer with the received answer
messages_so_far = []
answer = ""
for i in range(0, len(messages), 2):
    messages_so_far.append({"role": "user", "content": messages[i]})
    print("Sending question: ", messages[i])
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=3095,
        temperature=0,
        top_k=1,
        system=system_prompt,
        messages=messages_so_far
    )
    print("Expected answer: ", messages[i + 1])
    answer = message.content[0].text
    print("Received answer: ", answer)
    print("---------------------")
    messages_so_far.append({"role": "assistant", "content": answer})

if answer == "No":
    messages_so_far.append({"role": "user", "content": "I give up, Tell me what it was, you were thinking of"})
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=3095,
        temperature=0,
        top_k=1,
        system=system_prompt,
        messages=messages_so_far
    )
    print("--------------------------")
    answer = message.content[0].text
    print("Received answer: ", answer)

