import xml.etree.ElementTree as ET

# Define input and output files
txt_file = "./cipher/official-cards.txt"  # Path to the input text file
xml_file = "./output_cards.xml"  # Path to the output XML file


# Function to create a card XML element
def create_card_element(card_data):
    card = ET.Element("card")

    name = ET.SubElement(card, "name")
    name.text = card_data.get("Name")

    text = ET.SubElement(card, "text")
    text.text = f'{card_data.get("Skill#1", "")} {card_data.get("Skill#2", "")} {card_data.get("Skill#3", "")} {card_data.get("Skill#4", "")}'.strip()

    prop = ET.SubElement(card, "prop")

    layout = ET.SubElement(prop, "layout")
    layout.text = "normal"

    side = ET.SubElement(prop, "side")
    side.text = "front"

    card_type = ET.SubElement(prop, "type")
    card_type.text = card_data.get("Type")

    maintype = ET.SubElement(prop, "maintype")
    maintype.text = card_data.get("Class")

    manacost = ET.SubElement(prop, "manacost")
    manacost.text = card_data.get("Cost")

    colors = ET.SubElement(prop, "colors")
    colors.text = card_data.get("Color")

    cmc = ET.SubElement(prop, "cmc")
    cmc.text = str(len(card_data.get("Cost", "")))  # Assuming the length of Cost represents CMC

    pt = ET.SubElement(prop, "pt")
    pt.text = f'{card_data.get("Attack", "")}/{card_data.get("Support", "")}'

    return card


# Function to parse the text file and generate XML
def parse_txt_to_xml(txt_file, xml_file):
    # Create root element
    root = ET.Element("cockatrice_carddatabase", version="4")
    cards = ET.SubElement(root, "cards")

    # Open and read the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

        # Parse each card's data from the text file
        headers = lines[0].strip().split("\t")
        for line in lines[1:]:
            card_values = line.strip().split("\t")
            card_data = dict(zip(headers, card_values))
            card_element = create_card_element(card_data)
            cards.append(card_element)

    # Generate XML tree and write to file
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# Parse the file and generate XML
parse_txt_to_xml(txt_file, xml_file)
