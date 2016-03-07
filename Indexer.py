#!/usr/bin/python
###########################################################
# @Authors:
# Jacob Armentrout    66598462
# Gillian Bendicio    56433482
# Jennifer Chew       53649288
# Vinh Vu             21775557
#
# @Created: 02/18/16
# @Source: Indexer.py
###########################################################

import os
import re
import sys
import copy
import math
import time
import shutil
from collections import defaultdict


class Indexer:
    """Indexer class for the search engine index.

    Provides all methods and data structures to appropriately process, index and store
    terms and documents which will be later used to provide a functional search engine.

    Attributes:
        __doc_id: The current available unused document ID. Also represents the amount 
            of unique documents found so far (__doc_id - 1).
        __term_id: The current available unused term ID. Also represents the amount of 
            unique terms found so far (__term_id - 1).
        doc_id_lookup: Dictionary mapping document URLs to their document ID {URL : doc_id}.
        term_id_lookup: Dictionary mapping terms to their term ID {term : term_id}.
        doc_term_count: Dictionary mapping documents to their word count {doc_id : count}.
        indexer: Dictionary mapping term IDs to their dictionary of document IDs to the 
            frequency count within that same document {term_id : {doc_id : frequency}}.
        tf_idf: Dictionary mapping term IDs to their dictionary of document IDs to the
            TF-IDF (Term Frequency - Inverse Document Frequency) {term_id: {doc_id : tf-idf}}.
    """

    def __init__(self):
        """Initializes term and document ID to 1 and the lookup data structures to dictionaries."""
        self.__doc_id = 1
        self.__term_id = 1
        self.doc_id_lookup = dict()
        self.term_id_lookup = dict()
        self.doc_term_count = dict()
        self.indexer = dict()
        self.tf_idf = dict()
       
        # Added by Jake 
        self.indexer_path = "Indexer_Data"

    #
    # Processing functions.
    #
    def process_page(self, file_name):
        """Processes the page.

        Processes the page by stripping the read lines of whitespace and non-alphanumeric 
        characters. The stripped terms are then saved into the indexer data structure.

        Args:
            file_name: The name of the file to be processed.
        """
        with open(file_name, 'r') as f:
            # First line holds the URL of the page
            url = f.readline().strip()
            word_count = 0
            self.doc_id_lookup[url] = self.__doc_id

            lines = f.readlines()
            for line in lines:
                for word in re.sub("[^0-9a-zA-Z]+", " ", line).split(" "):
                    self.__add_word(word)
                    word_count += 1
            self.doc_term_count[self.__doc_id] = word_count
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

    def handle_dir(self, dirname):
        """Opens the file/directory for processing.

        Opens the directory and lists all the files/directories for processing.
        Recursively calls into any directories found, otherwise calls process_page().

        Args:
            dirname: The name of the directory to be processed.
        """
        self.createIndexerDir()
        for dirpath, directories, files in os.walk(dirname):
            for f in files:
                self.process_page(os.path.join(dirpath, f))

    def save_indexer_to_files(self):
        """Writes the index data to a file.

        Writes out to the file by temporarily redirecting the stdout to the given
        file.

        Files written:
            index.txt - Contains the indexer data.
            tf_idf.txt - Contains the TF-IDF data.
            terms.txt - Contains the term to term_id data.
            docs.txt - Contains the doc to doc_id data.

        Args:
            file_name: The name of the file to be written to.
        """
        stdout = sys.stdout
        files = [(self.indexer_path + "/index.txt", self.print_indexer),
                 (self.indexer_path + "/tf_idf.txt", self.print_tf_idf),
                 (self.indexer_path + "/doc_lengths.txt", self.print_doc_lengths),
                 (self.indexer_path + "/terms.txt", self.print_term_lookup),
                 (self.indexer_path + "/docs.txt", self.print_doc_lookup)]

        for name, func in files:
            with open(name, "w") as f:
                sys.stdout = f
                func()

        sys.stdout = stdout

    def __calculate_tf_idf(self, term_freq, doc_freq, doc_id):
        """Calculates the TF-IDF for the term.

        Args:
            term_freq: The frequency of the term.
            doc_freq: The amount of documents the term appears in.
            doc_id: The document ID.
        """
        return (1 + math.log(float(term_freq), 10)) * math.log(float(self.num_docs)/doc_freq, 10)

    def create_tf_idf(self):
        """Creates the TF-IDF indexer dictionary.

        The dictionary copies its values from the indexer data structure and replaces the term
        frequency value with the TF-IDF value.
        """
        self.tf_idf = copy.deepcopy(self.indexer)
        for k, v in self.tf_idf.items():
            for doc, tf in v.items():
                self.tf_idf[k][doc] = self.__calculate_tf_idf(tf, len(v), doc)


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
        return {v: k for k, v in self.term_id_lookup.items()}

    def get_inverse_doc_lookup(self):
        """Returns an inverse dictionary of doc_id_lookup {doc_id : doc}"""
        return {v: k for k, v in self.doc_id_lookup.items()}


    #
    # Printing functions.
    #
    def print_term_lookup(self, by_id=True):
        """Prints the key, value pairs of term_id_lookup.

        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k, v in sorted(self.term_id_lookup.items(), key=lambda x: x[by_id]):
            print("({} : {})".format(k, v))

    def print_doc_lookup(self, by_id=True):
        """Prints the key, value pairs of doc_id_lookup.

        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k, v in sorted(self.doc_id_lookup.items(), key=lambda x: x[by_id]):
            print("({} : {})".format(k, v))

    def print_inverse_term_lookup(self, by_id=True):
        """Prints the inverse key, value pairs of term_id_lookup.
        
        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k, v in sorted(self.get_inverse_term_lookup().items(), key=lambda x: x[not by_id]):
            print("({} : {})".format(k, v))

    def print_inverse_doc_lookup(self, by_id=True):
        """Prints the inverse key, value pairs of doc_id_lookup.
        
        Args:
            by_id: Boolean indicating whether to sort by ID, otherwise by name.
        """
        for k, v in sorted(self.get_inverse_doc_lookup().items(), key=lambda x: x[not by_id]):
            print("({} : {})".format(k,v))

    def print_indexer(self, print_word=False):
        """Prints the key, value pairs of the indexer.

        The format for the index is {term_id : {doc_id, frequency}}. In English, each term_id
        has dictionary values which indicates its frequency in a specific document.

        Args:
            print_word: Flag indicating if the user wants to print out the actual word along
                with the term.
        """
        for k, v in self.indexer.items():
            term = self.get_inverse_term_lookup()[k] if print_word else ""
            print("({} {} : ({})".format(k, term, dict(v)))

    def print_tf_idf(self, print_word=False):
        """Prints the key, value pairs of the indexer.

        The format for the index is {term_id : {doc_id, tf-idf}}. In English, each term_id
        has dictionary values which indicates its tf-idf value in a specific document.

        Args:
            print_word: Flag indicating if the user wants to print out the actual word along
                with the term.
        """
        for k, v in self.tf_idf.items():
            term = self.get_inverse_term_lookup()[k] if print_word else ""
            print("({} {} : ({})".format(k, term, dict(v)))

    def print_doc_lengths(self):
        """Prints the document ID, document length (word count) pairs."""
        for k, v in self.doc_term_count.items():
            print("({} : {})".format(k, v))

    def createIndexerDir(self):
        ''' Overwrites a dir if it already exists '''
        if os.path.exists(self.indexer_path):
            shutil.rmtree(self.indexer_path)
        os.makedirs(self.indexer_path)

if __name__ == "__main__":
    indexer = Indexer()

    # Time the indexer
    start = time.time()
    indexer.handle_dir("data")
    indexer.create_tf_idf()
    end = time.time()

    print("Time:", str(end - start), "seconds")

    indexer.save_indexer_to_files()
