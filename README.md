# Food Relations

This project is a demonstration of a very basic text mining approach to extract nutrigenomics data from [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) and [AGRICOLA](https://agricola.nal.usda.gov/) abstracts. It uses the [PubRunner project](https://github.com/jakelever/pubrunner) to make it easy to run the text mining tools on both corpora without having to deal with format conversions.

## How it works.

The diagram below outlines the key concepts of the project. The first stage involves the cooccurrenceExtractor.py script. It loads drug terms from [PubChem](https://pubchem.ncbi.nlm.nih.gov/) and a list of food items from the [Food Ontology](https://github.com/FoodOntology/foodon). It then loads each document and identifies all the drug and food terms using dictionary matching. It then outputs all the cooccurrences of these terms. This first stage is run multiple times for all the document files provided. The second stage uses the combineCooccurrences.py script. It takes the output of the multiple runs of the first stage and combines them together.

## Dependendencies

This project has a couple dependencies:
- PubRunner (which can be installed using pip)
- AGRICOLA (which is not currently publically available)

## Execution

With PubRunner installed, the test case can be run as follows

```
pubrunner --test .
```

Remove the "--test" to execute the very large full run.

## Technical Details

The two scripts cooccurrenceExtractor.py and combineCooccurrences.py are both short and contain comments on how they work. The other key file is pubrunner.yml which describes the resources and commands that PubRunner needs to run the project.
