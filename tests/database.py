# from fastapi.testclient import TestClient
# import pytest

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app import schemas
# from app.config import settings
# from app.database import get_db, Base
# from app import models


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DTB_USERNAME}:{settings.DTB_PWD}@{settings.DTB_HOSTNAME}/{settings.DTB_NAME}_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture()
# def session():
# # return the database
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture()
# def client(session):
# # return just the client response
#     # run following code BEFORE running the test below
#     # Base.metadata.drop_all(bind=engine)
#     # Base.metadata.create_all(bind=engine)
    
#     def override_get_db():
#         db = TestSessionLocal()
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db

#     yield TestClient(app)

#     # run any following code AFTER the test below
