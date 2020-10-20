from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib.auth.decorators  import login_required
import pandas as pd
from Wevioo import *
import threading
import pickle



# Create your views here.
with open ('Data/ProfilsIdeaux', 'rb') as fp:
    profilIdeaux = pickle.load(fp)
with open ('Data/RecommendationModel1', 'rb') as fp:
    rec = pickle.load(fp)
candidat = pd.read_csv("Data/candidats.csv")
df = pd.read_csv("Data/df_final_2.csv")
dfClean = df.iloc[:,2:]
dictProfile = {
        "Développeur Web Back-End" : 0,
        "Developpeur Front-End" : 1,
        "Développeur Embarqué Middleware" : 2,
        "Technical Lead/ Architecte JEE" : 3,
        "Développeur FullStack JS" : 4,
        "Développeur JAVA/JEE" : 5,
        "Développeur PHP/Symfony" : 6,
        "Développeur DRUPAL" : 7,
        "Product Owner/ PO" :8,

    } 

def login(request):
    b=11
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if(user.is_superuser):
                return redirect('adminIndex')
            else:
                return redirect('userIndex')
        return render(request,'BackOffice/login.html',{'err':'user not found'})

    else:       
        return render(request,"BackOffice/login.html")        



@login_required
def adminIndex(request):
    user = request.user.username

    ########### HIGH DEGREE ##########
    license = len(df[df["high_degree_score"]==1])
    master = len(df[df["high_degree_score"]==2])
    ing = len(df[df["high_degree_score"]==3])
    ingMast = len(df[df["high_degree_score"]==4])
    unknown = len(df[df["high_degree_score"]==0])
    
    ########## MOBILITY #############
    mobile = len(df[df["mobilité"]==1])/100
    nonmobile = len(df[df["mobilité"]==0])/100
    data = [license,master,ing,ingMast,unknown,mobile,nonmobile]
    ########## TOP SKILLS ###########
    topskills = top5Skills(candidat)
    ########## Languages ############
    lang1 = len(df[df["languages"]==0])
    lang2 = len(df[df["languages"]==1])
    lang3= len(df[df["languages"]==2])
    lang4 = len(df[df["languages"]==3])
    lang  = [lang1,lang2,lang3,lang4]
    ########## EXPERIENCES ############
    twoyears = len(df[df["months_experience"]<=24])/100
    threeyears = len(df[(df["months_experience"]>24) & (df["months_experience"]<=36)])/100
    fouryears = len(df[(df["months_experience"]>36) & (df["months_experience"]<=48)])/100
    fiveyears = len(df[(df["months_experience"]>48) & (df["months_experience"]<=60)])/100
    more_than_five_years =len(df[(df["months_experience"]>60)])/100
    experience = [twoyears,threeyears,fouryears,fiveyears,more_than_five_years]
    return render(request,"BackOffice/indexAdmin.html",{'username' : user,'Data':data,'skills':topskills,'lang':lang,'exp':experience})

@login_required
def pendarationBack(request):
    user = request.user.username
    with open ('Data/Dict_Profil_Competence', 'rb') as fp:
        dictionnaire = pickle.load(fp)
    if(request.method == 'POST'):
        for key,value in dictionnaire.items():
            for key1,value1 in value.items():
                dictionnaire[key][key1]=request.POST[key1+" "+key]
        print(dictionnaire)       
        
    with open('Data/Dict_Profil_Competence', 'wb') as fp:
        pickle.dump(dictionnaire, fp)
    return render(request,"BackOffice/penderation.html",{'username' : user,'dict' : dictionnaire})


@login_required
def userIndex(request):
    user = request.user.username
    return render(request,"FrontOffice/indexUser.html",{'username' : user})


def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required
def allCandidates(request):
    user = request.user.username
    df = pd.read_csv("Data/df_final_2.csv")
    df1 = df.iloc[0:50,[0,1]]
    df1.columns=["LinkedIn URL","Name and LastName"]
    return render(request,"BackOffice/allCandidates.html",{'DataFrame' : df1,'username':user})

@login_required
def cosine(request):
    user = request.user.username
    
    if(request.method == 'POST'):
        profile_score = request.POST["Profile"]
        index_score = dictProfile[profile_score] +2 
        dfSimilarityCalculus = dfClean.iloc[:,[0,1,index_score,11,12,13,14]]
        rec1 = RecommendationModel2(dfSimilarityCalculus,df,profilIdeaux,dfClean,None)
        result = rec1.recommendTopn(profile_score,index_score,int(request.POST["numRec"]))
        result.columns=["LinkedIn URL","Name and LastName"]
        return render(request,"FrontOffice/cosineRecommendation.html",{'username':user,'DataFrame':result})
    return render(request,"FrontOffice/cosineRecommendation.html",{'username':user})

@login_required
def difference(request):
    user = request.user.username

    if(request.method == 'POST'):
        result = rec.recommender(request.POST["Profile"],int(request.POST["numRec"]))
        return render(request,"FrontOffice/differenceRecommendation.html",{'username':user,'DataFrame':result})
    return render(request,"FrontOffice/differenceRecommendation.html",{'username':user})

@login_required
def euclidean(request):
    user = request.user.username
    if(request.method == 'POST'):
        ch= request.POST["Profile"]
        ch=ch.replace('/', '')
        print("############################################"+ch)
        with open ('Data/Modele_distance_euclidienne/'+ch, 'rb') as fp:
            data = pickle.load(fp)
        result = data.head(int(request.POST["numRec"]))
        return render(request,"FrontOffice/euclideanRecommendation.html",{'username':user,'DataFrame':result})
    return render(request,"FrontOffice/euclideanRecommendation.html",{'username':user})

@login_required
def decision(request):
    user = request.user.username

    if(request.method == 'POST'):
        profile_score = request.POST["Profile"]
        index_score = dictProfile[profile_score] + 2 
        dfSimilarityCalculus = dfClean.iloc[:,[0,1,index_score,11,12,13,14]]
        rec1 = RecommendationModel2(dfSimilarityCalculus,df,profilIdeaux,dfClean,None)
        dfCos = rec1.recommendTopn(profile_score,index_score,int(request.POST["numRec"]))
        
        
        dfDiff = rec.recommender(profile_score,int(request.POST["numRec"]))

        rec2 = RecommendationModel4(df)
        dfScore = rec2.recommender(request.POST["Profile"]).iloc[0:int(request.POST["numRec"]),[0,1]]


        ch= request.POST["Profile"]
        ch=ch.replace('/', '')
        print("############################################"+ch)
        with open ('Data/Modele_distance_euclidienne/'+ch, 'rb') as fp:
            data = pickle.load(fp)
        dfEuc = data.head(int(request.POST["numRec"]))

        result = priseDedecision(request.POST["method"],dfCos,dfDiff,dfScore,dfEuc,int(request.POST["numRec"]))

        return render(request,"FrontOffice/priseDeDecision.html",{'username':user,'DataFrame':result})
    return render(request,"FrontOffice/priseDeDecision.html",{'username':user})



@login_required
def similarity(request):
    user = request.user.username
    user = request.user.username
    with open ('Data/ProfilsIdeaux', 'rb') as fp:
        profilIdeaux = pickle.load(fp)
    df = pd.read_csv("Data/df_final_2.csv")
    df_affiche = df.iloc[0:30,[1,2,3]]
    df_affiche.columns=[" ","LinkedIn URL","Name and LastName"]
    if(request.method == 'POST'):
        profile_username = request.POST["urlprofile"][28:]
        cookie = "AQEDATB53fcBsaTWAAABccXf7DcAAAFx6exwN1YANvL_6nFmyrULi6T1gPVnjp0h91HkH1lEPVFyr00kgX4i2ASQOnzaHEGNkmPiPAyO2Xg7wv06406qzauKPJO37MNaGUbFBO_86L_UqbogzdVmCARO"
        profile = Preparation(profile_username,cookie)
        df_scrapped = profile.preparer().iloc[:,2:]
        dfClean = df.iloc[:,2:]
        dfSimilarityCalculus = dfClean.iloc[:,[0,1,3,11,12,13,14]]
        rec = RecommendationModel2(dfSimilarityCalculus,df,profilIdeaux,dfClean,df_scrapped)

        topSimilarN = rec.similarProfileScrap() 
        
        return render(request,"FrontOffice/similariteCondidat.html",{'username':user,'DataFrame' : topSimilarN})

    return render(request,"FrontOffice/similariteCondidat.html",{'username':user})


@login_required
def internalSimilarity(request):
    user = request.user.username
    with open ('Data/ProfilsIdeaux', 'rb') as fp:
        profilIdeaux = pickle.load(fp)
    df = pd.read_csv("Data/df_final_2.csv")
    df_affiche = df.iloc[0:30,[0,1]]
    df_affiche.columns=["LinkedIn URL","Name and LastName"]
    if(request.method == 'POST'):
        dfClean = df.iloc[:,2:]
        dfSimilarityCalculus = dfClean.iloc[:,[0,1,3,11,12,13,14]]
        rec = RecommendationModel2(dfSimilarityCalculus,df,profilIdeaux,dfClean,None)
        indexProfile = int(request.POST["indice"])
        topSimilarN = rec.similarProfile(indexProfile,10) 
        topSimilarN.columns=["LinkedIn URL","Name and LastName","Pourcentage de similarité"]
        return render(request,"FrontOffice/similariteCondidatInterne.html",{'username':user,'DataFrame' : topSimilarN})
    return render(request,"FrontOffice/similariteCondidatInterne.html",{'username':user,'DataFrame' : df_affiche})

@login_required
def scoring(request):
    user = request.user.username
    if(request.method == 'POST'):
        rec1 = RecommendationModel4(df)
        result = rec1.recommender(request.POST["Profile"]).iloc[0:int(request.POST["numRec"]),[0,1]]
        return render(request,"FrontOffice/scoringRecommendation.html",{'username':user,'DataFrame' : result})
    return render(request,"FrontOffice/scoringRecommendation.html",{'username':user})