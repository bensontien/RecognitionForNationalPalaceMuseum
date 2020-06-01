import logging
import csv, os, json
import numpy as np

def cosine_similarity_func(vector1, vector2):

    vector1_float = [float(idx) for idx in vector1 if idx !='']
    vector2_float = [float(idx) for idx in vector2 if idx !='']  

    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1_float, vector2_float):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)

def vectorHandler(vector_before):

    vector_before[len(vector_before)-1] = vector_before[len(vector_before)-1].replace("]","")   
    del vector_before[0]
    
    return vector_before


def main():
    
    #Init
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    fn1 = config['SimilarityCalculate']['Article_average']
    fn2 = config['SimilarityCalculate']['NPM_average']
    Result_doc= config['SimilarityCalculate']['Result']


    paragraphNum=""
    paragraphDescibe=""
    paragraphVector=[]

    artURL=""
    artVector=[]

    result_dict_temp={}
    result_dict={}

    with open(fn1,'r' ,encoding = 'utf-8-sig') as csvFile_read1:

        sentences1 = csv.reader(csvFile_read1)

        for sent in sentences1:

            paragraphNum = ''.join(sent[0])
            paragraphDescibe = ''.join(sent[1])
            paragraphVector_temp = sent[3].split()
            paragraphVector = vectorHandler(paragraphVector_temp)
            
            cosine_similarity_filter=[]


            with open(fn2,'r', encoding='utf-8-sig') as csvFile_read2:

                sentences2 = csv.reader(csvFile_read2)

                for sent2 in sentences2:

                    artURL = ''.join(sent2[3])
                    artVector_temp = sent2[5].split()
                    artVector = vectorHandler(artVector_temp)

                    cosineSimilarity=cosine_similarity_func(paragraphVector, artVector)

                    if(cosineSimilarity not in cosine_similarity_filter):

                        result_dict_temp[artURL]=list()
                        result_dict_temp[artURL].append(cosineSimilarity)
                        cosine_similarity_filter.append(cosineSimilarity)


                cosine_similarity_filter.clear()

                result_dict=sorted(result_dict_temp.items(),key=lambda item: item[1],reverse = True)
                    
                print(paragraphNum+"\n"+paragraphDescibe)
                print(result_dict[0:5], '\n')


                with open(Result_doc, 'a', newline='',encoding = 'utf-8-sig') as csvFile_result:

                    csvWriter=csv.writer(csvFile_result)
                    csvWriter.writerow([paragraphNum, paragraphDescibe, result_dict[0:5]])
                    
                    #Clear
                    result_dict_temp.clear()
                    result_dict.clear()
                    paragraphVector_temp.clear()
                    paragraphVector.clear()
                    artVector_temp.clear()
                    artVector.clear()


if __name__ == '__main__':
    main()