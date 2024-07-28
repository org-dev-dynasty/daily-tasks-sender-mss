import random
import string

def generate_confirmation_code(self):
        return ''.join(random.choices(string.digits, k=6))