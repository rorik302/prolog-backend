from uuid import UUID

from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    TENANT_UUID: UUID = UUID("7d99dc86-71d1-47f8-b101-f1bc39b9d42a")
    TENANT_SCHEMA_NAME: str = "test"
    USER_UUID: UUID = UUID("41e21a84-8258-42f3-bd5b-2c5574d19148")
    USER_EMAIL: str = "user@test.ru"
    USER_PASSWORD: str = "password"


test_settings: TestSettings = TestSettings()
