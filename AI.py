import openai

# Set up your OpenAI API key
openai.api_key = "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"


# Correct method for new library versions
response = openai.ChatCompletion.create(
    model="ft:gpt-4o-mini-2024-07-18:personal::AWpNwfq1",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "Your job is to convert the user input based on knowledge uploaded"},
        {"role": "user", "content": "None Forwarded: TPMSHE 7136=2B 7775=2B 1194=2B 12:16"}
    ],
    temperature=1.0,
)

# Print the result
print(response["choices"][0]["message"]["content"])
