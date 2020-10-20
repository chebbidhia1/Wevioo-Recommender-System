import pprint
import pandas as pd
import sys
from datetime import datetime
import numpy as np
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from langdetect import detect
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import wordpunct_tokenize
import re
from nltk.stem.snowball import SnowballStemmer
import difflib
from textblob import TextBlob
from scrape_linkedin import ProfileScraper
import matplotlib.pyplot as plt
import time
from sklearn import decomposition
from matplotlib import colors
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy.linalg as LA
from math import sqrt
import pickle
from scipy.spatial import distance
class Preparation:
    def __init__(self,Link,cookie):
        self.Link = Link
        self.cookie= cookie
        self.dict = Dict_Profil_Competence = {
            "Développeur Web Back-End" : { "Javascript" : 1,"SQL": 3,"NoSQL" :2,"Nodejs" : 3,"express.js":3,"Koa.js": 1,"Hapi.js" :1,
                                    "Angular JS": 1,"React JS" : 1,"Jquery" :1, "Bash": 1,
                                      "Nginx0" : 1,
                                      "C": 1,
                                      "C++": 1},
            "Developpeur Front-End" : {"Javascript" : 3,
                                "HTML5": 3,
                                "CSS" :3,
                                "REST" : 3,
                                "React JS":3,
                                "SASS": 1,
                                "PostCss" :1,
                                "WebPack": 1,
                                "Gitlab" : 1},
            "Développeur Embarqué Middleware" :  {"C" : 2,
                                "C++": 2,
                                "Linux" :3,
                                "Embedded C" : 3,
                                "Embedded C++":3},
            "Technical Lead/ Architecte JEE" :   {"Java" : 3,
                                "Jee": 3,
                                "microservices" :3,
                                "intégration continue" : 3,
                                "docker":3,
                                 "aws":1 },
            "Développeur FullStack JS" : {"Angular Js" : 3,"Ext.js" : 3,"Jquery" : 2 ,"HTML" : 2 ,"CSS" :2 ,
                                  "nodeJS" :2 ,"Javascript": 3,"MongoDB":2,"MySql":2},
            "Développeur JAVA/JEE" : { "Java" : 3,"JEE" : 3,"Spring" : 3,"SOA" : 1, "SOAP" :1  ,"rest" : 1, "microservices" : 3,
                              "git" : 2 , "SVN" : 2, "Jira" : 1, "confluence" : 1, "spring boot" : 3 ,
                              "spring security": 3, "Java8" : 3 },
            "Développeur PHP/Symfony" : { "PHP" :3 ,"Symfony" : 3,"Restfull API" : 2 ,"Git" :2},
            "Développeur DRUPAL" :  { "PHP" : 3,"CMS" : 1 ,"HTML" :1,"CSS" :1,"MySql" :1,"Symfony" : 2 ,"Javascript": 2,
                            "Git" : 2,"Drupal": 3 },
            "Product Owner/ PO" : { "Scrum" : 3 ,"Analyse Factorielle" : 3,"Testing" : 3 ,"Rédaction spécification" : 3}
    
}
    
    def __scrapping(self):
        profile = []
        scraper = ProfileScraper(cookie=self.cookie)
        profile.append(scraper.scrape(user=self.Link))
        dfr = pd.DataFrame({
            'personal_info': [],
            'experiences': [],
            'skills': [],
            'accomplishments': [],
        })
        dfr=dfr.append({'personal_info':profile[0].to_dict()["personal_info"], 
                   'experiences':profile[0].to_dict()["experiences"],
                   'skills':profile[0].to_dict()["skills"],
                   'accomplishments':profile[0].to_dict()["accomplishments"]},ignore_index=True)
        return dfr
    
    def __personal_info(self):
        dataframe=self.__scrapping()
        personal_info=dataframe["personal_info"][0]
        dataframe["summary"]=personal_info["summary"]
        if dataframe["personal_info"][0]["name"] == None:
            dataframe["name"]=self.Link
        else:
            dataframe["name"]=personal_info["name"]
        dataframe["image"]=personal_info["image"]
        dataframe["url"]="https://www.linkedin.com/in/"+self.Link
        dataframe.drop('personal_info',axis=1,inplace=True)
        return dataframe 
 
    def __Nettoyage(self): 
        dataframe1=self.__personal_info()
        stops=[]
        stops.append(stopwords.words('french'))
        stops.append(stopwords.words('english')) 
        
        jobs = dataframe1['experiences'][0]['jobs']
        for job in jobs:
            s = job['description']
            if s != None:
                try:
                    tok=wordpunct_tokenize(s)
                    for word in tok:
                        if word not in stops:
                            job['description']=" ".join(tok).lower()
                    job['description']=re.sub("[^a-zA-Z]"," ",job['description'])
                except:
                    print("pass 1")
                    pass
        jobs = dataframe1['experiences'][0]['jobs']
        for job in jobs:
            s = job['description']
            if s != None:
                try:
                    l=detect(s)
                    if l == 'fr':
                        stemmer = SnowballStemmer(language='french')
                    elif l == 'en':
                        stemmer = SnowballStemmer(language='english')
                    tok=wordpunct_tokenize(s)
                    words=[]
                    for word in tok:
                         words.append(stemmer.stem(word))
                    job['description']=" " .join(words).lower()
                except:
                    print("pass 2")
                    pass

        chaine=[]
        try:
            tok=wordpunct_tokenize(dataframe1["summary"][0])
            for word in tok:
                if word not in stops:
                    chaine.append(word)
            chaine=" ".join(chaine).lower()
            chaine=re.sub("[^a-zA-Z]"," ",chaine)
        except:
            print("pass 3")
            pass
        
        words=[]
        """try:
            l=detect(dataframe1['summary'][0])
            if l == 'fr':
                stemmer = SnowballStemmer(language='french')
            elif l == 'en':
                stemmer = SnowballStemmer(language='english')
            tok=wordpunct_tokenize(dataframe1['summary'][0])
            for word in tok:
                words.append(stemmer.stem(word))
            words=" ".join(words).lower()
        except:
            print("pass 4")
            pass"""
        if dataframe1['summary'][0] != '':
            l=detect(dataframe1['summary'][0])
            if l == 'fr':
                stemmer = SnowballStemmer(language='french')
            elif l == 'en':
                stemmer = SnowballStemmer(language='english')
            tok=wordpunct_tokenize(dataframe1['summary'][0])
            for word in tok:
                words.append(stemmer.stem(word))
            words=" ".join(words).lower()
            dataframe1["summary"]=words
        
        return dataframe1
    def __subjectivite(self):
        sub=self.__Nettoyage()
        result_text=[]
        try:
            result_text.append(TextBlob(sub['summary'][0]).sentiment.subjectivity)
        except:
            result_text.append(0)
        sub.drop('summary',axis=1,inplace=True)
        sub['subjectivite']=result_text
        return sub
    def __num_month(self,month):
        if month =='janv.' or month=='Jan':
            return 1
        if month =='févr.' or month=='Feb':
            return 2
        if month =='mars'  or month=='Mar':
            return 3
        if month =='avr.'  or month=='Apr':
            return 4
        if month =='mai'  or month=='May':
            return 5
        if month =='juin'  or month=='June':
            return 6
        if month =='juil.'  or month=='Jul':
            return 7
        if month =='août'  or month=='Aug':
            return 8
        if month =='sept.'  or month=='Sept':
            return 9
        if month =='oct.'  or month=='Oct':
            return 10
        if month =='nov.'  or month=='Nov':
            return 11
        if month =='déc.'  or month=='Dec':
            return 12
    def __diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month
    
    def __month_experience(self):
        month = self.__subjectivite()
        jobs = month['experiences'][0]['jobs']
        numbee_of_months=0
        sum_months=0
        for job in jobs :
            date = job['date_range']
            if date !=None :
                date=date.replace(" ","")
                if(len(date.split('–'))==1):
                    date=date+"–"+"not mentioned"
                # traitement du date début
                start_date = date.split('–')[0]
                if len(start_date)==4:
                    months=2
                    years = start_date
                else:
                    months= start_date[:-4]
                    years = start_date[-4:]
                    numms = self.__num_month(months)
                if(numms==None):
                    numms=6
                if years == '013':
                    years="2013"
                final_dates =str(numms)+'-'+years
                d1 = datetime.strptime(final_dates, "%m-%Y")
                #traitement date fin
                end_date = date.split('–')[1]
                if end_date=="Aujourd’hui" or end_date==" Present" or end_date=="Present":
                    today = datetime.today()
                    datem = str(today.month)+"-"+str(today.year)
                    d2 = datetime.strptime(datem, "%m-%Y") 
                elif end_date=="not mentioned":
                    monthe = numms
                    yeare = int(years)+1
                    datem = str(monthe)+"-"+str(yeare)
                    d2 = datetime.strptime(datem, "%m-%Y") 
                else :
                    if len(end_date)==4:
                        monthe = 2
                        yeare = end_date     
                    else:
                        monthe = end_date[:-4]
                        yeare = end_date[-4:]
                        numm = self.__num_month(monthe)
                        if(numm==None):
                            numm=6
                        final_date =str(numm)+'-'+yeare
                        d2 = datetime.strptime(final_date, "%m-%Y")
                diff=self.__diff_month(d2,d1)
                sum_months+=diff
        month["months_experience"] = sum_months
        return month
    def __experienced_skills(self):
        experienced=self.__month_experience()
        skills = experienced["skills"][0]
        jobs = experienced['experiences'][0]['jobs']
        ep=[]
        experienced_skills=[]
        for skill in skills:
            s = skill['name'].lower()
            for job in jobs:
                if (job["description"]!=None):
                    if('stage' not in  job["description"])&('internship' not in  job["description"])&('pfe' not in  job["description"])&('stage' not in  job["title"])&('internship' not in  job["title"])&('pfe' not in  job["title"]):
                        if s in job['description']:
                            ep.append(s)
        ep = list(dict.fromkeys(ep))
        experienced_skills.append(ep)
        experienced['experienced_skills']=experienced_skills
        return experienced
    
    def __profil(self):
        prof = self.__experienced_skills()
        skills = prof["skills"][0]
        p={}
        for d,dic in self.dict.items():
            score=0
            somme=0
            for d1,dic2 in dic.items():
                somme+=dic2
                l=[]
                for skill in skills:
                    s = skill['name'].lower() 
                    sss=[]
                    sss.append(s)
                    if  (len(difflib.get_close_matches(d1.lower(),sss,1,0.95))==1):
                        if(d1 not in l):
                            score= score +dic2
                            l.append(d1)
            prof[d]=score/(somme/10)
        return prof
    def __mobilite(self):
        mob = self.__profil()
        jobs=mob['experiences'][0]['jobs']
        abroad = "no"
        for job in jobs:
            if job["location"] is None:
                    abroad="unknown"      
            elif ("tunisia" not in job["location"].lower()) or ("tunisie" not in job["location"].lower()):
                abroad = "yes"
        if abroad == 'yes':
            mob["mobilité"]=1
        elif abroad=='no':
            mob["mobilité"]=0
        elif abroad == 'unknown':
            mob["mobilité"]=0
        return mob
    
    def __profil_ing(self,nomFac):
        if (('esprit' in nomFac.lower()) or ('ingénieur' in nomFac.lower()) or ('engineer' in nomFac.lower()) or ('enib' in nomFac.lower()) or ('enit' in nomFac.lower()) or ('ensit' in nomFac.lower()) or ('ensi' in nomFac.lower()) or ('ept' in nomFac.lower()) or ('esip' in nomFac.lower()) or ('essai' in nomFac.lower()) or ("sup'com" in nomFac.lower()) or 
            ('essat' in nomFac.lower()) or ('suptech' in nomFac.lower()) or ('enig' in nomFac.lower()) or
            ('insat' in nomFac.lower()) or ('enim' in nomFac.lower()) or ('enis' in nomFac.lower()) or ("ingénierie" in nomFac.lower()) ):
            return True
    def __profil_prepa(self,nomFac):
        if(('prepar' in nomFac.lower())or ('bac+2' in nomFac.lower())or ('bac + 2' in nomFac.lower()) or ('prépar' in nomFac.lower())): 
            return True
    def __profil_mastere(self,nomFac):
        if (('master' in nomFac.lower()) or ('maitrise' in nomFac.lower()) or ('Maîtrise' in nomFac)):
            return True
    def __profil_license(self,nomFac):
        if ('license' in nomFac.lower()) :
            return True
    def __high_degree(self):
        high_degree=self.__mobilite()
        education=high_degree['experiences'][0]['education']
        score=0
        d=0
        for ed in education :
            if(ed['degree'] is None):
                if(self.__profil_mastere(ed['name'])):
                    d+=5
                if(self.__profil_ing(ed['name'])): 
                    d+=20
                if(self.__profil_license(ed['name'])):
                    d+=1
                else:
                    d+=0
            elif(ed['degree'] is not None):
                if(self.__profil_mastere(ed['degree'])):
                    d+=5
                if(self.__profil_ing(ed['degree'])): 
                    d+=20
                if(self.__profil_license(ed['degree'])):
                    d+=1


        if(d>=25):
            score = 4
        elif(d<25 and d>=20):
            score=3
        elif(d<20 and d>=5):
            score=2
        elif(d<5 and d>0):
            score=1
        elif(d==0):
            score=0
        high_degree['high_degree_score']=score
        return high_degree
    
    def __endorsment(self):
        endor = self.__high_degree()
        skills= endor["skills"][0]
        liste=[]
        listee=[]
        try:
            for s in skills:
                liste.append(int(s["endorsements"]))
            print(liste)
            n = np.quantile(liste,.75) 
            for s in skills:
                if s["endorsements"]=="99+":
                    s["endorsements"]=100
                if int(s["endorsements"])>n:
                    listee.append(s["name"])
        except:
            pass
        listee = list(dict.fromkeys(listee))
        e=[]
        e.append(listee)
        endor["skills_with_endorsements"]=e
        return endor
    def __average(self):
        average=self.__endorsment()
        list_exp=[]
        for j in average['experiences'][0]['jobs'] :
            if(j['description'] != None ) :
                if(j['title'] != None ) :
                    if('stage' not in  j['description'] and  'internship' not in j['description'] and 'pfe' not in  j['description'] and 'stage' not in j['title'] and  'internship' not in  
                     j['title'] and 'pfe' not in  j['title']):
                        if(j['date_range'] != None) :
                            j['date_range']=j['date_range'].replace(" ","")
                            if(len(j['date_range'].split('–'))==1):
                                j['date_range']=j['date_range']+"–"+" Present"
                            start_date =j['date_range'].split('–')[0]
                            if len(start_date)==4:
                                months=2
                                years = start_date
                            else:
                                months= start_date[:-4]
                                years = start_date[-4:]
                            numms = self.__num_month(months)
                            if(numms==None):
                                numms=6
                            if years == '013':
                                years="2013"
                            final_dates =str(numms)+'-'+years
                            d1 = datetime.strptime(final_dates, "%m-%Y")
                            #traitement date fin
                            end_date = j['date_range'].split('–')[1]
                            if end_date=="Aujourd’hui" or end_date==" Present" or end_date=="Present":
                                today = datetime.today()
                                datem = str(today.month)+"-"+str(today.year)
                                d2 = datetime.strptime(datem, "%m-%Y") 
                            else :
                                if len(end_date)==4:
                                    monthe = 2
                                    yeare = end_date     
                                else:
                                    monthe = end_date[:-4]
                                    yeare = end_date[-4:]
                                    numm = self.__num_month(monthe)
                                    if(numm==None):
                                        numm=6
                                    final_date =str(numm)+'-'+yeare
                                    d2 = datetime.strptime(final_date, "%m-%Y")
                            diff=self.__diff_month(d2,d1)
                            list_exp.append(diff)
            else :
                if(j['title'] != None ):
                    if('stage' not in  j['title'] and  'internship' not in j['title'] and 'pfe' not in j['title']):
                        if(j['date_range'] != None):
                            j['date_range']=j['date_range'].replace(" ","")
                            if(len(j['date_range'].split('–'))==1):
                                j['date_range']=j['date_range']+"–"+" Present"
                            start_date = j['date_range'].split('–')[0]
                            if len(start_date)==4:
                                months=2
                                years = start_date
                            else:
                                months= start_date[:-4]
                                years = start_date[-4:]
                            numms = self.__num_month(months)
                            if(numms==None):
                                numms=6
                            if years == '013':
                                years="2013"
                            final_dates =str(numms)+'-'+years
                            d1 = datetime.strptime(final_dates, "%m-%Y")
                            #traitement date fin
                            end_date = j['date_range'].split('–')[1]
                            if end_date=="Aujourd’hui" or end_date==" Present" or end_date=="Present":
                                today = datetime.today()
                                datem = str(today.month)+"-"+str(today.year)
                                d2 = datetime.strptime(datem, "%m-%Y") 
                            else:
                                if len(end_date)==4:
                                    monthe = 2
                                    yeare = end_date     
                                else:
                                    monthe = end_date[:-4]
                                    yeare = end_date[-4:]
                                    numm = self.__num_month(monthe)
                                    if(numm==None):
                                        numm=6
                                    final_date =str(numm)+'-'+yeare
                                    d2 = datetime.strptime(final_date, "%m-%Y")
                            diff=self.__diff_month(d2,d1)
                            list_exp.append(diff)

        if len(list_exp)!=0:        
            average["average_duration"]=sum(list_exp)/(len(list_exp))
        return average
        
    def __Langue(self):
        language=self.__average()
        languages = []
        languages = language['accomplishments'][0]['languages']
        score=[]
        if len(languages)>5:
            language['languages']=3
        if len(languages)==5:
            language['languages']=2
        if len(languages)==4:
            language['languages']=1
        if len(languages)<4:
            language['languages']=0
        return language
    def __score(self):
        dfscore=self.__Langue()
        skills = dfscore['experienced_skills'][0]
        skillswe = dfscore["skills_with_endorsements"][0]
        p={}
        for d,dic in self.dict.items():
            score=0
            somme=0
            for d1,dic2 in dic.items():
                somme+=0.3*dic2
                l=[]
                ll=[]
                for skill in skills:
                    s = skill.lower()
                    sss=[]
                    sss.append(s)
                    if(d1 not in l):
                        if  (len(difflib.get_close_matches(d1.lower(),sss,1,0.95))==1):
                            score= score +0.2*dic2
                            l.append(d1)
                for skill in skillswe:
                    s = skill.lower()
                    sss=[]
                    sss.append(s)
                    if(d1 not in ll):
                        if  (len(difflib.get_close_matches(d1.lower(),sss,1,0.95))==1):
                            score= score +0.1*dic2
                            ll.append(d1)
                dfscore[d]=dfscore[d]+(score/(somme/3))
        return dfscore
    
    def preparer(self):
        df_final = self.__score()
        df_final.drop(columns=['accomplishments','experienced_skills','skills','skills_with_endorsements'], axis=1, inplace=True)
        df_final= df_final[['url', 'name', 'subjectivite', 'months_experience',
       'Développeur Web Back-End', 'Developpeur Front-End',
       'Développeur Embarqué Middleware', 'Technical Lead/ Architecte JEE',
       'Développeur FullStack JS', 'Développeur JAVA/JEE',
       'Développeur PHP/Symfony', 'Développeur DRUPAL', 'Product Owner/ PO',
       'mobilité', 'high_degree_score', 'average_duration', 'languages']]
        return df_final
   

        
class RecommendationModel1:
    def __init__(self,profilsIdeaux,dfClean):
        self.profilsIdeaux=profilsIdeaux
        self.dfClean=dfClean
        print("Calcul des scores........")
        for p in self.profilsIdeaux.index:
            liste=[]
            for i in range(len(self.dfClean)):
                liste.append(self.__similarite(self.profilsIdeaux.loc[p],self.dfClean.iloc[i,:],p))
            self.dfClean["score "+p]=liste
        for p in self.profilsIdeaux.index:
            liste=[]
            for i in range(len(self.profilsIdeaux)):
                liste.append(self.__similarite(self.profilsIdeaux.loc[p],self.profilsIdeaux.iloc[i,:],p))
            self.profilsIdeaux["score "+p]=liste
        print("fin")
    def __similarite_subjectivite(self,v1,v2):
        return (float(v1["subjectivite"])-float(v2["subjectivite"]))

    def __similarite_months_experience(self,v1,v2):
        return (float(v1["months_experience"])-float(v2["months_experience"]))/60

    def __similarite_mobilité(self,v1,v2):
        return (float(v1["mobilité"])-float(v2["mobilité"]))

    def __similarite_high_degree_score(self,v1,v2):
        return (float(v1["high_degree_score"])-float(v2["high_degree_score"]))/4

    def __similarite_average_duration(self,v1,v2):
        return (float(v1["average_duration"])-float(v2["average_duration"]))/24

    def __similarite_languages(self,v1,v2):
        return (float(v1["languages"])-float(v2["languages"]))/3

    def __similarite_profil(self,v1,v2,profil):
        return (float(v1[profil])-float(v2[profil]))/self.dfClean[profil].max()*20
    
    def __similarite(self,v1,v2,profil):
        return (self.__similarite_subjectivite(v1,v2)+ self.__similarite_mobilité(v1,v2) +
           self.__similarite_high_degree_score(v1,v2) + self.__similarite_average_duration(v1,v2)+
           self.__similarite_languages(v1,v2) + self.__similarite_months_experience(v1,v2)+
            self.__similarite_profil(v1,v2,profil))
    
    def recommender(self,profil,num):
        return self.dfClean.sort_values(by='score '+profil).iloc[:,[0,1]].head(num)
    
    def evaluation(self,profil,num):
        data = pd.DataFrame(columns=self.dfClean.iloc[:,17:17+9].columns)
        dataPlot = self.dfClean.sort_values(by='score '+profil).head(num)
        data.loc[profil] = self.profilsIdeaux.loc[profil]
        for i in range(len(dataPlot)):
            data.loc[dataPlot["name"][dataPlot.index[i]]] = dataPlot.iloc[i,:]
            
        plt.figure(figsize=(10,10))
        pca = decomposition.PCA().fit(data)
        data_projected = pca.transform(data)
        
        
        compteur = 0
        for word in data.index:
        
            x, y = data_projected[0, 0],data_projected[0, 1]
            xx, yy = data_projected[1:, 0],data_projected[1:, 1]
            xxx, yyy = x, y = data_projected[:, 0],data_projected[:, 1]
            plt.scatter(x, y, marker='o', color='red')
            plt.scatter(xx, yy, marker='o', color='blue')
            plt.text(xxx[compteur]+1, yyy[compteur]+0.1, word, fontsize=9)
            compteur+=1
        plt.title("Projection des "+str(num) +" individus les plus proches du profil "+profil)
        plt.show()
#####################################################################################################
############################# Similarité avec un profil donné #######################################    
    def __similarite_profiles_scrap(self,v1,v2,profiles):
        somme=0
        for p in profiles:
            somme+=self.__similarite_profil(v1,v2,p)
        return somme
    
    def  __similarite_all_scrap(self,v1,v2,profiles):
        return (self.__similarite_subjectivite(v1,v2)+ self.__similarite_mobilité(v1,v2) +
           self.__similarite_high_degree_score(v1,v2) + self.__similarite_average_duration(v1,v2)+
           self.__similarite_languages(v1,v2) + self.__similarite_months_experience(v1,v2)+
            self.__similarite_profiles_scrap(v1,v2,profiles))
    
    def __calcul_scores_scrap(self,profil_scrap):
        liste=[]
        for i in range(len(self.dfClean)):
            liste.append(self.__similarite_all_scrap(profil_scrap,self.dfClean.iloc[i,:],self.profilsIdeaux.index))
        self.dfClean["similaire de "+profil_scrap['name']]=liste
        
    def similaire_de(self,profil_scrap,num):
        self.__calcul_scores_scrap(profil_scrap)
        return self.dfClean.sort_values(by="similaire de "+profil_scrap['name']).iloc[:,1:17].head(num)
####################################################################################################################
###################################### Similaires au plus d'un profil ##################################    
    def __calcul_scores_demandé(self,liste_d):
        liste=[]
        for i in range(len(self.dfClean)):
            s=0
            chaine=""
            for l in liste_d:
                s+=self.dfClean["score "+l][i]
                chaine+=" "+l
            liste.append(s)
        self.dfClean["similarite "+chaine]=liste
        return chaine
      
    def multi_profil(self,liste_d,num):
        chaine = self.__calcul_scores_demandé(liste_d)
        return self.dfClean.sort_values(by="similarite "+chaine).iloc[:,[1,2,3,13,14,15,16]].head(num)   
        
        
    def evaluation_demande(self,profil,num):
        data = pd.DataFrame(columns=self.dfClean.iloc[:,17:17+9].columns)
        chaine=""
        for p in profil:
            data.loc[p] = self.profilsIdeaux.loc[p]
            chaine+=" "+p
        dataPlot = self.dfClean.sort_values(by="similarite "+chaine).head(num)
        for i in range(len(dataPlot)):
            data.loc[dataPlot["name"][dataPlot.index[i]]] = dataPlot.iloc[i,:]
            
        plt.figure(figsize=(10,10))
        pca = decomposition.PCA().fit(data)
        data_projected = pca.transform(data)
        
        classes=[]
        values = range(len(profil))
        colours = colors.ListedColormap(['r','g','y','k','c','m','orange','tan','b'])
        x, y = data_projected[:len(profil), 0],data_projected[:len(profil), 1]
        for word in data.iloc[:len(profil),:].index:
            classes.append(word)
        scatter = plt.scatter(x, y,c=values, cmap=colors.ListedColormap(colours.colors[:len(profil)]),marker="x")
        
        
        compteur = 0
        for word in data.iloc[len(profil):,:].index:
            xx, yy = data_projected[1:, 0],data_projected[1:, 1]
            xxx, yyy = x, y = data_projected[1:, 0],data_projected[1:, 1]
            plt.scatter(xx, yy, marker='o', color='blue')
            plt.text(xxx[compteur]+1, yyy[compteur]+0.1, word, fontsize=9)
            compteur+=1
        plt.title("Projection des "+str(num) +" individus les plus proches du profil "+chaine)
        plt.legend(handles=scatter.legend_elements()[0], labels=classes)
        plt.show()
        
########################################################################################################################       
        
    def top_profils(self,num):
        data = pd.DataFrame(columns=self.dfClean.iloc[:,17:17+9].columns)
        for p in self.profilsIdeaux.index:
            data.loc[p] = self.profilsIdeaux.loc[p]
        for p in self.profilsIdeaux.index:
            profil=self.dfClean.sort_values(by='score '+p).head(num)
            for i in range(len(profil)):
                data.loc[profil["name"][profil.index[i]]] = profil.iloc[i,:]
        
        plt.figure(figsize=(10,10))
        pca = decomposition.PCA().fit(data)
        data_projected = pca.transform(data)
        
        classes=[]
        values = [0,1,2,3,4,5,6,7,8]
        colours = colors.ListedColormap(['r','b','g','y','k','c','m','orange','tan'])
        x, y = data_projected[0:9, 0],data_projected[0:9, 1]
        for word in data.iloc[:9,:].index:
            classes.append(word)
        scatter = plt.scatter(x, y,c=values, cmap=colours,marker="x")
        
        compteur = 0

        for word in data.iloc[9:,:].index:
            xx1, yy1 = data_projected[9:, 0],data_projected[9:, 1]
            xx2, yy2 = data_projected[9+num:, 0],data_projected[9+num:, 1]
            xx3, yy3 = data_projected[9+2*num:, 0],data_projected[9+2*num:, 1]
            xx4, yy4 = data_projected[9+3*num:, 0],data_projected[9+3*num:, 1]
            xx5, yy5 = data_projected[9+4*num:, 0],data_projected[9+4*num:, 1]
            xx6, yy6 = data_projected[9+5*num:, 0],data_projected[9+5*num:, 1]
            xx7, yy7 = data_projected[9+6*num:, 0],data_projected[9+6*num:, 1]
            xx8, yy8 = data_projected[9+7*num:, 0],data_projected[9+7*num:, 1]
            xx9, yy9 = data_projected[9+8*num:, 0],data_projected[9+8*num:, 1]
            xxx, yyy = x, y = data_projected[9:, 0],data_projected[9:, 1]
            plt.scatter(xx1, yy1, marker='o', color='r')
            plt.scatter(xx2, yy2, marker='o', color='b')
            plt.scatter(xx3, yy3, marker='o', color='g')
            plt.scatter(xx4, yy4, marker='o', color='y')
            plt.scatter(xx5, yy5, marker='o', color='k')
            plt.scatter(xx6, yy6, marker='o', color='c')
            plt.scatter(xx7, yy7, marker='o', color='m')
            plt.scatter(xx8, yy8, marker='o', color='orange')
            plt.scatter(xx9, yy9, marker='o', color='tan')
            plt.text(xxx[compteur]+1, yyy[compteur]+0.1, word, fontsize=9)
            compteur+=1
            
        plt.title("Projection des top {} individus dans chaque profil ".format(num))
        plt.legend(handles=scatter.legend_elements()[0], labels=classes)
        plt.show()

        
class RecommendationModel2:
    def __init__(self,df,dfAll,pIde,dfClean,dfScraped):
        self.df = df
        self.dfAll=dfAll
        self.pIde=pIde
        self.dfClean = dfClean
        self.dfScraped = dfScraped
        
    #Recommend n candidate similar to a perfect profile
    def recommendTopn(self,nomProfil,indexProfil,n):
        sim=[]
        listfProfile = list(self.pIde.iloc[indexProfil,[0,1,indexProfil,11,12,13,14]])
        for i in range(len(self.df)):
            profil = list(self.df.loc[i,:])
            produit_scalaire = 0
            for i in range(len(profil)):
                produit_scalaire+=round(profil[i],6)*round(listfProfile[i],6)
            produit_norm = round(LA.norm(profil)*LA.norm(listfProfile),6)
            similarity =round(produit_scalaire/produit_norm,6)
            """"
            similarity =1-cosine(profil,listfProfile)
            """
            sim.append(similarity)
            
        self.dfAll['similarity']=sim
        recommended = self.dfAll.sort_values([nomProfil,'similarity'],ascending=False).iloc[0:n,[0,1]]
        return recommended
    
    # Evaluate Topn Recommendation
    def evaluationByPlotting(self,similarityDf):
        fgh = similarityDf.iloc[:,2:]
        objs=[fgh.iloc[:,[0,1,3,11,12,13,14]],self.pIde.iloc[:,[0,1,3,11,12,13,14]]]
        testtest = pd.concat(objs)
        ss1 = StandardScaler()
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(testtest)
        reduced = ss1.fit_transform(reduced)
        t = reduced.transpose()
        fig, ax = plt.subplots(figsize=(10,10))
        for i in range(len(testtest)):
            print(i)
            if(i==6):
                ax.plot([-1.2,t[0][i]],[-1.2,t[1][i]],'r-')
            if(i<5):
                typep='ro'
                ax.plot([-1.2,t[0][i]],[-1.2,t[1][i]],'g-')
            else:
                typep='bs'
                #ax.plot([-1.2,t[0][0]],[-1.2,t[1][0]],'y--')
            ax.plot(t[0][i],t[1][i],typep)

        for i,txt in enumerate(testtest.index):
            ax.annotate(txt, (t[0][i], t[1][i]))
        plt.ylim(-2,3)
        plt.xlim(-2,3)
        return plt
    
    def evaluateTopnByExecutionTime(self,nomProfil,indexProfil,n):
        tic = time.time()
        self.recommendTopn(nomProfil,indexProfil,n)
        tak = time.time()
        print("Executionn time was ----------> "+str(tak-tic))
    
    
    #Recommend n candidates similar to a candidate
    def similarProfile(self,index,n):
        profSimilar = self.dfClean.iloc[index,:]
        sim=[]
        for i in range(len(self.df)):
            profil = list(self.dfClean.loc[i,:])
            produit_scalaire = 0
            for i in range(len(profil)):
                produit_scalaire+=profil[i]*profSimilar[i]
            produit_norm = LA.norm(profil)*LA.norm(profSimilar)
            similarity =produit_scalaire/produit_norm
            sim.append(round(round((similarity+0.000001),5)*100,2))
        self.dfAll['similarityProfile'] =sim
        recommended = self.dfAll.sort_values('similarityProfile',ascending=False).iloc[0:n,[0,1,-1]]
        return recommended

    def similarProfileScrap(self):
        profSimilar = self.dfScraped.iloc[0,:]
        sim=[]
        for i in range(len(self.df)):
            profil = list(self.dfClean.loc[i,:])
            produit_scalaire = 0
            for i in range(len(profil)):
                produit_scalaire+=profil[i]*profSimilar[i]
            produit_norm = LA.norm(profil)*LA.norm(profSimilar)
            similarity =produit_scalaire/produit_norm
            sim.append(round(round((similarity+0.000001),5)*100,2))
        self.dfAll['similarityProfile'] =sim
        recommended = self.dfAll.sort_values('similarityProfile',ascending=False).iloc[0:10,[0,1,-1]]
        return recommended
    
    def similarProfileEvaluation(self,similarityDf):
        fgh = similarityDf.iloc[:,3:-3]
        ss1 = StandardScaler()
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(fgh)
        reduced = ss1.fit_transform(reduced)
        
        fig, axes = plt.subplots(figsize=(10,10))
        axes.set_xlim(-6,6) 
        axes.set_ylim(-6,6) 
        for i in range(len(fgh)):
            if i ==0:
                axes.plot(reduced[i,0],reduced[i,1],'bs')
            else:
                axes.plot(reduced[i,0],reduced[i,1],'ro')
        for i in range(len(fgh)):
            axes.annotate(similarityDf['name'][fgh.index[i]],(reduced[i,0],reduced[i,1]))
        plt.plot([-6,6],[0,0],color='silver',linestyle='-',linewidth=1)
        plt.plot([0,0],[-6,6],color='silver',linestyle='-',linewidth=1)
        return plt
    
    def evaluteSimilarProfilByTime(self,index,n):
        tic = time.time()
        self.similarProfile(index,n)
        tak = time.time()
        print("Executionn time was ----------> "+str(tak-tic))
#################################### CHIFA #################################################

class RecommendationModel3:
    def __init__(self,df_profile_type,result,df):
        self.df_profile_type=df_profile_type
        self.result=result
        self.df=df
        for i in df_profile_type.index:
            j=i.replace('/', '')
            with open('Data/Modele_distance_euclidienne/'+j, 'wb') as fp:
                pickle.dump(self.find_top_k_profile(i,result,df_profile_type),fp)
    
    def euclidean_distance(self,row1, row2):
        distance = 0.0
        for i in range(len(row1)-1):
            distance += (row1[i] - row2[i])**2
        return sqrt(distance)
    
    def find_top_k_profile(self,job,result2,df_profile_type2,k=50):
        skills_list=['Javascript', 'SQL', 'NoSQL', 'Nodejs', 'express.js', 'Koa.js',
       'Hapi.js', 'Angular JS', 'React JS', 'Jquery', 'Bash', 'Nginx0', 'C',
       'C++', 'HTML5', 'CSS', 'REST', 'SASS', 'PostCss', 'Webpack', 'Gitlab',
       'Linux', 'Embedded C', 'Embedded C++', 'Java', 'JEE', 'Microservices',
       'Intégration continue', 'Docker', 'AWS', 'NodeJS', 'Ext.js', 'HTML',
       'MongoDB', 'MySQL', 'Spring', 'SOA', 'SOAP', 'Git', 'SVN', 'Jira',
       'Confluence', 'Spring Boot', 'Spring Security', 'Java 8', 'PHP',
       'Symfony', 'Restfull API', 'GIT', 'CMS', 'Drupal', 'Scrum',
       'Analyse fonctionnelle', 'Testing', 'Rédaction']
        result2=self.result.copy()
        for i in skills_list:
            result2[i]=result2[i]*df_profile_type2[i][job]
    
        sc=StandardScaler()
        result3=pd.DataFrame(sc.fit_transform(result2),columns=result2.columns)
        df_profile_type3=pd.DataFrame(sc.fit_transform(df_profile_type2),columns=df_profile_type2.columns,index=df_profile_type2.index)
    
        row0 = df_profile_type3.loc[job,:]
        dst=pd.DataFrame(columns=['row','distance'],index=result3.index)
        for row in range(len(result3)):
            distance = self.euclidean_distance(row0, result3.loc[row,:])
            dst.loc[row,'row']=row
            dst.loc[row,'distance']=distance
            rs=pd.merge(dst,self.df,how='left',left_on='row', right_on=self.df.index)
            
        return (rs.sort_values(by='distance').head(k)).iloc[:,[2,3]]
  
    
    



################################ Dhia Slimm ##############################

class RecommendationModel4: 
    dfClean1=pd.DataFrame()
    dfClean2=pd.DataFrame()
    def __init__(self,dfClean1):
        self.dfClean1=dfClean1
    def optimal_avg_duration(self):
        exp=[]
        for i in range(len(self.dfClean1)):
            if(self.dfClean1["months_experience"][i]<36):
        
                if(self.dfClean1["months_experience"][i]==self.dfClean1["average_duration"][i]):
                    exp.append(1)
                else:
                    exp.append(0)         
            if((self.dfClean1["months_experience"][i]>=36) and (self.dfClean1["months_experience"][i]<=120)):
                exp.append(1)
            if(self.dfClean1["months_experience"][i]>120):
                exp.append(0)
        experience=pd.DataFrame(exp,columns=["experience"])
        self.dfClean1["experience"]=experience
    def f_back_end(self,x) :
        if ( (x>=24) and (x<60 ) ) :
            y=  0.111111111 * x + 39.3334
        if ( (x>=60) and (x<96)  ) :
            y=  0.194444 * x + 34.3376
        if  ( x<24 ) :
            y=0
        if (  x>=96  ) :
            y=  52.80978
        return y 
    def f_Java_JEE(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y=  0.222 * x + 36.8
        if ( (x>=60) and (x<96)  ) :
            y=  0.138 * x + 41.752
        if  ( x<36 ) :
            y=0
        if (  x>=96  ) :
            y=  0.057 * x + 49.6
        return y
    def f_PHP_Symfony(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y=  0.20833333333333334 * x + 30.5
        if ( (x>=60) and (x<96)  ) :
            y=  0.1388888888888889 * x + 34.666666666666664
        if  ( x<36 ) :
            y=0
        if (  x>=96  ) :
            y=  47.86111111111111
        return y
    def f_DRUPAL(self,x) :
        if ( (x>=24) and (x<36 ) ) :
            y=  0.10555555555555557 * x + 28.8
        if ( (x>=36) and (x<72)  ) :
            y=  0.186111111111111 * x + 25.900000000000006
        if  ( x<24 ) :
            y=0
        if (  (x>=72) and (x<120) ) :
            y=  0.06666666666666667 * x + 39.3
        if (  x>=120 ) :
            y=  47.233333333333334
        return y
    def f_PO(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y=  0.3333333333333333 * x + 33.0
        if ( (x>=60) and (x<120)  ) :
             y=  0.186111111111111 * x + 25.900000000000006
        if  ( x<36 ) :
            y=0
        if (  (x>=72) and (x<120) ) :
            y=  0.16666666666666666 * x + 35.0
        if (  x>=120 ) :
            y=  47.233333333333334
        return y

    def f_ArchitechteJee(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y=  0.3333333333333333 * x + 33.0
        if ( (x>=60) and (x<120)  ) :
            y=  0.186111111111111 * x + 25.900000000000006
        if  ( x<36 ) :
            y=0
        if (  (x>=72) and (x<120) ) :
            y=  0.16666666666666666 * x + 35.0
        if (  x>=120 ) :
            y=  47.233333333333334
        return y  
    
    def f_front_end(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y= 0.1388888888888889 * x + 31.666666666666664

        if ( (x>=60) and (x<96)  ) :
            y=  0.16666666666666666 * x + 30
        if  ( x<36 ) :
            y=0
        if (  x>=96 ) :
            y=  45.83333333333333
        return y
    
    def f_fullstack_js(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y= 0.166666666 * x + 36.004

        if ( (x>=60) and (x<96)  ) :
            y=  0.194444 * x + 34.33337
        if  ( x<36 ) :
            y=0
        if (  x>=96 ) :
            y=  52.805550000000004
        return y
    
    def f_embarque(self,x) :
        if ( (x>=36) and (x<60 ) ) :
            y= 0.2083333 * x + 32.5002

        if ( (x>=60) and (x<96)  ) :
            y=  0.32608 * x + 28.6963
        if  ( x<36 ) :
            y=0
        if (  x>=96 ) :
            y=  59.6739
        return y
    def calcul_score_back_end(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur Web Back-End"][i] * self.f_back_end(self.dfClean1["months_experience"][i])* 10) + (self.dfClean1["Developpeur Front-End"][i] * self.f_back_end(self.dfClean1["months_experience"][i])*3.15789)  + (self.dfClean1["Développeur Embarqué Middleware"][i]*self.f_back_end(self.dfClean1["months_experience"][i])*3.07692) + (self.dfClean1["Développeur FullStack JS"][i]*self.f_back_end(self.dfClean1["months_experience"][i])*2.38095) +(self.dfClean1["Développeur DRUPAL"][i]*self.f_back_end(self.dfClean1["months_experience"][i])*1.25) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreBackend"])
        self.dfClean1["scoreBackend"]=score
    def calcul_score_java_jee(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur JAVA/JEE"][i] * self.f_Java_JEE(self.dfClean1["months_experience"][i])* 10) + (self.dfClean1["Technical Lead/ Architecte JEE"][i] * self.f_Java_JEE(self.dfClean1["months_experience"][i])*3.75) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreJava/Jee"])
        self.dfClean1["scoreJava/Jee"]=score
        
    def calcul_score_php_symfony(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur PHP/Symfony"][i] * self.f_PHP_Symfony(self.dfClean1["months_experience"][i])* 10) + (self.dfClean1["Développeur DRUPAL"][i] * self.f_PHP_Symfony(self.dfClean1["months_experience"][i])*4.375) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreSymfony"])
        self.dfClean1["scoreSymfony"]=score
        
    def calcul_score_drupal(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur DRUPAL"][i] * self.f_DRUPAL(self.dfClean1["months_experience"][i])* 10) + (self.dfClean1["Développeur Web Back-End"][i] * self.f_DRUPAL(self.dfClean1["months_experience"][i])*0.47619)+ (self.dfClean1["Developpeur Front-End"][i] * self.f_DRUPAL(self.dfClean1["months_experience"][i])*3.157895) +(self.dfClean1["Développeur FullStack JS"][i] * self.f_DRUPAL(self.dfClean1["months_experience"][i])*4.285714)+(self.dfClean1["Développeur PHP/Symfony"][i] * self.f_DRUPAL(self.dfClean1["months_experience"][i])*8) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreDrupal"])
        self.dfClean1["scoreDrupal"]=score
   
    def calcul_score_po(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Product Owner/ PO"][i] * self.f_PO(self.dfClean1["months_experience"][i])* 10) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scorePO"])
        self.dfClean1["scorePO"]=score
    
    def calcul_score_architecte_jee(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Technical Lead/ Architecte JEE"][i] * self.f_ArchitechteJee(self.dfClean1["months_experience"][i])* 10) +(self.dfClean1["Développeur JAVA/JEE"][i] * self.f_ArchitechteJee(self.dfClean1["months_experience"][i])* 2) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreArchitechteJee"])
        self.dfClean1["scoreArchitechteJee"]=score
    
    def calcul_score_front_end(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Developpeur Front-End"][i] * self.f_front_end(self.dfClean1["months_experience"][i])* 10) +(self.dfClean1["Développeur Web Back-End"][i] * self.f_front_end(self.dfClean1["months_experience"][i])* 0.952381)+(self.dfClean1["Développeur FullStack JS"][i] * self.f_front_end(self.dfClean1["months_experience"][i])* 2.380952)+(self.dfClean1["Développeur DRUPAL"][i] * self.f_front_end(self.dfClean1["months_experience"][i])* 1.875) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])       
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreFrontend"])
        self.dfClean1["scoreFrontend"]=score
    
    def calcul_score_fullstack_js(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur FullStack JS"][i] * self.f_fullstack_js(self.dfClean1["months_experience"][i])* 10) +(self.dfClean1["Développeur Web Back-End"][i] * self.f_fullstack_js(self.dfClean1["months_experience"][i])* 0.952381)+(self.dfClean1["Developpeur Front-End"][i] * self.f_fullstack_js(self.dfClean1["months_experience"][i])* 3.157895)+(self.dfClean1["Développeur DRUPAL"][i] * self.f_fullstack_js(self.dfClean1["months_experience"][i])* 3.125) +((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scorefullStackJS"])
        self.dfClean1["scorefullStackJS"]=score
    
    def calcul_score_embarque(self):
        score=[]
        for i in range(len(self.dfClean1)):
            res=0
            res =  (self.dfClean1["Développeur Embarqué Middleware"][i] * self.f_embarque(self.dfClean1["months_experience"][i])* 10) +(self.dfClean1["Développeur Web Back-End"][i] * self.f_embarque(self.dfClean1["months_experience"][i])* 0.952381)+((3-self.dfClean1["languages"][i])*(-1)) +((4-self.dfClean1["high_degree_score"][i])* (-1)) +(100*self.dfClean1["experience"][i])
            if(res!=0):       
                score.append(res/100)
            else:
                score.append(0)
        score=pd.DataFrame(score,columns=["scoreEmbarque"])
        self.dfClean1["scoreEmbarque"]=score

    def sort_PO(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreSymfony","scoreArchitechteJee"])
            df=df.sort_values(by=["scorePO"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scorePO"],ascending=0)
        else:
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_Symfony(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """   
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","scoreArchitechteJee","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreArchitechteJee","scorePO"])
            df=df.sort_values(by=["scoreSymfony"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scoreSymfony"],ascending=0)
        else:
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_JavaJee(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """ 
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreEmbarque","scoreFrontend","scoreArchitechteJee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreJava/Jee"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scoreJava/Jee"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_Frontend(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """ 
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreEmbarque","scoreArchitechteJee","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreFrontend"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scoreFrontend"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_Embarque(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """ 
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreArchitechteJee","scoreFrontend","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreEmbarque"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scoreEmbarque"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_Drupal(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """ 
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreArchitechteJee","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreDrupal"],ascending=0)
        if(info=="all info"):
            df=df.sort_values(by=["scoreDrupal"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        
        return df
    def sort_Backend(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """ 
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreArchitechteJee","scoreDrupal","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreBackend"],ascending=0)
        if(info=="all info") :
            df=df.sort_values(by=["scoreBackend"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_fullStackJS(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scoreArchitechteJee","scoreBackend","scoreDrupal","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scorefullStackJS"],ascending=0)
        if(info=="all info") :
            df=df.sort_values(by=["scorefullStackJS"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def sort_ArchitechteJee(self,info):
        """
        pour voir la totalité de la table écrire "all info " sinon écrire "score only"
        """
        df=self.dfClean1
        if(info=="score only"):
            df=df.drop(columns=["url","subjectivite","months_experience","Développeur Web Back-End","Developpeur Front-End","Développeur Embarqué Middleware","Technical Lead/ Architecte JEE","Développeur FullStack JS","Développeur JAVA/JEE","Développeur PHP/Symfony","Développeur DRUPAL","Product Owner/ PO","high_degree_score","average_duration","languages","experience","scorefullStackJS","scoreBackend","scoreDrupal","scoreEmbarque","scoreFrontend","scoreJava/Jee","scoreSymfony","scorePO"])
            df=df.sort_values(by=["scoreArchitechteJee"],ascending=0)
        if(info=="all info") :
            df=df.sort_values(by=["scoreArchitechteJee"],ascending=0)
        else :
            print("pour voir la totalité de la table écrire 'all info' sinon écrire 'score only'")
        return df
    def recommender(self,nomProfil):
        self.optimal_avg_duration()
        if nomProfil == "Développeur Web Back-End":
            self.calcul_score_back_end()
            return self.sort_Backend("all info")
        if nomProfil == "Developpeur Front-End":
            self.calcul_score_front_end()
            return self.sort_Frontend("all info")
        if nomProfil == "Développeur Embarqué Middleware":
            self.calcul_score_embarque()
            return self.sort_Embarque("all info")
        if nomProfil == "Technical Lead/ Architecte JEE":
            self.calcul_score_architecte_jee()
            return self.sort_ArchitechteJee("all info")
        if nomProfil == "Développeur FullStack JS":
            self.calcul_score_fullstack_js()
            return self.sort_fullStackJS("all info")
        if nomProfil == "Développeur JAVA/JEE":
            self.calcul_score_java_jee()
            return self.sort_JavaJee("all info")
        if nomProfil == "Développeur PHP/Symfony":
            self.calcul_score_php_symfony()
            return self.sort_Symfony("all info")
        if nomProfil == "Développeur DRUPAL":
            self.calcul_score_drupal()
            return self.sort_Drupal("all info")
        if nomProfil == "Product Owner/ PO":
            self.calcul_score_po()
            return self.sort_PO("all info")

def priseDedecision(method,dfCos,dfDiff,dfScore,dfEuc,n):
    df_commun = pd.concat([dfCos,dfDiff,dfScore]).drop_duplicates()
    if(method == 'Scoring'):
        num = []
        rang =0
        for index in df_commun.index:
            k = 0
            if index in dfScore.index:
                k+=2 * (n-rang)
            if index in dfDiff.index:
                k+=1* (n-rang)
            if index in dfCos.index:
                k+=1 * (n-rang)
            if index in dfEuc.index:
                k+=1 * (n-rang)
            num.append(k)
            rang+=1

    if(method == 'Score'):
        num = []
        rang = 0
        for index in df_commun.index:
            k = 0
            if index in dfScore.index:
                k+=1 * (n-rang)
            if index in dfDiff.index:
                k+=2 * (n-rang)
            if index in dfCos.index:
                k+=1 * (n-rang)
            if index in dfEuc.index:
                k+=1 * (n-rang)
            num.append(k)
            rang+=1
    if(method == 'All'):
        num = []
        rang = 0
        for index in df_commun.index:
            k = 0
            if index in dfScore.index:
                k+=1 * (n-rang)
            if index in dfDiff.index:
                k+=1 * (n-rang)
            if index in dfCos.index:
                k+=2 * (n-rang)
            if index in dfEuc.index:
                k+=1 * (n-rang)
            num.append(k)
            rang+=1
    if(method == 'skill'):
        num = []
        rang = 0
        for index in df_commun.index:
            k = 0
            if index in dfScore.index:
                k+=1 * (n-rang)
            if index in dfDiff.index:
                k+=1 * (n-rang)
            if index in dfCos.index:
                k+=1 * (n-rang)
            if index in dfEuc.index:
                k+=2 * (n-rang)
            num.append(k)
            rang+=1

    df_commun["numrecommended"] = num
    return df_commun.sort_values("numrecommended",ascending=False).iloc[0:n,[0,1]]

def top5Skills(dfCandidat):
    dict1 = {}
    for skill in dfCandidat.columns[:-5]:
        var = len(dfCandidat[dfCandidat[skill]!=0])/100
        nbBoites = var // 5
        nbReste = var % 5
        if(nbReste < 2.5):
            dict1[skill] = int(nbBoites*5)
        else:
            dict1[skill] = int(nbBoites*5+5)
    dict2 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1],reverse=True)}
    return {k: dict2[k] for k in list(dict2)[:10]}