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

query = input("Input term: ")
terms = []
for term in re.sub("[^0-9a-zA-Z]+", " ", query.strip()).split(" "):
    print("Term: " + term)
    terms.append(term)

result = read_tf_idf()
print(result['249686'])
