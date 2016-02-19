"""
@Authors:
Jacob Armentrout    66598462
Gillian Bendicio    56433482
Jennifer Chew       53649288
Vinh Vu             21775557

@Created: 02/18/16

@Source: Indexer.py
"""

import os
import re
import sys
from collections import defaultdict

class Indexer():
    """Indexer class for the search engine index.

    Provides all methods and datastructures to appropriately process, index and store 
    terms and documents which will be later used to provide a functional search engine.

    Attributes:
        doc_id: The current available unused document ID. Also represents the amount 
            of unique documents found so far (doc_id - 1).
        term_id: The current available unused term ID. Also represents the amount of 
            unique terms found so far (term_id - 1).
        doc_id_lookup: Dictionary mapping document URLs to their document ID {URL : doc_id}.
        term_id_lookup: Dictionary mapping terms to their term ID {term : term_id}.
        indexer: Dictionary mapping term IDs to their dictionary of document IDs to the 
            frequency count within that same document {term_id : {doc_id : frequency}}.
    """

    def __init__(self):
        """Inits term and document ID to 1. The lookup datastructures to dictionaries."""
        self.doc_id = 1
        self.term_id = 1
        self.doc_id_lookup = dict()
        self.term_id_lookup = dict()
        self.indexer = dict()

    def processPage(self, file_name):
        """Processes the page.

        Processes the page by stripping the read lines of whitespace and non-alphanumeric 
        characters. The stripped terms are then saved into the indexer data structure.

        Args:
            file_name: The name of the file to be processed.
        """
        with open(file_name, 'r') as f:
            # First line holds the URL of the page
            url = f.readline()
            print "url", url
            self.doc_id_lookup[url] = self.doc_id
            
            lines = f.readlines()
            for line in lines:
                for word in line.split(" "):
                    s = re.sub('[^0-9a-zA-z]+', '', word)
                    if len(s) != 0:
                        if s not in self.term_id_lookup:
                            self.term_id_lookup[s] = self.term_id
                            self.indexer[self.term_id] = defaultdict(lambda: 0)
                            self.term_id += 1
                        self.indexer[self.term_id_lookup[s]][self.doc_id] += 1
            self.doc_id += 1

    def handleDir(self, dirname):
        """Opens the file/directory for processessing.

        Opens the directory and lists all the files/directories for processing.
        Recursively calls into any directories found, otherwise calls handleFile().
        
        Args:
            dirname: The name of the directory to be processed.
        """
        for dirpath, directories, files in os.walk(dirname):
            for f in files:
                self.processPage(os.path.join(dirpath, f))
            for d in directories:
                new_path = os.path.join(dirpath, d)
                print "New path: " + new_path
                self.handleDir(new_path)

    def get_inverse_term_lookup(self):
        """Returns an inverse dictionary of term_id_lookup: term_id -> term."""
        return {v : k for k,v in self.term_id_lookup.items()}

    def get_inverse_doc_lookup(self):
        """Returns an inverse dictionary of doc_id_lookup: doc_id -> doc."""
        return {v : k for k,v in self.doc_id_lookup.items()}       


if __name__ == "__main__":
    indexer = Indexer()
    indexer.handleDir("test");
    terms = indexer.term_id_lookup
    for k,v in indexer.get_inverse_term_lookup().items():
        print "key", k
        print v

    """
    for key,val in sorted(indexer.indexer.items()):
        print "Inverse TermId: " + str(key) + " term: " + indexer.inverse_term_id_lookup[key] 
        for vkey, v in val.items():
            print "DocId", str(vkey), "doc:", indexer.inverse_doc_id_lookup[vkey], "frequency", str(v)
    for k,v in sorted(terms.items(), key=lambda x: x[1][1]):
        print("Key:", k)
        print(v)'''
    """
