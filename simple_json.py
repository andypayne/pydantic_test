import json


def main() -> None:
    with open("./sample.json") as f:
        json_data = json.load(f)
        print(f"Item[0]: {json_data[1]}")
        print(f"Item[1] field 2: {json_data[1]['field2']}")


if __name__ == "__main__":
    main()
