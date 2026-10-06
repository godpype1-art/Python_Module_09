from pydantic import (BaseModel, ValidationError, Field, DateTime, model_validator)


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: DateTime = Field(DateTime)
    is_operacional: bool = Field(default=True)
    notes: str | None = Field(max_length=200, default=None)

    @classmethod
    @model_validator(mode='after')
    def validate(cls, value):
        return super().validate(value)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
