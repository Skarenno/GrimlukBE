from fastapi import HTTPException, status
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def validateBody(cls, body:dict):
    allowed_keys = cls.model_fields.keys()
    body_keys =  body.keys()

    logger.info(allowed_keys)
    logger.info(body)

    #Check for valid keys
    for attribute in body_keys:
        logger.info(f"attribute: {attribute}")
        if not attribute in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{attribute} is not a valid key for {cls.__name__}"
            )