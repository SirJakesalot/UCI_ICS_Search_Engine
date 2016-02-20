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
        __doc_id: The current available unused document ID. Also represents the amount 
            of unique documents found so far (__doc_id - 1).
        __term_id: The current available unused term ID. Also represents the amount of 
            unique terms found so far (__term_id - 1).
        doc_id_lookup: Dictionary mapping document URLs to their document ID {URL : doc_id}.
        term_id_lookup: Dictionary mapping terms to their term ID {term : term_id}.
        indexer: Dictionary mapping term IDs to their dictionary of document IDs to the 
            frequency count within that same document {term_id : {doc_id : frequency}}.
    """

    def __init__(self):
        """Inits term and document ID to 1 and the lookup datastructures to dictionaries."""
        self.__doc_id = 1
        self.__term_id = 1
        self.doc_id_lookup = dict()
        self.term_id_lookup = dict()
        self.indexer = dict()

    #
    # Processing functions.
    #
    def processPage(self, file_name):
        """Processes the page.

        Processes the page by stripping the read lines of whitespace and non-alphanumeric 
        characters. The stripped terms are then saved into the indexer data structure.

        Args:
            file_name: The name of the file to be processed.
        """
        with open(file_name, 'r') as f:
            # First line holds the URL of the page
            url = f.readline().strip()
            self.doc_id_lookup[url] = self.__doc_id
            
            lines = f.readlines()
            for line in lines:
                for word in re.sub("[^0-9a-zA-Z]+", " ", line).split(" "):
                    self.__add_word(word)
            self.__doc_id += 1

    def __add_word(self, word):
        """Processes the word into a proper term.

        Lowercases and strips it of any non-alphanumeric characters, then stores the
        new term into its appropriate dictionary.

        Args:
            word: The word to be processed.
        """
        word = word.lower().strip()
        if len(word) != 0:
            if word not in self.term_id_lookup:
                self.term_id_lookup[word] = self.__term_id
                self.indexer[self.__term_id] = defaultdict(lambda: 0)
                self.__term_id += 1
            self.indexer[self.term_id_lookup[word]][self.__doc_id] += 1

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

    def save_indexer_to_files(self):
        """Writes the index data to a file.

        Writes out to the file by temporarily redirecting the stdout to the given
        file.

        Files written:
            index.txt - Contains the indexer data
            terms.txt - Contains the term to term_id data
            docs.txt - Contains the doc to doc_id data

        Args:
            file_name: The name of the file to be written to.
        """
        stdout = sys.stdout
        files = [("index.txt", self.print_indexer),
                 ("terms.txt", self.print_term_lookup),
                 ("docs.txt", self.print_doc_lookup)]

        for name,func in files:
            with open(name, "w") as f:
                sys.stdout = f
                func()

        sys.stdout = stdout


    #
    # Getter functions.
    #
    @property
    def num_terms(self):
        """Returns the amount of unique terms found."""
        return self.__term_id - 1

    @property
    def num_docs(self):
        """Returns the amount of unique documents found."""
        return self.__doc_id - 1

    def get_inverse_term_lookup(self):
        """Returns an inverse dictionary of term_id_lookup {term_id : term}."""
        return {v : k for k,v in self.term_id_lookup.items()}

    def get_inverse_doc_lookup(self):
        """Returns an inverse dictionary of doc_id_lookup {doc_id : doc}"""
        return {v : k for k,v in self.doc_id_lookup.items()}       


    #
    # Printing functions.
    #
    def print_term_lookup(self, by_id=True):
        """Prints the key, value pairs of term_id_lookup.

        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k,v in sorted(self.term_id_lookup.items(), key=lambda x: x[by_id]):
            print "({} : {})".format(k,v)

    def print_doc_lookup(self, by_id=True):
        """Prints the key, value pairs of doc_id_lookup.

        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k,v in sorted(self.doc_id_lookup.items(), key=lambda x: x[by_id]):
            print "({} : {})".format(k,v)

    def print_inverse_term_lookup(self, by_id=True):
        """Prints the inverse key, value pairs of term_id_lookup.
        
        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k,v in sorted(self.get_inverse_term_lookup().items(), key=lambda x: x[not by_id]):
            print "({} : {})".format(k,v)

    def print_inverse_doc_lookup(self, by_id=True):
        """Prints the inverse key, value pairs of doc_id_lookup.
        
        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k,v in sorted(self.get_inverse_doc_lookup().items(), key=lambda x: x[not by_id]):
            print "({} : {})".format(k,v)

    def print_indexer(self, print_word=False):
        """Prints the key, value pairs of the indexer.

        The format for the index is {term_id : {doc_id, frequency}}. In English, each term_id
        has dictionary values which indicates its frequency in a specific document.

        Args:
            with_word: Flag indicating if the user wants to print out the actual word along
            with the term.
        """
        for k,v in self.indexer.items():
            term = self.get_inverse_term_lookup()[k] if print_word else ""
            print "({} {} : ({})".format(k, term, dict(v))


if __name__ == "__main__":
    indexer = Indexer()
    indexer.handleDir("data/xtune.ics");

    print indexer.num_docs
    print indexer.num_terms

    indexer.save_indexer_to_files()
