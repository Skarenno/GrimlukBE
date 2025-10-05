from app.models.db_models import UserModel
from app.models.request_models import UserInfoRequest
import uuid

residence_fields = [
    "residence_address_1",
    "residence_address_2",
    "postal_code",
    "city",
    "province",
    "country"
]

def map_user_info_to_db(request: UserInfoRequest, existing_user: UserModel | None = None) -> UserModel:
    user_data = request.model_dump()

    for field in residence_fields:
        if field in user_data and isinstance(user_data[field], str):
            user_data[field] = user_data[field].upper()

    if existing_user:
        for k, v in user_data.items():
            setattr(existing_user, k, v)
        return existing_user

    return UserModel(id=str(uuid.uuid4()), **user_data)
