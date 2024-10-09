import json
import os

def convert_to_fixture_format(input_file, output_file, model_name):
    # Load existing JSON data
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Prepare the new format
    fixture_data = []
    for index, entry in enumerate(data):
        # Create a dictionary in the Django fixture format
        fixture_entry = {
            "model": model_name,
            "pk": index + 1,  # Primary key (1-based index)
            "fields": entry  # Assuming entry is already a dict of fields
        }
        fixture_data.append(fixture_entry)

    # Write the new format to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(fixture_data, outfile, indent=4)

# Example usage
# Specify your input CSV and output JSON file paths and the model name
convert_to_fixture_format('fixtures/places.json', 'fixtures/places.json', 'core.models.Place')
convert_to_fixture_format('fixtures/hotels.json', 'fixtures/hotels.json', 'core.models.Hotel')
convert_to_fixture_format('fixtures/users.json', 'fixtures/users.json', 'core.models.User')
convert_to_fixture_format('fixtures/reviews.json', 'fixtures/reviews.json', 'core.models.Review')
