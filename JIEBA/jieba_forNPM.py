import jieba, os, json

#Init
base_path = os.path.dirname(__file__)
config = json.load(open(os.path.join(base_path, 'config.json')))
fn = config['DataSet']['NPMCorpus']
op = config['DataSet']['NPMCorpus_seg']
jieba.set_dictionary(os.path.join(base_path, 'dict.txt.big'))

def main():
    
    #load stopword set
    stopword_set = set()
    with open(os.path.join(base_path, 'stop_words.txt'),'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    with open(op, 'a', newline='',encoding = 'utf-8-sig') as output:
        with open(fn,'r', encoding='utf-8-sig') as sentences:
            for sentence in sentences:

                sentence = sentence.replace(" ","")
                sentence = sentence.replace(",,,,","")
                sentence = sentence.replace("\"","")
                sentence = sentence.replace("□","")
                sentence = sentence.replace("口","")
                sentence = sentence.strip('\n')
                words = jieba.cut(sentence, cut_all=False)

                for word in words:
                    if word not in stopword_set:
                        output.write(word+' ')
                        print(word+"\n")
                output.write('\n\n')


        output.close()


if __name__ == '__main__':
    main()