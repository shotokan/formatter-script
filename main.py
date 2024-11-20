import requests
import json
import csv

url = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"


def get_json_data(url):
    """Fetches the JSON data from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the response is bad
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return None


def extract_attributes(value_escr):
    """Extracts the necessary attributes from the 'value' in 'es-CR'."""
    # Extract the requested values
    allergens = [
        allergen["name"]
        for allergen in value_escr.get("allergens", {}).get("value", [])
    ]
    return {
        "allergens": allergens,
        "sku": value_escr.get("sku", {}).get("value", ""),
        "vegan": value_escr.get("vegan", {}).get("value", "FALSE"),
        "kosher": value_escr.get("kosher", {}).get("value", "FALSE"),
        "organic": value_escr.get("organic", {}).get("value", "FALSE"),
        "vegetarian": value_escr.get("vegetarian", {}).get("value", "FALSE"),
        "gluten_free": value_escr.get("gluten_free", {}).get("value", "FALSE"),
        "lactose_free": value_escr.get("lactose_free", {}).get("value", "FALSE"),
        "package_quantity": value_escr.get("package_quantity", {}).get("value", 1.0),
        "unit_size": value_escr.get("unit_size", {}).get("value", 0.0),
        "net_weight": value_escr.get("net_weight", {}).get("value", 0.0),
    }


def save_as_csv(file_name, data):
    """Saves the extracted data into a CSV file."""
    csv_headers = [
        "allergens",
        "sku",
        "vegan",
        "kosher",
        "organic",
        "vegetarian",
        "gluten_free",
        "lactose_free",
        "package_quantity",
        "unit_size",
        "net_weight",
    ]
    try:
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerow(csv_headers)
            writer.writerow(data)
        print(f"Data successfully saved in {file_name}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")


def fetch_and_save_as_csv(url, file_name):
    """Fetches JSON data from the URL and saves it into a CSV file."""
    data = get_json_data(url)
    if data is None or "allVariants" not in data:
        print("No data found.")
        return

    if len(data["allVariants"]) == 0:
        print("No variants found.")
        return

    if "attributesRaw" not in data["allVariants"][0]:
        print("No attributes found.")
        return

    # Look for the custom_attributes
    for v in data["allVariants"][0]["attributesRaw"]:
        if v["name"] == "custom_attributes":
            value_escr = json.loads(v["value"]["es-CR"])

            # Extract the attributes
            attributes = extract_attributes(value_escr)

            # Save the data to CSV
            save_as_csv(
                file_name,
                [
                    attributes["allergens"],
                    attributes["sku"],
                    attributes["vegan"],
                    attributes["kosher"],
                    attributes["organic"],
                    attributes["vegetarian"],
                    attributes["gluten_free"],
                    attributes["lactose_free"],
                    attributes["package_quantity"],
                    attributes["unit_size"],
                    attributes["net_weight"],
                ],
            )
            break


if __name__ == "__main__":
    fetch_and_save_as_csv(url, "products.csv")
