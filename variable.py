rint("Hello! I am your AI Chatbot.")
print("Type 'bye' to exit.")
while True:
    user = input("You: ")

    if user.lower() =="hello":
        print("Bot: Hello! How arer you?")

    elif user.lower() == "how are you":
        print("Bot: I am fine!_🙂")

    elif user.lower() == "what is your name":
        print("Bot: My name is python Bot.")

    elif user.lower == "bye":
        print("Bot: Goodbye! 👋")
        break
    else:
        print("Bot: sorry, I don't understand.") 
