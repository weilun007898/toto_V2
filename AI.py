import openai

# Set up your OpenAI API key
openai.api_key = "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"

file_path = "basic rules.txt"
file_path_1 = "training_chat.txt"
with open(file_path, "r") as file:
    file_content = file.read()
with open(file_path_1, "r") as file:
    file_content_1 = file.read()
Q = "mpt 8579=2 9058=3 st 7676.3 8787.4 3621.8.6.3"
Z = "E\n7765  .3 .3 .3 iBox\nH E\n3453 .3\n1143 .3"
X = "M S 3132=2 HE 4320=2 0342=2 E S 7644=2 4147=2 1474=2"

response = openai.ChatCompletion.create(
    model="gpt-4o",  # or "gpt-3.5-turbo"
    # model="ft:gpt-4o-mini-2024-07-18:abunene::AiFZsnhU",
    messages=[
        {"role": "system", "content": "Your job is to convert the user input based on knowledge uploaded"},
        {"role": "user", "content": f"Here is the rules \n\n{file_content}\n\n and \n\n{file_content_1}\n\n that you "
                                    f"need to understand, Please"
                                    f"look out the region make sure the region is compatible with the number. Now"
                                    f"answer this: {Q}"},
        {"role": "assistant", "content": "D\n#123\n8579#2\n9058#3\n#43\n7676#3\n8787#4\n3621#8#6#3"},
        {"role": "user", "content": f"Here is the rules \n\n{file_content}\n\n and \n\n{file_content_1}\n\n that you "
                                    f"need to understand, Please"
                                    f"look out the region make sure the region is compatible with the number. Now"
                                    f"answer this: {Z}"},
        {"role": "assistant", "content": "D\n#89\n**7765#3#3#3\n#1\n3454#3\n1143#3"},
        {"role": "user", "content": "Wrong! The answer is D\n#9\n**7765#3#3#3\n#89\n3454#3\n1143#3"},
        {"role": "assistant", "content": "D\n#9\n**7765#3#3#3\n#89\n3454#3\n1143#3"},
        {"role": "user", "content": f"answer this: {X}"}
    ],
    temperature=1.0,
)

# Print the result
print(response["choices"][0]["message"]["content"])
