# two_factor.py
import pyotp

def generate_2fa_secret(email: str) -> str:
    secret = pyotp.random_base32()
    return secret

def generate_otp(secret: str) -> str:
    """Generate a one-time password based on the provided secret."""
    totp = pyotp.TOTP(secret, interval= 30)
    otp = totp.now()
    return otp

def verify_otp(secret: str, otp: str) -> bool:
    """Verify the provided OTP against the secret."""
    totp = pyotp.TOTP(secret)   
    return totp.verify(otp)

def debug_otp_flow(secret: str, user_otp: str):
    """Debug OTP generation and verification."""
    totp = pyotp.TOTP(secret)
    generated_otp = totp.now()
    print(f"Generated OTP: {generated_otp}")
    print(f"User Provided OTP: {user_otp}")
    print(f"OTP Validity Time (in seconds): {totp.interval}")
    is_valid = totp.verify(user_otp)
    print(f"Is OTP valid? {is_valid}")
    return is_valid
