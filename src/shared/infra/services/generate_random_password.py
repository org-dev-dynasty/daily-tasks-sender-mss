import random
import string

def generate_random_password():
  characters = string.ascii_letters + string.digits + string.punctuation
  password = []
  
  # Ensure the password has at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character
  password.append(random.choice(string.ascii_uppercase))
  password.append(random.choice(string.ascii_lowercase))
  password.append(random.choice(string.digits))
  password.append(random.choice(string.punctuation))
  
  # Fill the rest of the password up to 12 characters
  while len(password) < 12:
      password.append(random.choice(characters))
  
  # Shuffle the characters to ensure randomness
  random.shuffle(password)
  
  # Convert the list of characters into a string
  return ''.join(password)