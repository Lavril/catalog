from pydantic import BaseModel, ConfigDict


class PhoneSchema(BaseModel):
    number: str

    model_config = ConfigDict(from_attributes=True)


class ActivitySchema(BaseModel):
    id: int
    name: str
    parent_id: int | None

    model_config = ConfigDict(from_attributes=True)


class BuildingSchema(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class OrganizationSchema(BaseModel):
    id: int
    name: str
    building: BuildingSchema
    phones: list[PhoneSchema]
    activities: list[ActivitySchema]

    model_config = ConfigDict(from_attributes=True)
