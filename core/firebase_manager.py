"""Firebase Manager for Auth and Data Storage (No-Billing Spark Plan).

Uses Pyrebase4 to interact with Firebase REST API.
"""

import pyrebase
import os
import json
from dotenv import load_dotenv
from typing import Optional, Dict, Union, Tuple

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "") # Make optional
}

# Initialize Firebase safely
try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
except Exception as e:
    print(f"[FIREBASE] Initialization Error: {e}")
    firebase = None
    auth = None
    db = None

class FirebaseManager:
    """Handles user sessions and lightweight data logging."""

    @staticmethod
    def sign_in_anonymous() -> Tuple[Optional[Dict], Optional[str]]:
        """Signs in a user anonymously. Returns (user_dict, error_msg)."""
        if not auth:
            return None, "Firebase not initialized."
        try:
            user = auth.sign_in_anonymous()
            return user, None
        except Exception as e:
            error_json = getattr(e, 'args', [None])[0]
            try:
                error_msg = json.loads(error_json)['error']['message']
            except:
                error_msg = str(e)
            return None, error_msg

    @staticmethod
    def sign_in_email(email: str, password: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Signs in with email/password. Returns (user_dict, error_msg)."""
        if not auth:
            return None, "Firebase not initialized."
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return user, None
        except Exception as e:
            error_json = getattr(e, 'args', [None])[0]
            try:
                error_msg = json.loads(error_json)['error']['message']
            except:
                error_msg = str(e)
            return None, error_msg

    @staticmethod
    def sign_up_email(email: str, password: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Creates a new user account. Returns (user_dict, error_msg)."""
        if not auth:
            return None, "Firebase not initialized."
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return user, None
        except Exception as e:
            error_json = getattr(e, 'args', [None])[0]
            try:
                error_msg = json.loads(error_json)['error']['message']
            except:
                error_msg = str(e)
            return None, error_msg

    @staticmethod
    def log_simulation_result(user_id: str, results: Dict) -> bool:
        """Logs summary simulation data to Realtime DB."""
        if not db:
            return False
        try:
            db.child("users").child(user_id).child("simulations").push(results)
            return True
        except Exception as e:
            print(f"[FIREBASE] DB Error: {e}")
            return False
