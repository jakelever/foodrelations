import argparse
import bioc
import json
import itertools
from collections import defaultdict,Counter

def getID_FromLongestTerm(text, lookupDict):
	"""
	Given a span of text, this method will tokenize and then identify the set of entities that exist in the text. It will prioritise long terms first in order to reduce ambiguity.

	Example: For the text "the cheese pizza is good" and the lookup dict of {("cheese","pizza"):1, ("pizza",):2}, the algorithm will identify "cheese pizza" as an entity with ID 1. Those tokens will then be removed, and so "pizza" will not be identified.

	:param text: The text span to be searched. It will be tokenized using the very naive method of splitting by whitespace.
	:param lookupDict: Dictionary that maps tokenized terms to a particular ID
	:type text: str
	:type lookupDict: dict with tuple keys
	:returns: IDs of all entities identified in text
	:rtype: set
	"""

	terms = set()

	# Lowercase and do very naive tokenization of the text
	np = text.lower().split()

	# The length of each search string will decrease from the full length
	# of the text down to 1
	for l in reversed(range(1, len(np)+1)):
		# We move the search window through the text
		for i in range(len(np)-l+1):
			# Extract that window of text
			s = tuple(np[i:i+l])
			# Search for it in the dictionary
			if s in lookupDict:
				sTxt = " ".join(np[i:i+l])

				for wordlistid,tid in lookupDict[s]:
					#myTxt = "%s\t%s" % (tid,sTxt)
					#terms.add((wordlistid,myTxt))
					terms.add((wordlistid,sTxt))
				# If found, save the ID(s) in the dictionar
				#terms.update(lookupDict[s])
				
				# And blank it out
				np[i:i+l] = [ "" for _ in range(l) ]

	return terms

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Count cooccurrences between different terms within passages of a BioC-format corpus file. This uses a very naive method for tokenization (a simple white-space split) which should be replaced with a CoreNLP/Spacy implementation for real-world usage.')
	parser.add_argument('--biocFile',required=True,type=str,help='BioC file to use')
	parser.add_argument('--wordlist1',required=True,type=str,help='First wordlist to use (in JSON format)')
	parser.add_argument('--wordlist2',required=True,type=str,help='Second wordlist to use (in JSON format)')
	parser.add_argument('--outFile',required=True,type=str,help='File to output cooccurrence counts to')

	args = parser.parse_args()

	print("Loading wordlist...")
	with open(args.wordlist1) as f:
		wordlist1 = json.load(f)
	with open(args.wordlist2) as f:
		wordlist2 = json.load(f)

	lookup = defaultdict(set)
	
	print("Tokenizing wordlists...")
	for id,terms in wordlist1.items():
		for term in terms:
			tokenized = term.lower().split()
			lookup[tuple(tokenized)].add( (1,id) )
	
	for id,terms in wordlist2.items():
		for term in terms:
			tokenized = term.lower().split()
			lookup[tuple(tokenized)].add( (2,id) )

	print("Processing document...")
	cooccurrences = Counter()
	with bioc.iterparse(args.biocFile) as parser:
		collection_info = parser.get_collection_info()
		for docid,document in enumerate(parser):
			if docid != 0 and (docid % 1000) == 0:
				print("   %d documents complete" % docid)

			for passage in document.passages:
				# Identify which terms appear in the passage (and find the longest terms first in order to avoid ambiguity)
				termids = getID_FromLongestTerm(passage.text,lookup)

				term1ids = [ id for wordlistid,id in termids if wordlistid == 1 ]
				term2ids = [ id for wordlistid,id in termids if wordlistid == 2 ]

				termids = sorted(termids)
				for a,b in itertools.product(term1ids,term2ids):
					cooccurrences[(a,b)] += 1

	print("Writing cooccurrences to file")
	with open(args.outFile,'w') as outF:
		for (a,b),count in cooccurrences.items():
			outF.write("%s\t%s\t%d\n" % (a,b,count))

	print("Complete.")


