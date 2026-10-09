from pydantic import (BaseModel, ValidationError, Field, model_validator)
from datetime import datetime
from typing_extensions import Optional, Self
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str | None] = Field(
        max_length=500, default=None
        )
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def data_validator(self) -> Self:

        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact id must start with AC (Alien Contact)")

        if (
            self.contact_type is ContactType.PHYSICAL
            and self.is_verified is False
        ):
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type is ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )

        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals should include received messages")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=================================")

    a_contact = AlienContact(
        contact_id="AC-8080",
        timestamp="2026-09-16 23:22",
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes="45",
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True
        )

    print("Valid contact report:")
    print(f"ID: {a_contact.contact_id}")
    print(f"Type: {a_contact.contact_type}")
    print(f"Location: {a_contact.location}")
    print(f"Signal: {a_contact.signal_strength}/10")
    print(f"Duration: {a_contact.duration_minutes} minutes")
    print(f"Witnesses: {a_contact.witness_count}")
    print(f"Message: {a_contact.message_received}")
    print()
    print("=================================")
    print("Expected validation error:")
    try:
        a_contact = AlienContact(
            contact_id="AC-8080",
            timestamp="2026-09-16 23:22",
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes="45",
            witness_count=1,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
            )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'].split(",")[1].strip())


if __name__ == "__main__":
    main()
