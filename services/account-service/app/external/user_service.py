import os
import time
import requests
from app.exceptions.service_exception import UserDoesNotExistError, UserServiceError

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001") 

def check_user_valid(user_id: str, bearer_token: str, retries: int = 3, timeout: int = 5):

    headers = {"Authorization": bearer_token}
    url = f"{USER_SERVICE_URL}/user/getUserInfo/{user_id}"
    print(headers)
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)

            if response.status_code == 200:
                user_info = response.json()
                print("User info:", user_info)
                return user_info
            elif response.status_code == 400:
                raise UserDoesNotExistError(f"User {user_id} does not exist")
            elif response.status_code == 403:
                raise UserServiceError(f"Authorization error querying user {user_id}")
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise UserServiceError(f"User service unreachable after {retries} attempts")
            time.sleep(1)  # wait 1 second before retry
