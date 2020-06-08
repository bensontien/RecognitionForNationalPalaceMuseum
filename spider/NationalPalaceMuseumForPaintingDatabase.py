import bs4, requests, os, csv
import time, json

def main():

    #Init
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    fn = config['DataSet']['NPMCorpus']

    for i in range(config['DataSet']['Quantity']):

        dataStartnum = config['NPM']['ID']
        dataURLnum = "0"+ str(int(dataStartnum)+i)
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
            
            #品名與釋文
            datatable1 = objSoup.find_all("table", class_="table_list")
            dataTag1=datatable1[0].find_all("tr")
            artworksName_box=dataTag1[2].find_all("td")
            artworksName=artworksName_box[1].text
            
            translation = dataTag1[-1].find_all("td")
            getTranslationContent=translation[-1].text
    
            #文物介紹
            datatable2 = objSoup.find_all("table", id="gvReference")
            
            try:
                dataTag2=datatable2[0].find_all("tr")
            except:
                time.sleep(1)
                continue
            
            

            for i in range (len(dataTag2)):
                
                if('內容簡介（中文）' in dataTag2[i].text):
                
                    artworksContent_box=dataTag2[i].find_all("td")
                    getContent=artworksContent_box[-1].text
                    artworksContent=getTranslationContent+getContent
                    print("ArtworksName: ",artworksName)
                    print("ArtworksContent: ",artworksContent)
                    
                    with open(fn, 'a', newline='',encoding = 'utf-8-sig') as csvFile:
                        csvWriter=csv.writer(csvFile)
                        csvWriter.writerow([artworksName,artworksContent,url])
                    
                    break
                else:
                    continue

        else:
            print("Page Download failed")

if __name__ == '__main__':
    main()