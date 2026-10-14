import random


def show_intro():
    print("====================================")
    print("      NUMBER GUESSING GAME")
    print("====================================")
    print("I will think of a number between 1 and 100.")
    print("You have 7 chances to guess it correctly.")
    print("Type 'exit' anytime to quit the game.")


def play_round():
    secret_number = random.randint(1, 100)
    attempts = 0

    while attempts < 7:
        guess = input("\nEnter your guess (1-100): ").strip()

        if guess.lower() == "exit":
            print("Thanks for playing! Goodbye!")
            return False

        try:
            guess = int(guess)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess < 1 or guess > 100:
            print("Number must be between 1 and 100.")
            continue

        attempts += 1

        if guess < secret_number:
            print("Too low! Try a higher number.")
        elif guess > secret_number:
            print("Too high! Try a lower number.")
        else:
            print(f"Correct! You guessed the number in {attempts} attempt(s).")
            return True

        remaining = 7 - attempts
        print(f"Attempts left: {remaining}")

    print(f"Game over! The secret number was {secret_number}.")
    return True


def main():
    show_intro()
    score = 0

    while True:
        won = play_round()
        if won is False:
            break

        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ("y", "yes"):
            print(f"Your final score is: {score}")
            print("Thanks for playing!")
            break

        score += 1
        print("\nStarting a new round...")


if __name__ == "__main__":
    main()
