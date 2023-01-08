#!/usr/bin/env python3

import argparse
import os
from itertools import pairwise


parser = argparse.ArgumentParser()
parser.add_argument('--input', default='', type=str, help='Input file path')
parser.add_argument('--output', default='', type=str, help='Output file path')
parser.add_argument('--title', default='', type=str, help='Document title')


conversions = {
	'`' : '$',

	'∃' : '\\exists ',
	'∄' : '\\nexists ',
	'∀' : '\\forall ',

	'∈' : '\\in ',
	'∉' : '\\notin ',

	'⊂' : '\\subset ',
	'⊆' : '\\subseteq ',
	'⊃' : '\\supset ',
	'⊇' : '\\supseteq ',

	'α' : '\\alpha ',
	'β' : '\\beta ',
	'γ' : '\\gamma ',
	'δ' : '\\delta ',
	'Δ' : '\\Delta ',
	'Θ' : '\\Theta ',
	'𝛝' : '\\vartheta ',
	'𝜗' : '\\vartheta ',
	'ω' : '\\omega ',
	'Ω' : '\\Omega ',
	'π' : '\\pi ',
	'ε' : '\\epsilon ',
	'φ' : '\\varphi ',
	'σ' : '\\sigma ',
	'λ' : '\\lambda ',
	'τ' : '\\tau ',

	'𝓙' : '\\mathcal{F}',



	'𝔼' : '\\mathbb{E}',
	'ℕ' : '\\mathbb{N}',
	

	'Σ' : '\\sum\\limits ',

	'<=>' : '\\iff ',
	'=>' : '\\implies ',
	'<=' : '\\impliedby ',
	'->' : '\to ',

	'≐' : '\\doteq ',
	
	'&' : '\\&',
	'#' : '\\#'
}

sectionTypes = {
	'Df' : 'definition',
	'Th' : 'theorem',
	'Thm' : 'theorem',
	'Ob' : 'observation',
	'Ex' : 'example'
}


sectionCodes = {
	'definition' : 'df',
	'theorem' : 'th',
	'observation' : 'ob',
	'example' : 'ex',
	None : 'misc'
}

subsectionTypes = {
	'Proof:' : 'proof'
}




class Entry:
	def __init__(self):
		self.items = []
		self.indent = 0


	def __repr__(self):
		text = ''

		for item in self.items:
			text += f'{item}\n'

		text += '\n'

		return text


	def addItem(self, item):
		self.items.append(item)


class ListItem(Entry):
	def __init__(self, itemType):
		super().__init__()

		self.type = itemType


	def __repr__(self):
		whitespace = '\t' * (self.indent + 1)
		
		text = f'{whitespace}\\item '

		for item in self.items:
			text += f'{item}'

		return text


class BulletList(Entry):
	def __init__(self, enumerated):
		super().__init__()

		self.enumerated = enumerated


	def __repr__(self):
		whitespace = '\t' * self.indent
		keyword = 'enumerate' if self.enumerated else 'itemize'

		text = f'{whitespace}\\begin{{{keyword}}}\n\n'

		if self.indent < 1:
			text += f'{whitespace}\\itemsep0em\n\n'

		for item in self.items:
			text += f'{item}\n'

		text += f'{whitespace}\\end{{{keyword}}}\n'

		return text


class Subsection(Entry):
	def __init__(self, subsectionType):
		super().__init__()

		self.type = subsectionType


	def __repr__(self):
		text = f'\\begin{{{subsectionTypes[self.type]}}}\n'

		for item in self.items:
			text += f'{item}\n'

		text += f'\\end{{{subsectionTypes[self.type]}}}\n'

		return text


class Line(Entry):
	def __init__(self, text):
		super().__init__()

		self.text = text


	def __repr__(self):
		whitespace = '\t' * self.indent
		
		return f'{whitespace}{replaceStrings(self.text)}\n'


class Section:
	def __init__(self, title, sectionType):
		self.title = title
		self.type = sectionType
		self.items = []
		self.count = None


	def __repr__(self):
		name = replaceStrings(self.title) if len(self.title) > 0 else str(self.count)

		if self.type != None:
			text = f'\\begin{{{self.type}}}[{name}]\n\n' 
		else:
			text = f'\\subsection*{{{replaceStrings(self.title)}}}\n\n'

		for item in self.items:
			text += str(item)

		if self.type != None:
			text += f'\\end{{{self.type}}}\n' 

		return text


	def addItem(self, item):
		self.items.append(item)


	def fileName(self):
		name = '_'.join(sanitizeString(self.title).split()).lower() if len(self.title) > 0 else str(self.count)

		return f'{sectionCodes[self.type]}-{name}'


	def save(self, path):
		with open(f'{path}/{self.fileName()}.tex', 'w') as f:
			f.write(str(self))



class Document:
	def __init__(self, title, text):
		self.title = title
		self.chapters = parse(text)


	def __repr__(self):
		text = ''

		for chapter in self.chapters:
			text += f'\\subfile{{chapters/{chapter.fileName()}/main.tex}}\n\n'
			text += '\\pagebreak\n\n'

		return text	


	def addChapter(self, chapter):
		self.chapters.append(chapter)


	def save(self, path):
		chapterPath = path + '/chapters'

		if not os.path.exists(chapterPath):
			os.mkdir(chapterPath)

		for chapter in self.chapters:
			chapter.save(chapterPath)

		with open(chapterPath + '.tex', 'w') as f:
			f.write(str(self))


class Chapter:
	def __init__(self, title):
		self.title = title
		self.sections = []
		self.count = None


	def __repr__(self):
		text = '\\begin{center}\n'
		text += f'\\section{{{replaceStrings(self.title)}}}\n'
		text += '\\hrule\n'
		text += '\\end{center}\n\n'

		for section in self.sections:
			text += f'\\subfile{{elements/{section.fileName()}.tex}}\n'

		return text	
	

	def addSection(self, section):
		self.sections.append(section)


	def fileName(self):
		name = str(self.count) + '-' + '_'.join(sanitizeString(self.title).split()).lower()

		return name


	def save(self, path):
		name = self.fileName()
		path += f'/{name}'

		if not os.path.exists(path):
			os.mkdir(path)

		elementPath = f'{path}/elements'

		if not os.path.exists(elementPath):
			os.mkdir(elementPath)

		for section in self.sections:
			section.save(elementPath)

		with open(path + f'/main.tex', 'w') as f:
			f.write(str(self))


def replaceStrings(text):
	for c in conversions:
		text = text.replace(c, conversions[c])

	return text



def extractSectionTitleAndType(line):
	parts = line.split(':')

	if len(parts) < 2:
		return line, None

	prefix = parts[0]
	title = ' '.join(parts[1:]).strip()

	if prefix in sectionTypes:
		return title, sectionTypes[prefix]

	return title, None


def sanitizeString(s):
	o = ''

	for c in s:
		if c.isalnum():
			o += c

	return o



def extractEntry(lines):
	if len(lines) > 1:
		firstLine = lines[0]
		secondLine = lines[1]

		if secondLine.startswith('==='): # chapter
			entry = Chapter(firstLine)

			return 0, entry, lines[2:]
			
		elif secondLine.startswith('---'): # section
			sectionTitle, sectionType = extractSectionTitleAndType(firstLine)
			entry = Section(sectionTitle, sectionType)

			return 0, entry, lines[2:]

	line = lines[0]
	indent = len(line) - len(line.strip())

	suffix, itemType = identifyList(line)

	if itemType != None: # list item
		entry = ListItem(itemType)
		entry.addItem(Line(suffix))

		return indent, entry, lines[1:]

	elif line.startswith('###'): # subsection (proof)
		title = line.split(' ')[1]
		entry = Subsection(title)

		return 0, entry, lines[1:]

	else: # only text
		entry = Line(line)

	return indent, entry, lines[1:]




def identifyList(line):
	l = line.split()

	if len(line) < 1 or len(l) < 1:
		return line, None

	prefix = l[0]
	suffix = ' '.join(l[1:])

	listType = None

	if prefix[-1] == '.' and prefix[:-1].isnumeric():
		number = int(prefix[:-1])

		listType = number
		# print(number, suffix)

	elif prefix == '-':
		listType = '-'

	elif prefix == '+':
		listType = '+'

	elif prefix == '*':
		listType = '*'

	return suffix, listType


def parse(text):
	lines = text.splitlines()

	chapters = []
	listStack = []
	indentLengths = {}

	chapter = None
	section = None
	subsection = None

	sectionCount = 0

	while len(lines) > 0:
		if len(lines[0].strip()) < 1:
			lines = lines[1:]

			continue

		indent, entry, lines = extractEntry(lines)

		if isinstance(entry, Chapter): # start chapter
			chapter = entry
			section = None
			subsection = None

			sectionCount = 0

			listStack = []
			indentLengths = {}

			chapters.append(chapter)
			chapter.count = len(chapters)

			continue

		if chapter == None: # start implicit chapter
			chapter = Chapter('')
			section = None
			subsection = None

			sectionCount = 0

			listStack = []
			indentLengths = {}

			chapters.append(chapter)
			chapter.count = len(chapters)

		if isinstance(entry, Section): # start section
			section = entry
			subsection = None

			section.count = sectionCount
			sectionCount += 1

			listStack = []
			indentLengths = {}

			chapter.addSection(section)

			continue

		if section == None: # start implicit section
			section = Section('', None)
			subsection = None

			section.count = sectionCount
			sectionCount += 1

			listStack = []
			indentLengths = {}

			chapter.addSection(section)

		if isinstance(entry, Subsection): # start subsection
			subsection = entry

			listStack = []
			indentLengths = {}

			section.addItem(subsection)

			continue

		# list or text
		# pop stack until stack's top indent is same or lower
		while len(listStack) > 0 and indentLengths[len(listStack) - 1] > indent:
			listStack.pop()
			indentLengths.pop(len(listStack))

		# if there is a list in the stack with same or lower indent as the current, start a new list or continue previous
		if isinstance(entry, ListItem): 
			if len(listStack) > 0 and indentLengths[len(listStack) - 1] == indent:
				# if the current entry continues the previous list, add to that list
				# continues enumeration
				if isinstance(entry.type, int) and entry.type - 1 == listStack[-1].items[-1].type:
					listStack[-1].addItem(entry)
					entry.indent = indent

					continue

				# continues itemization
				elif entry.type == listStack[-1].items[-1].type:
					listStack[-1].addItem(entry)
					entry.indent = indent

					continue

				# does not continue, remove previous list form stack
				else:
					listStack.pop()
					indentLengths.pop(len(listStack))					

			# if new list was started, convert item to list
			bulletList = BulletList(isinstance(entry.type, int))
			bulletList.addItem(entry)

			entry.indent = len(listStack)
			entry = bulletList

		# if list stack still not empty, nest into list and end
		if len(listStack) > 0:
			listStack[-1].items[-1].addItem(entry)
			entry.indent = len(listStack)

			if isinstance(entry, BulletList):
				indentLengths.update({len(listStack) : indent})
				listStack.append(entry)

			continue

		# if list stack was empty, add to section or subsection
		section.addItem(entry)
		entry.indent = 0

		# has to be repeated separately?
		if isinstance(entry, BulletList):
			indentLengths.update({len(listStack) : indent})
			listStack.append(entry)

		continue

	return chapters




def main(args: argparse.Namespace):
	with open(args.input, 'r') as file:
		text = file.read()

	document = Document(args.title, text)
	document.save(args.output)

	return



if __name__ == '__main__':
	args = parser.parse_args([] if "__file__" not in globals() else None)

	main(args)

