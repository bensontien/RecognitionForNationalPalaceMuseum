import bs4, requests, os, csv
import time, json

def main():

    #Init
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    fn = config['DataSet']['ArticleCorpus']

    for i in range(config['DataSet']['Quantity'],0,-1):
  
        dataStartnum = config['Article']['ID']
        dataURLnum = str(int(dataStartnum)+(i-2000))
        print(dataURLnum)

        url = config['DataSet']['URL'] + dataURLnum 
        
        time.sleep(2.5)
        try:
            html = requests.get(url)
        except:
            time.sleep(10)
            continue

        print("Page Downloading...")
        
        if(html.status_code == requests.codes.ok):

            print("Page Download Sucessful")

            objSoup = bs4.BeautifulSoup(html.text, 'lxml')

            articleTag=objSoup.select('.article-component-section')

            try:
                articleInfo_box = articleTag[0].select('.info')
            except:
                continue

            articleInfo_type_box=articleInfo_box[0].find('a')
            articleInfo_type=articleInfo_type_box.text
            print(articleInfo_type)
        

            if(config['Article']['Type'] in articleInfo_type):

                articleContent_box = articleTag[0].select('.article-content')
                articleContent = articleContent_box[0].find_all('p')

                with open(fn, 'a', newline='',encoding = 'utf-8-sig') as csvFile:

                    csvWriter=csv.writer(csvFile, delimiter=' ')
                
                    for p in articleContent:
                    
                        csvWriter.writerow(p.text)
            
        else:
            print("Page Download failed")

if __name__ == '__main__':
    main()