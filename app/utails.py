
# Import CryptContext from passlib to handle password hashing
from passlib.context import CryptContext  

# Create a CryptContext instance with bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  


# Function to hash a password before storing it in the database
def hash(password: str):  
    return pwd_context.hash(password)  # Hashes the password using bcrypt


# Function to verify if a provided password matches the stored hash
def verify(plain_password, hashed_password):  
    return pwd_context.verify(plain_password, hashed_password)  # Compares plain password with hashed version
