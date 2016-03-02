import re
from Indexer import Indexer
#indexer = Indexer()
#indexer.handle_dir("data")
#indexer.create_tf_idf()



def read_tf_idf():
    ''' Reads the tf_idf.txt produced by Indexer into a dictionary '''
    tf_idf = dict()
    with open("tf_idf.txt") as f:
        for line in f.readlines():
            lineElements = re.sub("[\(:\{\}\),]*", "",line).split()
            # Term id is guaranteed the first
            term_id = lineElements[0] 
            docIDs2tf = [(lineElements[i],lineElements[i+1]) for i in range(1,len(lineElements) - 1, 2)]
            # Initialize term_id -> {docID -> tf_idf}
            tf_idf[term_id] = dict()
            for doc in docIDs2tf:
                tf_idf[term_id][doc[0]] = float(doc[1])
    return tf_idf

def read_terms():
    term2termID = dict()
    with open("terms.txt") as f:
        for line in f.readlines():
            lineElements = re.sub("[\(:\{\}\),]*", "",line).split()
            term2termID[lineElements[0]] = lineElements[1]
    return term2termID

def getTermsFromQuery(query):
    return re.sub("[^0-9a-zA-Z]+", " ", query.strip()).split(" ")

if __name__ == "__main__":
    tf_idf = read_tf_idf()
    term2term_id = read_terms()
    query = "machine learning"

    for term in getTermsFromQuery(query):
        print("Term: " + term + ", term_id: " + term2term_id[term])
        # Sort by the tf_idf query results by the tf_idf value
        queryResults = sorted(tf_idf[term2term_id[term]].items(), key = lambda x: (x[1],x[0]))
        diff_idf = set()
        for docID2tf_idf in queryResults:
            diff_idf.add(docID2tf_idf[1])
        for idf in diff_idf:
            print(idf)
        print("Number of different tf_idfs: " + str(len(diff_idf)))
        print("Total number of tf_idfs: " + str(len(queryResults)))
