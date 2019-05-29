from bs4 import BeautifulSoup, Tag


def element_is(element, name=None, attributes=None, text=None):
	if name is not None:
		if element.name != name:
			return False

	if attributes is not None:
		for key, value in attributes.items():
			if key not in element.attrs:
				return False
			elif element.attrs[key] != value:
				return False

	if text is not None:
		if element.text != text:
			return False

	return True


def parent_is(element, name=None, attributes=None, text=None):
	if element.parent is None:
		return False
	else:
		return element_is(element.parent, name=name, attributes=attributes, text=text)


def child_is(element, name=None, attributes=None, text=None):
	if hasattr(element, 'children'):
		return any([element_is(element=child, name=name, attributes=attributes, text=text) for child in element.children])
	else:
		return False


def element_has(element, name=None, attributes=None, text=None):
	if element.find(name=name, attributes=attributes or {}):
		for t in element.find_all(name=name, attributes=attributes or {}):
			if text is None:
				return True
			elif t.text == text:
				return True
	return False


def find_all(
		elements, name=None, attributes=None, text=None
):
	if isinstance(elements, (BeautifulSoup, Tag)):
		element = elements
		return [
			tag for tag in element.find_all(name=name, attrs=attributes or {})
			if element_is(element=tag, text=text)
		]
	else:
		return [
			tag
			for element in elements
			for tag in find_all(elements=element, name=name, attributes=attributes)
		]
