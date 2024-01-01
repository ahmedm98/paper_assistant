from lxml import etree


class TEIFile:
    def __init__(self, file_path):
        self.tree = etree.parse(file_path)
        self.ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        self._title = None
        self._abstract = None
        self._body = None

    def get_title(self):
        if self._title is None:
            title_element = self.tree.find(
                ".//tei:titleStmt/tei:title", self.ns
            )
            self._title = (
                title_element.text
                if title_element is not None
                else "Title not found"
            )
        return self._title

    def get_abstract(self):
        if self._abstract is None:
            abstract = self.tree.find(
                ".//tei:profileDesc/tei:abstract", self.ns
            )
            self._abstract = (
                etree.tostring(
                    abstract, method="text", encoding="unicode"
                ).strip()
                if abstract is not None
                else "Abstract not found"
            )
        return self._abstract

    def get_body(self):
        if self._body is None:
            body = self.tree.find(".//tei:body", self.ns)
            paragraphs = []
            for div in body.findall(".//tei:div", self.ns):
                paragraph = {}
                head = div.find(".//tei:head", self.ns)
                head_text = head.text if head is not None else "No Header"
                paragraph["header"] = head_text

                para_texts = []
                for para in div.findall(".//tei:p", self.ns):
                    para_text = para.text or ""
                    para_texts.append(para_text)

                paragraph["text"] = para_texts
                paragraphs.append(paragraph)
            self._body = paragraphs

        return self._body


"""
def extract_text_from_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # TODO make this better but only extracting relevant text.
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
"""
