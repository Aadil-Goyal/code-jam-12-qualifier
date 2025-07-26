from __future__ import annotations

import re
from node import Node

def query_selector_all(node: Node, selector: str) -> list[Node]:
	selectors = selector.split(", ")
	out = []
	req_tag, req_id, req_class = '', '', set()
	for s in selectors:
		if not s: continue

		s = re.match(r"(\w*)([#\w-]*)([.\w-]*)", s).groups()
		req_tag = s[0]
		req_id = s[1][1:]
		req_class = set(s[2].split('.')[1:])

		out.extend(loop(node, req_tag, req_id, req_class))
	return out

def loop(node: 'Node', req_tag: str, req_id: str, req_class: set[str]) -> list[Node]:
	out = []
	if check(node, req_tag, req_id, req_class):
		out.append(node)

	for child in node.children:
		out.extend(loop(child, req_tag, req_id, req_class))
	return out

def check(node: 'Node', req_tag: str, req_id: str, req_class: set[str]) -> bool:
	if req_tag != '' and node.tag != req_tag:
		return False
	if req_id != '' and node.attributes.get('id', '') != req_id:
		return False
	if not req_class.issubset(node.attributes.get('class', '').split()):
		return False

	return True


def main():
	# node = Node(tag="h1", text="This is a heading!")
	node = Node(
			tag="div",
			attributes={"id": "topDiv"},
			children=[
				Node(
					tag="div",
					attributes={"id": "innerDiv", "class": "container colour-primary"},
					children=[
						Node(tag="h1", text="This is a heading!"),
						Node(
							tag="p",
							attributes={"class": "colour-secondary", "id": "innerContent"},
							text="I have some content within this container also!",
						),
						Node(
							tag="p",
							attributes={"class": "colour-secondary", "id": "two"},
							text="This is another paragraph.",
						),
						Node(
							tag="p",
							attributes={"class": "colour-secondary important"},
							text="This is a third paragraph.",
						),
						Node(
							tag="a",
							attributes={"id": "home-link", "class": "colour-primary button"},
							text="This is a button link.",
						),
					],
				),
				Node(
					tag="div",
					attributes={"class": "container colour-secondary"},
					children=[
						Node(
							tag="p",
							attributes={"class": "colour-primary"},
							text="This is a paragraph in a secondary container.",
						),
					],
				),
			],
		)

	# out = query_selector_all(node, ".colour-primary")
	out = query_selector_all(node, ".missing-class")

	print(f'{out=}')


if __name__ == "__main__":
	main()

