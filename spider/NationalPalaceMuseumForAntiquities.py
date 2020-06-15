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
        
        time.sleep(0.5)
        
        try:
            html = requests.get(url)
        except:
            time.sleep(5)
            print("Failed,Retry after 5s.")
            continue

        print("Page Downloading...")
        
        if(html.status_code == requests.codes.ok):

            print("Page Download Sucessful")

            try:
                objSoup = bs4.BeautifulSoup(html.text, 'lxml')
            except:
                continue    
            
            #品名
            datatable1 = objSoup.find_all("table", class_="table_list")
            dataTag1=datatable1[0].find_all("tr")
            artworksName_box=dataTag1[1].find_all("td")
            artworksName_temp=artworksName_box[1].find_all("span", id="lblTitleName")
            artworksName=artworksName_temp[0].text
            
            #說明
            Content = dataTag1[-1].find_all("td")
            getContent=Content[-1].text
            
            
            if(artworksName!="" and getContent!=""):
                
                print("ArtworksName: ",artworksName)
                print("ArtworksContent: ",getContent) 

                with open(fn, 'a', newline='',encoding = 'utf-8-sig') as csvFile:
                    csvWriter=csv.writer(csvFile)
                    csvWriter.writerow([artworksName,getContent,url])
            else:
                continue
            
        else:
            print("Page Download failed")

if __name__ == '__main__':
    main()