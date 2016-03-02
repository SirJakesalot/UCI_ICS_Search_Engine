import re
from Indexer import Indexer
#indexer = Indexer()
#indexer.handle_dir("data")
#indexer.create_tf_idf()

def read_tf_idf():
    result = dict()
    
    with open("tf_idf.txt") as f:
        for line in f.readlines():
            line = re.sub("[\(:\{\}\),]*", "",line).split()
            term_id = line[0]
            doc_id_2_tf = [(line[i],line[i+1]) for i in range(1,len(line) - 1, 2)] 
            result[term_id] = dict()
            for doc in doc_id_2_tf:
                result[term_id][doc[0]] = doc[1]
            #print(result[term_id])
    return result
def read_terms():
    result = dict()
    with open("terms.txt") as f:
        for line in f.readlines():
            line = re.sub("[\(:\{\}\),]*", "",line).split()
            result[line[0]] = line[1]
    return result
tf_idf = read_tf_idf()
term2term_id = read_terms()
query = "machine learning"
for term in re.sub("[^0-9a-zA-Z]+", " ", query.strip()).split(" "):
    print("Term: " + term + ", term_id: " + term2term_id[term])
    result = list(tf_idf[term2term_id[term]])
    for i in range(0,10):
        print(result[i])

