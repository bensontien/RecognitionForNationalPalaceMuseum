import logging
import os, json
from gensim.models import word2vec

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    #Init
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    trainingSegData = config['TrainingSetting']['TrainData']
    
    sentences = word2vec.LineSentence(trainingSegData)
    model1 = word2vec.Word2Vec(sentences, size=config['TrainingSetting']['size'], window=config['TrainingSetting']['window'],min_count=config['TrainingSetting']['min_count'], sg=config['TrainingSetting']['sg'], workers=config['TrainingSetting']['workers'])
    model1.wv.save_word2vec_format("W2V_embedding.model", binary= False)

if __name__ == "__main__":
    main()