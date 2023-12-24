import xml.etree.ElementTree as ET


def extract_text_from_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Function to recursively extract text from each element
    def recurse_and_extract(element):
        text_content = ""
        if element.text:
            text_content += element.text.strip() + " "
        for child in element:
            text_content += recurse_and_extract(child)
        return text_content

    # Extract text starting from the root
    extracted_text = recurse_and_extract(root)
    return extracted_text
