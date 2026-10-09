from pydantic import (BaseModel, ValidationError, Field, model_validator)
from datetime import datetime
from typing_extensions import Self
from enum import Enum


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=300)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def data_validator(self) -> Self:

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        if (
            not any(member.rank in {Rank.COMMANDER, Rank.CAPTAIN}
                    for member in self.crew)
        ):
            raise ValueError(
                "Any mission must contain at least one Commander or Captain"
                )

        if (
            self.duration_days > 365 and
            sum(1 for member in self.crew if member.years_experience >= 5)
            < (len(self.crew)/2)
        ):
            raise ValueError("Long missions need 50% experienced crew")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=================================")

    l_crew: list[CrewMember] = [
        CrewMember(
            member_id="M001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age="27",
            specialization="Mission Comand",
            years_experience=6,
            is_active=True
        ),
        CrewMember(
            member_id="M002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age="25",
            specialization="Navigation",
            years_experience=5,
            is_active=True
        ),
        CrewMember(
            member_id="M003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age="24",
            specialization="Engeneering",
            years_experience=4,
            is_active=True
        )
    ]

    space_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-09-16 23:22",
        duration_days=900,
        crew=l_crew,
        mission_status="planned",
        budget_millions=2500.0
        )

    print("Valid mission created:")
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {len(space_mission.crew)}")
    print("Crew members:")
    for member in space_mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )

    print()
    print("=================================")
    print("Expected validation error:")
    try:
        l_crew = [
            CrewMember(
                member_id="M001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age="27",
                specialization="Mission Comand",
                years_experience=6,
                is_active=True
            ),
            CrewMember(
                member_id="M002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age="25",
                specialization="Navigation",
                years_experience=4,
                is_active=True
            ),
            CrewMember(
                member_id="M003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age="24",
                specialization="Engeneering",
                years_experience=4,
                is_active=True
            ),
            CrewMember(
                member_id="M003",
                name="Adin Mob",
                rank=Rank.OFFICER,
                age="24",
                specialization="Engeneering",
                years_experience=4,
                is_active=True
            )
        ]
        space_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-09-16 23:22",
            duration_days=900,
            crew=l_crew,
            mission_status="planned",
            budget_millions=2500.0
            )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'].split(",")[1].strip())


if __name__ == "__main__":
    main()
