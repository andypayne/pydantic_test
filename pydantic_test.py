import json
import pydantic
from typing import Optional, List


class RootValidationError(Exception):
    """
    Raised when the root item fails validation.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class Field3ValidationError(Exception):
    """
    Raised when field3 fails validation.
    """

    def __init__(self, value: int, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class ItemType(pydantic.BaseModel):
    id: int
    field1: str
    field2: str
    field3: Optional[float]
    field4: Optional[str]

    @pydantic.root_validator(pre=True)
    @classmethod
    def root_validator(cls, values):
        """
        Validator for the item
        """
        if "field3" not in values and "field4" not in values:
            raise RootValidationError(
                message="Either field3 or field4 must be defined."
            )
        return values

    @pydantic.validator("field3")
    @classmethod
    def field3_valid(cls, value):
        """
        Validator for field3
        """
        if value > 1000:
            raise Field3ValidationError(
                value=value, message="field3 must be less than 1000."
            )
        return value

    class Config:
        """
        Pydantic config
        """

        allow_mutation = False
        # anystr_lower = True


def main() -> None:
    with open("./sample.json") as f:
        json_data = json.load(f)
        items: List[ItemType] = [ItemType(**item) for item in json_data]
        print(f"Item 0: {items[0]}")
        print(f"Item 2 dict: {items[2].dict(exclude={'id'})}")
        print(f"Item 1 field2: {items[1].field2}")
        # Copy
        item0_copy = items[0].copy()
        print(f"copy of item 0: {item0_copy}")
        # Mutation will fail with allow_mutation set to False above.
        # items[2].field1 = "Change attempt"


if __name__ == "__main__":
    main()
