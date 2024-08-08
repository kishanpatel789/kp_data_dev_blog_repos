import random 

greeting_options = [
    "Let's get after it!",
    "Good morning, gorgeous. It's math time.",
    "Rise and shine. It's time to grind.",
    "Remember that guy who couldn't add? Me neither.",
]

def generate_greeting() -> str:
    """
    Selects and returns a random greeting from the list of greeting options.

    Returns:
        str: A randomly selected greeting.
    """
    return random.choice(greeting_options)