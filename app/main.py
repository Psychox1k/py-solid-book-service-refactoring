import json
import xml.etree.ElementTree as ET
from typing import Protocol


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class Displayer(Protocol):
    def display(self, book: Book) -> None:
        ...


class Printer(Protocol):
    def print(self, book: Book) -> None:
        ...


class Serializer(Protocol):
    def serialize(self, book: Book) -> None:
        ...


class ConsoleDisplayer:
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplayer:
    def display(self, book: Book):
        print(book.content[::-1])


class ConsolePrinter:
    def print(self, book: Book):
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrinter:
    def print(self, book: Book):
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class JSONSerializer:
    def serialize(self, book: Book):
        return json.dumps({"title": book.title, "content": book.content})


class XMLSerializer:
    def serialize(self, book: Book):
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


DISPLAYERS: dict[str, Displayer] = {
    "console": ConsoleDisplayer(),
    "reverse": ReverseDisplayer(),
}


PRINTERS: dict[str, Printer] = {
    "console": ConsolePrinter(),
    "reverse": ReversePrinter(),
}

SERIALIZERS: dict[str, Serializer] = {
    "json": JSONSerializer(),
    "xml": XMLSerializer(),
}


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    last_result = None

    for cmd, method_type in commands:
        if cmd == "display":
            if method_type not in DISPLAYERS:
                raise ValueError(f"Unknown display type: {method_type}")
            DISPLAYERS[method_type].display(book)
        elif cmd == "print":
            if method_type not in PRINTERS:
                raise ValueError(f"Unknown print type: {method_type}")
            PRINTERS[method_type].print(book)
        elif cmd == "serialize":
            if method_type not in SERIALIZERS:
                raise ValueError(f"Unknown serialize type: {method_type}")
            last_result = SERIALIZERS[method_type].serialize(book)
        else:
            raise ValueError(f"Unknown command: {cmd}")

    return last_result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    result = main(sample_book, [("display", "reverse"), ("serialize", "xml")])
    if result:
        print(f"\nSerialized Output:\n{result}")
