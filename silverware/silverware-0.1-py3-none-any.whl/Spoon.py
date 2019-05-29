from .find_all import find_all, element_is, element_has, parent_is, child_is
from .find_between import find_between, find_after, find_before
from .find_between import get_ancestors
from .find_between import get_siblings, get_preceding_siblings, get_succeeding_siblings
from .clone_beautiful_soup_tag import clone_beautiful_soup_tag
from .find_links import find_links
from bs4 import BeautifulSoup, Tag
import warnings


class Spoon:
	def __init__(self, soup):
		"""
		:param list[Tag] or list[BeautifulSoup] or Tag or BeautifulSoup soup:
		"""
		if isinstance(soup, (Tag, BeautifulSoup)):
			self._soup = soup
		else:
			self._soup = list(soup)

	@property
	def soup(self):
		"""
		:rtype: BeautifulSoup
		"""
		return self._soup

	def is_single(self):
		return isinstance(self._soup, (Tag, BeautifulSoup))

	@classmethod
	def clone(cls, soup, in_spoon=False):
		if isinstance(soup, cls):
			soup = soup.soup
		result = clone_beautiful_soup_tag(elements=soup)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def copy(self):
		return self.clone(soup=self.soup, in_spoon=True)

	@classmethod
	def filter(cls, soup, name=None, attributes=None, text=None, in_spoon=True):
		if isinstance(soup, cls):
			soup = soup.soup
		result = find_all(elements=soup, name=name, attributes=attributes, text=text)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def find_all(self, name=None, attributes=None, text=None, in_spoon=True):
		return self.filter(soup=self.soup, name=name, attributes=attributes, text=text, in_spoon=in_spoon)

	@classmethod
	def after(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = find_after(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_after(self, in_spoon=True):
		return self.after(element=self, in_spoon=in_spoon)

	@classmethod
	def before(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = find_before(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_before(self, in_spoon=True):
		return self.before(element=self, in_spoon=in_spoon)

	@classmethod
	def between(cls, element1, element2, in_spoon=True):
		if isinstance(element1, cls):
			element1 = element1.soup
		if isinstance(element2, cls):
			element2 = element2.soup
		result = find_between(element1=element1, element2=element2)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	@classmethod
	def parent(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = element.parent
		if result is None:
			warnings.warn('element does not have a parent!')
			result = element
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_parent(self, in_spoon=True):
		return self.parent(element=self.soup, in_spoon=in_spoon)

	@classmethod
	def children(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = element.children
		if result is None:
			raise RuntimeError('element does not have a children attribute!')
		elif len(result) == 0:
			warnings.warn('element does not have children!')
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	@classmethod
	def ancestors(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = get_ancestors(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_ancestors(self, in_spoon=True):
		return self.ancestors(element=self.soup, in_spoon=in_spoon)

	@classmethod
	def siblings(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = get_siblings(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_siblings(self, in_spoon=True):
		return self.siblings(element=self.soup, in_spoon=in_spoon)

	@classmethod
	def preceding_siblings(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = get_preceding_siblings(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_preceding_siblings(self, in_spoon=True):
		return self.preceding_siblings(element=self.soup, in_spoon=in_spoon)

	@classmethod
	def succeeding_siblings(cls, element, in_spoon=True):
		if isinstance(element, cls):
			element = element.soup
		result = get_succeeding_siblings(element=element)
		if in_spoon:
			return cls(soup=result)
		else:
			return result

	def get_succeeding_siblings(self, in_spoon=True):
		return self.succeeding_siblings(element=self.soup, in_spoon=in_spoon)

	@property
	def text(self):
		return self.soup.text

	@property
	def attributes(self):
		return self.soup.attrs

	def __getitem__(self, item):
		return self.soup[item]

	def element_is(self=None, element=None, name=None, attributes=None, text=None):
		if self is not None:
			element = element or self.soup
		return element_is(element=element, name=name, attributes=attributes, text=text)

	def parent_is(self=None, element=None, name=None, attributes=None, text=None):
		if self is not None:
			element = element or self.soup
		return parent_is(element=element, name=name, attributes=attributes, text=text)

	def child_is(self=None, element=None, name=None, attributes=None, text=None):
		if self is not None:
			element = element or self.soup
		return child_is(element=element, name=name, attributes=attributes, text=text)

	@classmethod
	def element_has(cls, element, name=None, attributes=None, text=None):
		if isinstance(element, cls):
			element = element.soup
		return element_has(element=element, name=name, attributes=attributes, text=text)

	def has(self, name=None, attributes=None, text=None):
		return self.element_has(element=self.soup, name=name, attributes=attributes, text=text)

	def find_links(self=None, element=None, base_url=None):
		if self is not None:
			element = element or self.soup
		return find_links(element=element, base=base_url)