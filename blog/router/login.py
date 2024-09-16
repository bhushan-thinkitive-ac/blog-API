from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid
import pyotp
from .. import schemas, data_base, models, token
from ..hashing import Hash
from ..email import send_password_reset_email
from ..two_factor import generate_2fa_secret, generate_otp, verify_otp, debug_otp_flow

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)

@router.post('/enable_2fa')
def enable_two_factor(items: schemas.EnableTwoFactor, db: Session = Depends(data_base.get_db)):
    user = db.query(models.User).filter(models.User.email == items.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not Hash.verify(user.password, items.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    secret = generate_2fa_secret(items.email)
    user.two_factor_secret = secret
    user.is_two_factor_enabled = True
    db.commit()

    otp = generate_otp(secret)  # Generate a test OTP for immediate verification or communication
    return {"otp": otp, "detail": "2FA enabled. Use the OTP provided for verification."}

@router.post('/verify_2fa')
def verify_two_factor(items: schemas.VerifyTwoFactor, db: Session = Depends(data_base.get_db)):
    user = db.query(models.User).filter(models.User.email == items.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.is_two_factor_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is not enabled for this user")

    is_valid = verify_otp(user.two_factor_secret, items.code)

    print("user.two_factor_secret", user.two_factor_secret, "items.code", items.code)
    if not is_valid:
        # Use the debug function to troubleshoot
        # Use the debug function to troubleshoot
        debug_otp_flow(user.two_factor_secret, items.code)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP code")
    
    return {"detail": "2FA code verified successfully"}

@router.post('/')
def login_verify_2fa(items: schemas.VerifyTwoFactor, db: Session = Depends(data_base.get_db)):
    user = db.query(models.User).filter(models.User.email == items.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.is_two_factor_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is not enabled for this user")

    # Debugging output
    is_valid = verify_otp(user.two_factor_secret, items.code)
    if not is_valid:
        debug_otp_flow(user.two_factor_secret, items.code)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP code")
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}




@router.post('/forget_password')
def forget_password(items: schemas.ForgetPassword, db: Session = Depends(data_base.get_db)):
    user = db.query(models.User).filter(models.User.email == items.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Generate a unique reset code
    reset_code = str(uuid.uuid4())
    
    # Send the email with the reset code
    send_password_reset_email(items.email, reset_code)
    
    return {"reset_code": reset_code, "detail": "Password reset code has been sent to your email."}

