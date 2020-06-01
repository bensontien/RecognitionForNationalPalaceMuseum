import logging
import csv, jieba, os, json
import numpy as np
from gensim.models import KeyedVectors,word2vec

def main():

    #Init
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    fn = config['DataSet']['ArticleCorpus']
    op = config['SimilarityCalculate']['Article_average']

    word_sentences_list=[]
    word_input_sentences_list=[]
    seg_sentence=""
    averageVector=np.zeros(200)
    averageVectorarray=np.zeros(200)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model1 = KeyedVectors.load_word2vec_format("W2V_embedding.model", binary=False)
    w2v_dict = dict(zip(model1.wv.index2word, model1.wv.syn0))

    #load stopword set
    stopword_set = set()
    with open('JIEBA\stop_words.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    with open(op, 'a', newline='',encoding = 'utf-8-sig') as csvFile_op:

        csvWriter=csv.writer(csvFile_op)
        countNUM=0

        with open(fn,'r', encoding='utf-8-sig') as csvFile_ip:

            sentences = csv.reader(csvFile_ip)

            for sent in sentences:

                sentence = ''.join(sent)

                countNUM=countNUM+1

                sentence = sentence.replace(" ","")
                sentence = sentence.replace(",,,,","")
                sentence = sentence.replace("\"","")

                sentence = sentence.strip('\n')
                words = jieba.cut(sentence, cut_all=False)
                
                for word in words:
                    if word not in stopword_set:
                        seg_sentence=seg_sentence+" "+word
                        

                if sentence.isspace() == True:
                    continue
            
                else:
                    word_sentences_list = seg_sentence.split()

                    for i in range(len(word_sentences_list)):
                        if word_sentences_list[i] in w2v_dict:
                            vec = model1.wv.vectors[model1.wv.vocab[word_sentences_list[i]].index]
                            averageVectorarray = np.vstack((averageVectorarray, vec))
                            word_input_sentences_list.append(word_sentences_list[i])
            

                if len(word_input_sentences_list)==0:
                    continue

                else:
                    
                    averageVectorarray=np.delete(averageVectorarray,0,0)
                    averageVector= np.mean(averageVectorarray, axis=0)
                    print(countNUM,'\n')
                    print(word_input_sentences_list)
                    print(np.array2string(averageVector, separator=','))
                    csvWriter.writerow([countNUM,sentence,word_input_sentences_list, averageVector])
                    

                    #Clear
                    word_input_sentences_list=[]
                    seg_sentence=""
                    averageVectorarray=np.zeros(200)
                    averageVector=np.zeros(200)


if __name__ == '__main__':
    main()