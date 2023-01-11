import json

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


with open('stringMap.json', 'w') as file:
	json.dump(stringMap, file, indent=4)




