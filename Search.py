#!/usr/bin/python3

from Indexer import Indexer
import sys, os, shutil, time, re

class Search_Engine(Indexer):
    query_data_path = "Query_Data"
    def __init__(self, data_path = ""):
        ''' Either read the Indexer info from files or generate it
            If readFromFiles is true: path = path to the dir containing the results from saving Indexer files before
            ELSE readFromFiles is false: path = path to the data dir'''

        self.createQueryDir()
        Indexer.__init__(self)
        index_timer_start = time.time()
        if len(data_path) == 0: # No need to calculate again
            self.read_files(self.indexer_path) # Indexer_Data
            print("Read index in {0} seconds".format(str(time.time() - index_timer_start)))
        else:
            self.handle_dir(data_path)
            self.create_tf_idf()
            print("Generated index in seconds: {0}".format(str(time.time() - index_timer_start)))
            self.save_indexer_to_files()
        self.inverse_doc_lookup = self.get_inverse_doc_lookup()
        
    def read_files(self, path):
        self.doc_id_lookup = self.read_dict(path + "/docs.txt")
        self.term_id_lookup = self.read_dict(path + "/terms.txt")
        # Don't need doc term count
        #self.indexer = read_dict_of_dict(path + "/index.txt")
        self.tf_idf = self.read_dict_of_dict(path + "/tf_idf.txt")

    def read_dict(self, path):
        result = dict()
        with open(path) as f:
            for line in f.readlines():
                lineElements = re.sub("[\(:\{\}\),]*", "",line).split()
                result[lineElements[0]] = lineElements[1]
        return result
    def read_dict_of_dict(self, path):
        result = dict()
        with open(path) as f:
            for line in f.readlines():
                # Parse line into elements
                lineElements = re.sub("[\(:\{\}\),]*", "",line).split()
                # Term id is guaranteed the first element in a line
                term_id = lineElements[0]
                # Every key is in position i and every value is at i + 1
                docIDs2vals = [(lineElements[i],lineElements[i+1]) for i in range(1,len(lineElements) - 1, 2)]
                # Initialize term_id -> {docID -> tf_idf}
                result[term_id] = dict()
                for doc in docIDs2vals:
                    result[term_id][doc[0]] = doc[1]
        return result

    def printContainer(self, container, title):
        ''' Helper function to write an iterable's contents to a file'''
        print("<{0}>".format(title))
        if not container:
            print("EMPTY")
        else:
            for element in container:
                print("-> {0}".format(element))
        print("</{0}>".format(title))

    def getTermsFromQuery(self, query):
        return re.sub("[^0-9a-zA-Z]+", " ", query.lower().strip()).split(" ")

    def createQueryDir(self):
        ''' Overwrites a directory if it already exists '''
        if os.path.exists(self.query_data_path):
            shutil.rmtree(self.query_data_path)
        os.makedirs(self.query_data_path)

    def getTermDocSets(self, terms):
        '''A list of sets, one for each term whose contents is a set
        of all the docIds it appears in. Taking the intersection of
        all these sets will give us a set of all common docIds
        across all terms'''
        termDocSets = []
        for term in terms:
            if not term in self.term_id_lookup:
                print("Term '{0}' not in corpus".format(term))
                continue
            term_id = self.term_id_lookup[term]
            print("Term: {0}, Term Id: {1}".format(term, term_id))
            # Get the term's {doc_id : tf_idf}
            term_tf_idf = self.tf_idf[term_id].items()
            termDocSet = set(doc_id for doc_id, tf_idf in term_tf_idf)
            termDocSets.append(termDocSet)
        return termDocSets
    def getCommonDocIds(self, termDocSets):
        commonDocIds = []
        if (len(termDocSets) != 0):
            commonDocIds = list(set.intersection(*termDocSets))
        return commonDocIds
        # print container
    def getQueryResults(self, commonDocIds, terms):
        query_tf_idf = []
        term_doc_tf_idf = []
        for doc_id in commonDocIds:
            for term in terms:
                if term in self.term_id_lookup:
                    term_id = self.term_id_lookup[term]
                    term_doc_tf_idf.append(self.tf_idf[term_id][doc_id])
            query_tf_idf.append((self.inverse_doc_lookup[doc_id], max(term_doc_tf_idf)))
            term_doc_tf_idf = []
        query_tf_idf.sort(key = lambda item : (item[1],item[0]), reverse = True)
        return query_tf_idf

    def printQueryResults(self, query_results):
        print("<QUERY RESULTS>")
        position = 1
        for doc_id, tf_idf in query_results:
            print("position: {0}, url: {1}, tf_idf: {2}".format(position, self.inverse_doc_lookup[doc_id], tf_idf))
            position += 1
        print("</QUERY RESULTS>")

    def search(self, query):
        stdout = sys.stdout
        search_timer_start = time.time()
        path = "{0}/{1}".format(self.query_data_path, query)
        with open(path, "w") as f:
            sys.stdout = f
            print("Given query: {0}".format(query))
            # Break the query up into terms
            terms = self.getTermsFromQuery(query)
            self.printContainer(terms, "TOKENIZED QUERY")

            termDocSets = self.getTermDocSets(terms)
            commonDocIds = self.getCommonDocIds(termDocSets) 
            query_results = self.getQueryResults(commonDocIds, terms)
            self.printContainer(query_results, "QUERY RESULTS")
            print("Time for query in seconds: {0}".format(str(time.time() - search_timer_start)))
        sys.stdout = stdout


if __name__ == "__main__":
    '''
        Indexer objects
        ---------------
        doc_id_lookup: {url : doc_id}
        term_id_lookup: {term : term_id}
        doc_term_count: {doc_id : word_count}
        indexer: {term_id : {doc_id : freq}}
        tf_idf: {term_id : {doc_id : tf_idf}}
    '''
    # File path locations
    #data_path = "data"
    data_path = "/home/jake/Desktop/data"
    search_engine = Search_Engine(data_path)
    #search_engine = Search_Engine()

    # Create the directory to hold the query files
    queries = ["machine learning", "mondego", "software engineering", "security", "student affairs", "graduate courses", "informatics", "REST", "computer games", "information retrieval"] 

    query_timer_start = time.time()
    for query in queries:
        search_engine.search(query)
