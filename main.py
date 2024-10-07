import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


# Base URL for image links
BASE_IMAGE_URL = "https://cipher-compendium.com/images/cards/"

txt_file = "./cipher/official-cards.txt"  # Path to the input text file
xml_file = "./output_cards.xml"  # Path to the output XML file

# Function to escape special characters and clean text
def escape_description(description):
    return description.replace("\n", " ").replace("&#x27;", "'")

# Function to normalize card names for grouping (ignores the "+" at the end)
def normalize_card_name(card_name):
    return card_name.replace("+", "").strip()

# Function to add or update a card element with card properties and sets
def add_card_properties_and_set(cards_dict, card):
    normalized_name = normalize_card_name(card.get('Name', ''))

    # Check if the card with the similar normalized name already exists
    if normalized_name in cards_dict:
        card_element = cards_dict[normalized_name]
    else:
        # Create a new card element if not already present
        card_element = ET.Element("card")
        ET.SubElement(card_element, "name").text = normalized_name  # Store normalized name

        # Combine and escape card skills
        description = f"{card.get('Skill#1', '')} {card.get('Skill#2', '')} {card.get('Skill#3', '')} {card.get('Skill#4', '')}".strip()
        ET.SubElement(card_element, "text").text = escape_description(description)

        prop = ET.SubElement(card_element, "prop")
        ET.SubElement(prop, "manacost").text = card.get('Cost', '')
        ET.SubElement(prop, "colors").text = card.get('Color', 'NORMAL')
        ET.SubElement(prop, "maintype").text = card.get('Class', '')
        ET.SubElement(prop, "type").text = card.get('Type', '')

        # Adding attack/support as pt (Power/Toughness in other games)
        if card.get('Attack') and card.get('Support'):
            ET.SubElement(prop, "pt").text = f"{card.get('Attack')}/{card.get('Support')}"

        # Store the card in the dictionary
        cards_dict[normalized_name] = card_element

    # Add the set element for the specific version of the card (based on rarity and image)
    set_code = card.get('Imagefile', '')  # Extract set code from Imagefile
    image_url = f"{BASE_IMAGE_URL}{set_code}.png"  # Construct image URL

    # Add set with image URL and rarity
    set_element = ET.SubElement(card_element, "set", rarity=card.get('Rarity', 'Unknown'), picURL=image_url)
    set_element.text = card.get('Set', 'Unknown')

# Function to create XML structure
def create_cockatrice_xml(cards):
    root = ET.Element("cockatrice_carddatabase", version="4", attrib={
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "https://raw.githubusercontent.com/Cockatrice/Cockatrice/master/doc/carddatabase_v4/cards.xsd"
    })

    ET.SubElement(root, "sets")
    cards_element = ET.SubElement(root, "cards")

    # Dictionary to hold card elements by normalized name (to combine sets for similar cards)
    cards_dict = {}

    for card in cards:
        add_card_properties_and_set(cards_dict, card)  # Add properties and sets to the card

    # Append all card elements to the cards element
    for card_element in cards_dict.values():
        cards_element.append(card_element)

    return ET.ElementTree(root)

# Function to pretty-print XML
def pretty_print_xml(tree):
    rough_string = ET.tostring(tree.getroot(), 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")

# Save the XML to a file with pretty print
def save_xml(tree, filename):
    pretty_xml = pretty_print_xml(tree)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Pretty-printed XML saved to {filename}")

# Function to parse the text file and return card data
def parse_txt_file(txt_file):
    cards = []
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split("\t")
        for line in lines[1:]:
            card_values = line.strip().split("\t")
            card_data = dict(zip(headers, card_values))
            cards.append(card_data)
    return cards

if __name__ == "__main__":

    # Parse the text file
    cards = parse_txt_file(txt_file)

    if cards:
        # Create Cockatrice XML
        cockatrice_tree = create_cockatrice_xml(cards)

        # Save the XML with pretty print
        save_xml(cockatrice_tree, xml_file)
