#!/usr/bin/env python3

import argparse
import os
import json 

from unidecode import unidecode

# conversions = {
# 	'\\\\' : '\\backslash ',

# 	# '`' : '$',

# 	'∃' : '\\exists ',
# 	'∄' : '\\nexists ',
# 	'∀' : '\\forall ',

# 	'∈' : '\\in ',
# 	'∉' : '\\notin ',

# 	'⊂' : '\\subset ',
# 	'⊆' : '\\subseteq ',
# 	'⊃' : '\\supset ',
# 	'⊇' : '\\supseteq ',

# 	'α' : '\\alpha ',
# 	'β' : '\\beta ',
# 	'γ' : '\\gamma ',
# 	'δ' : '\\delta ',
# 	'Δ' : '\\Delta ',
# 	'Θ' : '\\Theta ',
# 	'𝛝' : '\\vartheta ',
# 	'𝜗' : '\\vartheta ',
# 	'ω' : '\\omega ',
# 	'Ω' : '\\Omega ',
# 	'π' : '\\pi ',
# 	'ε' : '\\epsilon ',
# 	'φ' : '\\varphi ',
# 	'σ' : '\\sigma ',
# 	'λ' : '\\lambda ',
# 	'τ' : '\\tau ',

# 	'𝓘' : '\\mathcal{I}',
# 	'𝓙' : '\\mathcal{F}',
# 	'𝓕' : '\\mathcal{F}',


# 	'𝔼' : '\\mathbb{E}',
# 	'ℕ' : '\\mathbb{N}',
	

# 	'Σ' : '\\sum\\limits ',

# 	'<=>' : '\\iff ',
# 	'=>' : '\\implies ',
# 	'<=' : '\\impliedby ',
# 	'->' : '\\to ',

# 	'≐' : '\\doteq ',
	
# 	'&' : '\\&',
# 	'#' : '\\#',

# 	'⨄' : '\\uplus'
# }

sectionTypes = {
	'Df' : 'definition',
	'Th' : 'theorem',
	'Thm' : 'theorem',
	'Ob' : 'observation',
	'Ex' : 'example',
	'Vt' : 'theorem',
	'Pz' : 'observation',
	'Př' : 'example',
	'Alg' : 'algorithm',
	'Blk' : 'block'
}


# for filenames
sectionCodes = {
	'definition' : 'df',
	'theorem' : 'th',
	'observation' : 'ob',
	'example' : 'ex',
	'algorithm' : 'alg',
	'block' : 'misc'
}

subsectionTypes = {
	'Proof:' : 'proof',
	'Důkaz:' : 'proof'
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

		text = f'\n{whitespace}\\begin{{{keyword}}}\n\n'

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
		text = f'\n\\begin{{{subsectionTypes[self.type]}}}\n'

		for item in self.items:
			text += f'{item}\n'

		text += f'\\end{{{subsectionTypes[self.type]}}}\n'

		return text







class Line(Entry):
	def __init__(self, text):
		super().__init__()

		self.parseLine(replaceStrings(text))


	def __repr__(self):
		text = '\t' * self.indent

		for item in self.items:
			text += str(item)

		return text


	def addItem(self, item):
		if isinstance(item, str):
			if len(self.items) < 1 or not isinstance(self.items[-1], str):
				self.items.append('')

			self.items[-1] += str(item)

		else:
			self.items.append(item)


	def parseLine(self, line):
		blockDelimiters = {
			'`' : MathBlock,
			'¶' : TextBlock
		}

		i = 0

		while i < len(line):
			c = line[i]

			if c in blockDelimiters.keys():
				e = line.find(c, i + 1) # block end index

				block = blockDelimiters[c](line[i + 1:e])
				self.addItem(block)

				i = e + 1

			else:
				self.addItem(c)

				i += 1


			# if c in keyCharacters:
			# 	if c == '`':
			# 		blockType = MathBlock

			# 	elif c == '¶':
			# 		blockType = TextBlock

			# 	# block not opened, add to stack
			# 	if not isinstance(blockStack[-1], blockType):
			# 		block = blockType()
			# 		blockStack[-1].addItem(block)
			# 		blockStack.append(block)

			# 	# block closed, remove from stack
			# 	elif len(blockStack) > 1:
			# 		blockStack.pop()

			# else:
			# 	blockStack[-1].addItem(c)



class MathBlock(Line):
	def __repr__(self):
		text = '$'

		for item in self.items:
			text += str(item)

		text += '$'

		return text


class TextBlock(Line):
	def __repr__(self):
		text = '\\text{'

		for item in self.items:
			text += str(item)

		text += '}'

		return text	





class Section:
	def __init__(self, title, sectionType):
		self.title = title
		self.type = sectionType
		self.items = []
		self.count = None


	def __repr__(self):
		name = replaceStrings(self.title) if len(self.title) > 0 else str(self.count)

		# if self.type != None:
		text = f'\\begin{{{self.type}}}[{name}]\n\n' 
		# else:
			# text = f'\\subsection*{{{replaceStrings(self.title)}}}\n\n'

		for item in self.items:
			text += str(item)

		# if self.type != None:
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



def extractSectionTitleAndType(line):
	parts = line.split(':')

	if len(parts) < 2:
		return line, 'block'

	prefix = parts[0]
	title = ' '.join(parts[1:]).strip()

	if prefix in sectionTypes:
		return title, sectionTypes[prefix]

	return title, 'block'


def sanitizeString(s):
	o = ''

	for c in s:
		if c.isalnum() or c == ' ':
			o += c

	return unidecode(o)



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
	indent = len(line) - len(line.lstrip())

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
		if len(lines[0].lstrip()) < 1:
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
			section = Section('', 'block')
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



def merge(args):
	merged = ''


	for filename in sorted(os.listdir(args.input)):
		path = os.path.join(args.input, filename)

		if os.path.isfile(path) and os.path.splitext(path)[-1] == '.md':
			with open(path, 'r') as inFile:
				text = inFile.read()

				lines = text.splitlines()
				lines = lines[args.strip_top : len(lines) - args.strip_bottom + 1]

				text = '\n'.join(lines)

				merged += text + '\n'

	if args.output != '':
		with open(args.output, 'w') as outFile:
			outFile.write(merged)


def convert(args):
	with open(args.input, 'r') as file:
		text = file.read()

	document = Document(args.title, text)
	document.save(args.output)


def replaceStrings(text):
	for c in conversions:
		text = text.replace(c, conversions[c])

	return text


def main():
	parser = argparse.ArgumentParser(
			prog = 'texdown',
			description = 'Converts specially formated markdown to latex.'
		)

	parser.add_argument('-i', '--input', default='', type=str, help='Input file path')
	parser.add_argument('-o', '--output', default='', type=str, help='Output file path')
	parser.add_argument('-t', '--title', default='', type=str, help='Document title')
	parser.add_argument('-m', '--merge', default=False, type=str, help='Document title')
	parser.add_argument('-c', '--convert', default=False, type=str, help='Document title')
	parser.add_argument('-st', '--strip_top', default=0, type=int, help='Number of lines to remove from the top')
	parser.add_argument('-sb', '--strip_bottom', default=0, type=int, help='Number of lines to remove from the bottom')
	parser.add_argument('-l', '--language', default='EN', type=str, choices=['EN', 'CZ'], help='Formatting language')

	args = parser.parse_args()

	if args.merge:
		merge(args)

	elif args.convert:
		scriptPath = os.path.join(os.path.split(__file__)[0], 'stringMap.json')

		with open(scriptPath, 'r') as file:
			global conversions
			conversions = json.load(file)

		convert(args)

	return



if __name__ == '__main__':
	main()

