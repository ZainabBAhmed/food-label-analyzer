import csv
import os

class FoodLogManager:
    """
    Handles saving, reading, searching, updating, and deleting
    food products from the food log CSV file.
    """

    def _init_(self, filename="food_log.csv"):
        self.filename = filename
        self.fields = [
            "food_name",
            "barcode",
            "calories",
            "sugar",
            "fat",
            "salt",
            "allergens"
        ]

        self.create_file()

    def create_file(self):
        """
        Creates the CSV file if it does not already exist.
        """
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()

    def save_food(self, food):
        """
        Saves a food product to the CSV file.

        The food argument should be a dictionary containing:
        food_name, barcode, calories, sugar, fat, salt, allergens
        """

        try:
            with open(
                self.filename,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fields
                )

                writer.writerow({
                    "food_name": food.get("food_name", "Unknown"),
                    "barcode": food.get("barcode", "N/A"),
                    "calories": food.get("calories", "N/A"),
                    "sugar": food.get("sugar", "N/A"),
                    "fat": food.get("fat", "N/A"),
                    "salt": food.get("salt", "N/A"),
                    "allergens": food.get("allergens", "None")
                })

            return True

        except (OSError, csv.Error) as error:
            print(f"Error saving food: {error}")
            return False

    def get_all_foods(self):
        """
        Reads and returns all saved food products.
        """

        foods = []

        try:
            with open(
                self.filename,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    foods.append(row)

            return foods

        except FileNotFoundError:
            print("Food log file was not found.")
            return []

        except (OSError, csv.Error) as error:
            print(f"Error reading food log: {error}")
            return []

    def search_food(self, search_term):
        """
        Searches for a food product by name or barcode.
        """

        foods = self.get_all_foods()
        results = []

        search_term = str(search_term).lower().strip()

        for food in foods:
            food_name = food["food_name"].lower()
            barcode = food["barcode"].lower()

            if search_term in food_name or search_term in barcode:
                results.append(food)

        return results

    def delete_food(self, search_term):
        """
        Deletes a food product by name or barcode.
        """

        foods = self.get_all_foods()

        if not foods:
            return False

        search_term = str(search_term).lower().strip()

        new_foods = []
        deleted = False

        for food in foods:
            food_name = food["food_name"].lower()
            barcode = food["barcode"].lower()

            if (
                search_term in food_name
                or search_term in barcode
            ):
                deleted = True
            else:
                new_foods.append(food)

        if deleted:
            try:
                with open(
                    self.filename,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    writer = csv.DictWriter(
                        file,
                        fieldnames=self.fields
                    )

                    writer.writeheader()
                    writer.writerows(new_foods)

                return True

            except (OSError, csv.Error) as error:
                print(f"Error deleting food: {error}")
                return False

        return False

    def update_food(self, search_term, updated_food):
        """
        Updates an existing food product by name or barcode.
        """

        foods = self.get_all_foods()

        if not foods:
            return False

        search_term = str(search_term).lower().strip()
        updated = False

        for food in foods:
            food_name = food["food_name"].lower()
            barcode = food["barcode"].lower()

            if (
                search_term in food_name
                or search_term in barcode
            ):
                for field in self.fields:
                    if field in updated_food:
                        food[field] = updated_food[field]

                updated = True
                break

        if updated:
            try:
                with open(
                    self.filename,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    writer = csv.DictWriter(
                        file,
                        fieldnames=self.fields
                    )

                    writer.writeheader()
                    writer.writerows(foods)

                return True

            except (OSError, csv.Error) as error:
                print(f"Error updating food: {error}")
                return False

        return False


# ---------------------------------------------------------
# TESTING THE FILE HANDLING MODULE
# ---------------------------------------------------------

if __name__ == "_main_":

    food_log = FoodLogManager()

    # Sample food products for testing
    food1 = {
        "food_name": "Indomie Instant Noodles",
        "barcode": "1234567890123",
        "calories": "450",
        "sugar": "3",
        "fat": "18",
        "salt": "2.5",
        "allergens": "Wheat, Soy"
    }

    food2 = {
        "food_name": "Coca Cola",
        "barcode": "9876543210987",
        "calories": "140",
        "sugar": "39",
        "fat": "0",
        "salt": "0",
        "allergens": "None"
    }

    # Save sample foods
    food_log.save_food(food1)
    food_log.save_food(food2)

    print("\n--- SAVED FOOD PRODUCTS ---")

    foods = food_log.get_all_foods()

    for food in foods:
        print(food)

    # Search for a food
    print("\n--- SEARCH RESULTS ---")

    results = food_log.search_food("Indomie")

    for food in results:
        print(food)

    print("\nFile handling test completed successfully.")