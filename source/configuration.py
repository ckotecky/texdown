#!/usr/bin/env python3


stringMap = {
	'\\\\' : '\\backslash ',

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

	'𝓘' : '\\mathcal{I}',
	'𝓙' : '\\mathcal{F}',
	'𝓕' : '\\mathcal{F}',


	'𝔼' : '\\mathbb{E}',
	'ℕ' : '\\mathbb{N}',
	

	'Σ' : '\\sum\\limits ',

	'<=>' : '\\iff ',
	'=>' : '\\implies ',
	'<=' : '\\impliedby ',
	'->' : '\\to ',

	'≐' : '\\doteq ',
	
	'&' : '\\&',
	'#' : '\\#',

	'⨄' : '\\uplus'
}

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


def main():
	import json

	with open('stringMap.json', 'w') as file:
		json.dump(stringMap, file, indent=4)

	with open('sectionTypes.json', 'w') as file:
		json.dump(sectionTypes, file, indent=4)

	with open('sectionCodes.json', 'w') as file:
		json.dump(sectionCodes, file, indent=4)

	with open('subsectionTypes.json', 'w') as file:
		json.dump(subsectionTypes, file, indent=4)



if __name__ == '__main__':
	main()