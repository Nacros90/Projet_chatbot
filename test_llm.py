import openai

client = openai.OpenAI(api_key="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")

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un assistant amical."},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content
    return reply

while True:
    user_input = input("Vous: ")
    if user_input.lower() == "quit":
        break
    bot_response = generate_response(user_input)
    print("Bot:", bot_response)
