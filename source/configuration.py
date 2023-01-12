#!/usr/bin/env python3


# order matters: Σ_ must be before Σ
stringMap = {
	# '\\\\' : '\\backslash ',
	' \\ ' : ' \\backslash ',
	'`' : '$',
	'\t' : '\\quad ',
	'  ' : '\\; ',
	'   ' : '\\enskip ',
	
	'Σ_' : '\\sum\\limits_',
	'π_' : '\\prod\\limits_',

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
	'Σ' : '\\Sigma ',
	'λ' : '\\lambda ',
	'τ' : '\\tau ',
	'π' : '\\pi ',

	'𝓘' : '\\mathcal{I}',
	'𝓙' : '\\mathcal{F}',
	'𝓕' : '\\mathcal{F}',


	'𝔼' : '\\mathbb{E}',
	'ℕ' : '\\mathbb{N}',

	'<=>' : '\\iff ',
	'=>' : '\\implies ',
	'<=' : '\\impliedby ',
	'->' : '\\to ',

	'≐' : '\\doteq ',
	
	'&' : '\\&',
	'#' : '\\#',

	'⨄' : '\\uplus',
	'∪' : '\\cup',
	'∩' : '\\cap'
}

sectionTypes = {
	'Df' : 'definition',
	'Th' : 'theorem',
	'Thm' : 'theorem',
	'Lm' : 'lemma',
	'Ob' : 'observation',
	'Ex' : 'example',
	'Vt' : 'theorem',
	'Pz' : 'observation',
	'Pb' : 'problem',
	'Př' : 'example',
	'Alg' : 'algorithm',
	'Ds' : 'corollary',
	'Cr' : 'corollary',
	'Fakt' : 'fact',
	'Nt' : 'note',
	'Blk' : 'block'
}


# for filenames
sectionCodes = {
	'definition' : 'df',
	'theorem' : 'th',
	'note' : 'nt',
	'observation' : 'ob',
	'lemma' : 'lm',
	'example' : 'ex',
	'algorithm' : 'alg',
	'corollary' : 'cr',
	'problem' : 'pb',
	'fact' : 'fact',
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