#########################              BIENVENUE SUR PYSTAGE              #########################


# Importation des librairies numpy, pandas et tkinter

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import *
#pip install customtkinter
import customtkinter
#pip install plotly
import plotly.graph_objects as go
import plotly.express as px
import webbrowser
import os
import json
#pip install folium
import folium
#pip install xlrd 'si pas à jour'
#pip install openpyxl 'si toujours pas à jour'
from PIL import Image 
from PIL import ImageDraw 
from PIL import ImageFont 

#permet de regrouper des variables selon un dictionnaire établi
def variabiliser(df,nomDeColonne,dicoVariables,nomNouvelleColonne):
    variablesADegager = df[nomDeColonne]
    listeNouvelleVariable=[0]*len(variablesADegager)
    index=-1
    for uneVariable in variablesADegager:
        index+=1
        for laVariable in dicoVariables:
            if isinstance(dicoVariables[laVariable], list):
                for unElement in dicoVariables[laVariable]:
                    if unElement in uneVariable:
                        listeNouvelleVariable[index]=laVariable
                    else:
                        if listeNouvelleVariable[index]==0:
                            listeNouvelleVariable[index]='Autres'
            else:
                if dicoVariables[laVariable] in uneVariable:
                    listeNouvelleVariable[index]=laVariable
                else:
                    if listeNouvelleVariable[index]==0:
                        listeNouvelleVariable[index]='Autres'
    dfFinal = df
    dfFinal[nomNouvelleColonne]=listeNouvelleVariable
    return dfFinal

#permet de compter le nombre de stages en fonction d'un paramètre
def creerDataFrame(df,nomdeColonne):
    df2 = df.drop_duplicates(subset = [nomdeColonne])
    colonne = df[nomdeColonne]
    colonne2 = df2[nomdeColonne]
    nbColonne = [0] * len(colonne2)
    listeVariables = []
    index = -1
    for laFormation in colonne2:
        index+=1
        listeVariables.append(laFormation)
        for uneFormation in colonne:
            if laFormation == uneFormation:
                nbColonne[index]+=1  
    df3 = pd.DataFrame(
        {'Colonne':listeVariables,
         'Nombre de stages': nbColonne
         })
    return df3

#permet de dessiner un barchat avec des hover
def dessinerBar(df,descending,repartition,annee):
    if type(annee) is list: 
            titre = "Répartiton des " + str(repartition) + " sur toutes les années"
    else:
        if len(annee)==8:
            titre = "Répartiton des " + str(repartition) + " entre " + str(annee[0:4])+" et "+str(annee[4:9])
        else:
            titre = "Répartiton des " + str(repartition) + " en " + str(annee)
    couleur = ['#d39c83']*len(df)
    fig = px.bar(df, x='Colonne', 
                 y='Nombre de stages',
                 color_discrete_sequence=couleur,
                 hover_data=['topEntreprise','nbStructure']
                 )
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(title={
                            'text':titre,
                            'y':0.97,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    if descending:
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    fig.write_html("Html\\barchart.html")

#permet de dessiner un diagramme en ligne
def dessinerLigne(df):
    fig = px.line(dfFin, x="Année", y="Nombre de stages",width=750,height=700,color='Formation',markers= True,title="Évolution du nombre de stages par formation",color_discrete_sequence=px.colors.qualitative.Antique)
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(title_x=0.5,paper_bgcolor="#817D7D")
    fig.update_traces(line=dict(width=4),marker=dict(size=12))
    fig.write_html("Html\\ligne.html")

#permet de dessiner un pie chart
def dessinerCamembert(df,plus,dimension,repartition,annee):
    if type(annee) is list:
            titre = "Répartiton des " + str(repartition) + " sur toutes les années"
    else:
        if len(annee)==8:
            titre = "Répartiton des " + str(repartition) + " entre " + str(annee[0:4])+" et "+str(annee[4:9])
        else:
            titre = "Répartiton des " + str(repartition) + " en " + str(annee)
    fig = px.pie(df, values='Nombre de stages', names='Colonne',
             title=titre,
             custom_data=['topEntreprise','nbStructure'], labels={'topEntreprise':'Meilleure structure','nbStructure':'Nombre de structures'},
             color_discrete_sequence=px.colors.sequential.Brwnyl,
             width=dimension[0],
             height=dimension[1])
    fig.update_traces(textposition='inside', textinfo='percent+label',\
                 hovertemplate = "Departement:%{label}: <br>Nombre de stages: %{value} </br>(Meilleure structure, Nombre de structures) : %{customdata}")
    fig.update_layout(title_x=0.5)
    nom_html = "html\\camembert"+str(plus)+".html"
    fig.write_html(nom_html)

#Création d'une fonction qui retranscrit les éléments sélectionnés de notre listbox
def selected_Annee():
    for i in optAnnee.curselection():
        if optAnnee.get('active') == 'Toutes': 
            lstAnnee.insert(i,allitemAnnee) 
            optAnnee.selection_clear(1,'end')
            optAnnee.itemconfig(i,foreground = 'lightgray')
            optAnnee.itemconfig(0, foreground = "Black")
        else:
            print(optAnnee.get(i))
            lstAnnee.insert(i, optAnnee.get(i))
            optAnnee.selection_clear(0)
            optAnnee.itemconfig(0,foreground = 'lightgray')
            optAnnee.itemconfig(i, foreground = "Black")

def selected_formation():
    for i in optformation.curselection():
        if optformation.get('active') == 'Toutes': 
            lstFormation.insert(i,allitemFormation) 
            optformation.selection_clear(1,'end')
            optformation.itemconfig(i,foreground = 'lightgray')
            optformation.itemconfig(0, foreground = "Black")
        else:
            print(optformation.get(i))
            lstFormation.insert(i, optformation.get(i))
            optformation.selection_clear(0)
            optformation.itemconfig(0,foreground = 'lightgray')
            optformation.itemconfig(i, foreground = "Black")

def selected_Diplome():
    for i in optDiplome.curselection():
        if optDiplome.get('active') == 'Tous': 
            lstDiplome.insert(i,allitemDiplome) 
        else:
            print(optDiplome.get(i))
            lstDiplome.insert(i, optDiplome.get(i))

def tous():
    selected_Annee()
    selected_Diplome()
    selected_formation()

def create():
    app.destroy()
    webbrowser.open_new_tab("html\\HtMl.html")

#effectuer un podium sur un dataframe
def Top(df,colonneTop,nombreTop,TopCb):
    df2 = df.groupby([colonneTop]).count()
    top = df2[nombreTop].nlargest(n=TopCb)
    top = top.rename_axis('nom_entreprise').reset_index()
    return top

#sert d'enlever à un dataframe une valeur précise
def enleverValeur(df,colonne,valeur):
    indexNames = df[df[colonne]==valeur].index
    df2 = df.drop(indexNames)
    return df2

#sert de garder une valeur précise d'un dataframe
def garderValeur(df,colonne,valeur):
    indexNames = df[df[colonne]!=valeur].index
    df2 = df.drop(indexNames)
    return df2

def add_data_GeoJson_Monde(map):
    commune_data = folium.features.GeoJson(
        data=pays,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["name","nbstage","topstructure","nbstructure"],
            aliases=["Pays : ","Nombre de stage : ","Structure avec le plus d'embauche : ","Nombre de structure d'acceuil : "],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            ),
            sticky=False,
        ),
    )
    map.add_child(commune_data)
    map.keep_in_front(commune_data)

def add_data_GeoJson_Region(map):
    commune_data = folium.features.GeoJson(
        data=region,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["nom","nbstage","topstructure","nbstructure"],
            aliases=["Région : ","Nombre de stage : ","Structure avec le plus d'embauche : ","Nombre de structure d'acceuil : "],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            ),
            sticky=False,
        ),
    )
    map.add_child(commune_data)
    map.keep_in_front(commune_data)

def add_data_GeoJson_Commune(map):
    commune_data = folium.features.GeoJson(
        data=commune,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["nom","codepostal","nbstage","topstructure","nbstructure"],
            aliases=["Commune : ","Code postal : ","Nombre de stage : ","Structure avec le plus d'embauche : ","Nombre de structure d'acceuil : "],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            ),
            sticky=False,
        ),
    )
    map.add_child(commune_data)
    map.keep_in_front(commune_data)


# Permet de créer un fichier csv à  partir d'un excel 
datacsv = 'Base_AREXIS.csv'

#Si le fichier excel existe déjà alors on le lis
if os.path.isfile(datacsv):
    arexis = pd.read_csv('Base_AREXIS.csv', sep=';')
    
#Sinon on créer un fichier csv à partir du fichier excel. Cela permet d'améliorer la fluidité de notre outil
else:
    arexis = pd.read_excel('Base_AREXIS.xlsx')
    arexis.to_csv ("Base_AREXIS.csv", sep=";") 


#Création d'un dictionnaire pour regrouper toutes les formations sans prendre en compte les options
dicoFormation = {"GEA":["GEA","Gestion des Entreprises et des Administrations"],"STID":"Statistique","HSE":"Hygiène","GMP":"Mécanique","GEII":"Electrique","TechdeCo":"Commercialisation","GTE":"Thermique","Chimie":"Chimie","Civil":"Civil","MP":"Physiques","LP Métiers":"Métiers","Autres":'0'}
dicoSecteur = {"Emploi":["86","7"],"Industriel":["1","2","3"],"BTP":["41","42","43"],"Commerce":["45","46","47"],"Banque/Assurance":["64","65","66"],"Erreur":"n"}


#Enlever les nan qu'on a remplacer par du vide
arexis.fillna('',inplace=True)


#Remplacement des DUT01 et DUT02 par DUT1 et DUT2
replaceDUT01 = {'DUT01':'DUT1'}
arexis = arexis.replace(replaceDUT01)
replaceDUT02 = {'DUT02':'DUT2'}
arexis = arexis.replace(replaceDUT02)


# Le data frame est transposé dans un tableau numpy
tableauData = np.array(arexis)


#Permet d'affecter la fonction sur notre data Frame initial afin d'avoir les formations regrouper
data2 = variabiliser(arexis,'intitule',dicoFormation,'formationGen')
  
annee_double = np.array(arexis["idexercice"])  
annee_double2 = pd.unique(annee_double)


#On crée une liste dans laquelle on va ajouter chaque année unique ainsi qu'une selection all 
OptionListAnnee = ["Toutes"]


#On ajoute chaque année unqiue à  notre liste contant le all
for i in range(len(annee_double2)):
    OptionListAnnee.append(annee_double2[i])
    

#Formatage de la page 

app = tk.Tk()
app.title('Interface PYstage')
app.geometry('800x700')
app.resizable(width=0, height=0)
app.configure(bg='#C5D1DC')
app.iconphoto(False, tk.PhotoImage(file='./image/PYstage.png'))

yscrollbarAnnee = Scrollbar(app, repeatdelay = 0, bg = "#E4C79B", bd= 0,highlightthickness = 0,highlightcolor ="#E4C79B", repeatinterval = 50,troughcolor = "#E4C79B",activebackground = '#E8C695' )
yscrollbarAnnee.pack()  
yscrollbarAnnee.place(x=230,y=480,width=13, height=100)

yscrollbarformation = tk.Scrollbar(app, repeatdelay = 0)
yscrollbarformation.pack()  
yscrollbarformation.place(x=480,y=480,width=13, height=100)
yscrollbarformation.config (background ='#1F6AA4', borderwidth = 0, relief  = 'flat')

yscrollbarDiplome = tk.Scrollbar(app, background ='#1F6AA4', borderwidth = 0, repeatdelay = 0)
yscrollbarDiplome.pack()  
yscrollbarDiplome.place(x=755,y=480,width=13, height=100)

login_btn = PhotoImage(file = "./image/layouttk.png") 

img = Button(app, image = login_btn, borderwidth = 0) 
img.pack(side = "bottom", fill = "both", expand = "yes") 


#compteur qui compte le nombre d'éléments dans notre liste
compteur = 0


#Création de la listbox à choix multiples pour les années

optAnnee = Listbox(app,selectmode = "multiple",height=5, yscrollcommand = yscrollbarAnnee.set,exportselection = False, activestyle = 'none',justify = 'center', selectbackground = '#CCDDCC' ,background = '#CCDDCC',font =('Times', '11', 'italic'),borderwidth = 0,bd=5, relief = 'flat',highlightbackground="#CCDDCC",highlightcolor ="#CCDDCC" )
for f in range(len(OptionListAnnee)):
    optAnnee.insert(f,OptionListAnnee[f])
    optAnnee.pack()
    optAnnee.place(x = 50,y = 292)
    compteur += 1
yscrollbarAnnee.config(command = optAnnee.yview)

#Création d'une liste dans lequel on considére que chaque élèment sont cliqués, cette liste sera affectées à  l'option all
allitemAnnee = []
allitemAnnee += optAnnee.get(1,compteur)

lstAnnee = []


#Même procédure pour les pays de stages
formation = np.array(arexis["formationGen"])        
formation_double = pd.unique(formation)

OptionListformation  =  ["Toutes"]

for a in range(len(formation_double)):      
    OptionListformation.append(formation_double[a])
 
    
compteur = 0  

optformation = Listbox(app,selectmode = "multiple",height=5,exportselection = False, activestyle = 'none', selectbackground = '#CCDDFF' ,background = '#CCDDFF',justify = 'center',font =('Times', '11', 'italic'),borderwidth = 0,bd=0,relief = 'flat',highlightbackground="#CCDDFF",highlightcolor ="#CCDDFF",disabledforeground = 'lightgray')
for h in range(len(OptionListformation)):
    optformation.insert(h,OptionListformation[h])
    optformation.pack()
    optformation.place(x = 315,y = 292)
    compteur += 1
yscrollbarformation.config(command = optformation.yview )

quitte = tk.Button(app, text="Quit", command=app.destroy, font = ("Helvetica",'12',"bold"))
quitte.pack()
quitte.place(x=900,y=10)

lstFormation = []
allitemFormation = []
allitemFormation += optformation.get(1,compteur)


diplome = np.array(arexis["type_diplome"])         
diplome_double = pd.unique(diplome)
 
OptionListDiplome  =  ["Tous"]

for a in range(len(diplome_double)):      
    OptionListDiplome.append(diplome_double[a])
 

compteur = 0   
    
optDiplome = Listbox(app,selectmode = "multiple",height=5, yscrollcommand = yscrollbarDiplome.set,exportselection = False, activestyle = 'none',justify = 'center', selectbackground = '#FBAA99' ,selectforeground ="white",background = '#FBAA99',font =('Times', '11', 'italic'),borderwidth = None,bd=5,relief = 'flat',highlightbackground="#FBAA99",highlightcolor ="#FBAA99" )
for h in range(len(OptionListDiplome)):
    optDiplome.insert(h,OptionListDiplome[h])
    optDiplome.pack()
    optDiplome.place(x = 565,y = 292)
    compteur += 1
yscrollbarDiplome.config(command = optDiplome.yview )

    
quitte = tk.Button(app, text="Quit", command=app.destroy,relief = 'flat', foreground = 'white',activeforeground = 'red', background = '#000000',font=("Arial", 13),highlightthickness = 0,overrelief = 'flat',height=1,width=4,activebackground = "#000000",borderwidth = 0)
quitte.pack()
quitte.place(x=727,y=15)


lstDiplome = []
    
allitemDiplome = []
allitemDiplome += optDiplome.get(1,compteur)


label = ''
idx = optDiplome.get(0,tk.END).index(label)
optDiplome.delete(idx)

values = [optDiplome.get(idx) for idx in optDiplome.curselection()]


btnDiplome = tk.Button(app, text='Confirmer', command=tous,width=10,relief = 'flat',foreground = '#000000', background = '#97C2EA',font=("Arial", 13),activeforeground  = 'green',highlightthickness = 0,overrelief = 'flat', activebackground = "#97C2EA",borderwidth = 0)
btnDiplome.bind('<Button-1>')

 
# Placer le bouton et la listbox
btnDiplome.pack()
btnDiplome.place(x=355,y=492)


btnPlus= tk.Button(app, text='Afficher graphique',command = create,width=15,relief = 'flat',foreground = '#000000',activeforeground = 'darkblue', background = '#97C2EA',font=("Arial", 13), highlightthickness = 0,overrelief = 'flat',activebackground = '#97C2EA',borderwidth = 0)
btnPlus.bind('<Button-1>')

 
# Placer le bouton et la listbox
btnPlus.pack()
btnPlus.place(x=590,y=569)

app.mainloop()

for i in range(len(lstAnnee)):
    lstAnnee += lstAnnee[i]

for i in range(len(lstDiplome)):
    lstDiplome += lstDiplome[i]
    
for i in range(len(lstFormation)):
    lstFormation += lstFormation[i]
    

# Création des data frame avec les filtres appliqués

filtre = arexis.query("idexercice == " + str(lstAnnee) + '')

filtre2 = arexis.query("formationGen == " + str(lstFormation) + '' )

filtre3 = arexis.query("type_diplome == " + str(lstDiplome) + '')

final = pd.merge(filtre, filtre2)
final2 = pd.merge(final, filtre3)


#gestion de la transformation du code NAF en secteur
df=final2
secteurNAF = df['naf']
listeSecteur = []
for unSecteur in secteurNAF:
    if  unSecteur!='':
        if str(unSecteur)[0]=='4' or str(unSecteur)[0]=='6' or str(unSecteur)[0]=='8':
            listeSecteur.append(str(unSecteur)[0:2])
        else:
            listeSecteur.append(str(unSecteur)[0])
    else:
        listeSecteur.append('n')
df['codeSecteur']=listeSecteur
dicoSecteur = {"Emploi":["86","7"],"Industriel":["1","2","3"],"BTP":["41","42","43"],"Commerce":["45","46","47"],"Banque/Assurance":["64","65","66"],"Erreur":"n"}
dfFiltré = variabiliser(df,'codeSecteur',dicoSecteur,'secteur')
dfFin = creerDataFrame(dfFiltré,'secteur')
dfFinFin1 = enleverValeur(dfFin, 'Colonne', 'Erreur')

codeNAF = dfFinFin1['Colonne']
nomEntreprise=[]
nbStructure=[]
total=0
for unCode in codeNAF:
    data = garderValeur(dfFiltré,'secteur',unCode)
    nomEntreprise.append(Top(data,'denom_social','Exercice',1)['nom_entreprise'][0])
    nbStructure.append(len(creerDataFrame(data,'denom_social')['Nombre de stages']))
dfFinFin1['topEntreprise']=nomEntreprise
dfFinFin1['nbStructure']=nbStructure



#gestion de la transformation du code postal en departement
df=final2
codePostal = df['cp_service']
listeDep = []
for unDepartement in codePostal:
    if unDepartement !='':
        if str(unDepartement)[0:2]=='86' or str(unDepartement)[0:2]=='79' or str(unDepartement)[0:2]=='16' or str(unDepartement)[0:2]=='17':
            listeDep.append(str(unDepartement)[0:2])
        else:
            listeDep.append('Autres')
    else:
        listeDep.append('n')
df['codeDepartement']=listeDep
dicoDepartement = {"Vienne":"86","Deux-Sèvres":"79","Charente":"16","Charente-Maritime":"17"}
dfFiltré = variabiliser(df,'codeDepartement',dicoDepartement,'departementPC')
dfFin = creerDataFrame(dfFiltré,'departementPC')
dfFinFin2 = enleverValeur(dfFin, 'Colonne', 'Autres')

departement = dfFinFin2['Colonne']
nomEntreprise=[]
nbStructure=[]
total=0
for unDepartement in departement:
    data = garderValeur(dfFiltré,'departementPC',unDepartement)
    nomEntreprise.append(Top(data,'denom_social','Exercice',1)['nom_entreprise'][0])
    nbStructure.append(len(creerDataFrame(data,'denom_social')['Nombre de stages']))
dfFinFin2['topEntreprise']=nomEntreprise
dfFinFin2['nbStructure']=nbStructure

dfFiltré = variabiliser(final2,'intitule',dicoFormation,'formationGen')
dfFin = creerDataFrame(dfFiltré,'formationGen')
dfFinFin = enleverValeur(dfFin, 'Colonne', 'Autres')

#gestion de la transformation de la formation pour barchart
formation = dfFinFin['Colonne']
nomEntreprise=[]
nbStructure=[]
for uneFormation in formation:
    data = garderValeur(dfFiltré,'formationGen',uneFormation)
    nomEntreprise.append(Top(data,'denom_social','Exercice',1)['nom_entreprise'][0])
    nbStructure.append(len(creerDataFrame(data,'denom_social')['Nombre de stages']))
 
dfFinFin['topEntreprise']=nomEntreprise
dfFinFin['nbStructure']=nbStructure   


#gestion des erreurs en cas de dataframe vide
if len(final2)!=0:
    if lstAnnee != []:
        if len(lstAnnee[1])>=2 and type(lstAnnee[0]) is not list:
            contane = -1
            for uneAnnee in lstAnnee:
                if len(uneAnnee)!=1:
                  contane+=1    
            annee = str(lstAnnee[contane][0:4])+str(lstAnnee[0][5:9])
            dessinerCamembert(dfFinFin1,'',[630,380],'structures',annee)
            dessinerCamembert(dfFinFin2,1,[630,380],'departements',annee) 
            dessinerBar(dfFinFin,True,'formations',annee)
        else:
            dessinerCamembert(dfFinFin1,'',[630,380],'structures',lstAnnee[0])
            dessinerCamembert(dfFinFin2,1,[630,380],'departements',lstAnnee[0]) 
            dessinerBar(dfFinFin,True,'formations',lstAnnee[0])
else:
    ar = np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0]])
    prout = pd.DataFrame(ar, columns = ['Colonne','Nombre de stages','topEntreprise','nbStructure'])
    dessinerCamembert(dfFinFin1,'',[630,380],'structures','')
    dessinerCamembert(dfFinFin2,1,[630,380],'departements','') 
    dessinerBar(prout,True,'formations','')
    
#creation du dataframe du nombre de stages par formation en fonction de l'année pour diagramme en ligne   
df = variabiliser(arexis,'intitule',dicoFormation,'formationGen')
dfFiltré = creerDataFrame(df,'formationGen')
formation = dfFiltré['Colonne']
perkastor=0
for uneFormation in formation:
    data = garderValeur(df,'formationGen',uneFormation)
    if perkastor == 0:
        perkastor=1
        dfFin = creerDataFrame(data, 'idexercice')
        dfFin=dfFin.assign(Formation=uneFormation)
        dfFin.columns = ['Année', 'Nombre de stages','Formation']
    else:
        dfInter = creerDataFrame(data, 'idexercice')
        dfInter=dfInter.assign(Formation=uneFormation)
        dfInter.columns = ['Année', 'Nombre de stages','Formation']
        dfFin = pd.concat([dfFin, dfInter],ignore_index = True,sort = False)

dessinerLigne(dfFin)

###########################                nb stage              ##################################

pays = json.load(open("./carte/monde.geojson"))

df = creerDataFrame(final2,"idpays_service")

listePays = [i["id"] for i in pays["features"]]
stagesAssoc = [0] * (len(listePays))

nbstage = df["Nombre de stages"]
nompays = df["Colonne"]
stagesAssocPresents = []
paysPresents = []

for unStage in nbstage :
    stagesAssocPresents.append(unStage)

for unPays in nompays :
    paysPresents.append(unPays)
    
compteur = 0
compteur2 = 0

for aaa in listePays : 
    for bbb in paysPresents :
        if str(aaa) == str(bbb) :
            stagesAssoc[compteur] = stagesAssocPresents[compteur2]
        compteur2 += 1
    compteur +=1
    compteur2 = 0

dffifi = pd.DataFrame({
    "Pays" : listePays,
    "Unite" : stagesAssoc
    }) 



pret = []
for a in range (0,len(listePays)) :
    dic = { "nbstage" : stagesAssoc[a]}
    pret.append(dic)

for aa in range(len(pret)) :
    pays["features"][aa]["properties"].update(pret[aa])

#########################                 top structure            ######################################

listeStruc = []
for un in listePays :
    if un in paysPresents :
        dataframe = garderValeur(final2, 'idpays_service', un)
        top = Top(dataframe,'denom_social','Exercice',1)
        toptop = top["nom_entreprise"]
        for unun in toptop :
            listeStruc.append(unun)
    else :
        listeStruc.append("Pas de donnée")

pret2 = []
for az in range (0,len(listePays)) :
    dic2 = { "topstructure" : listeStruc[az]}
    pret2.append(dic2)

for aa2 in range(len(pret2)) :
    pays["features"][aa2]["properties"].update(pret2[aa2])

 
#########################          nombre de structure d'acceuil        ####################################
nbStruc = []
for prout in listePays :
    if prout in paysPresents :
        dataframe = garderValeur(final2, 'idpays_service', prout)
        liste = dataframe['denom_social']
        listev2 = []
        for undenom in liste :
            listev2.append(undenom)
        listev3 = np.unique(listev2)
        sheeesh = len(listev3)
        nbStruc.append(sheeesh)
    else : 
        nbStruc.append("0")

pret3 = []
for azz in range (0,len(listePays)) :
    dic3 = { "nbstructure" : nbStruc[azz]}
    pret3.append(dic3)

for aa3 in range(len(pret3)) :
    pays["features"][aa3]["properties"].update(pret3[aa3])
    
    
######################       carte      #############################################################
    
monde = folium.Map(location = [30, 15],zoom_start=1)

folium.Choropleth(
    geo_data = pays,
    data = dffifi,
    name="choropleth",
    columns = ["Pays","Unite"],
    key_on="feature.id",
    color = "blue",
    fill_color='YlOrRd',
    legend_name='Nombre de stages',
    fill_opacity=0.6,
    line_opacity=0.5,
).add_to(monde)

# folium.LayerControl().add_to(monde)




style_function = lambda x: {
        "color": "#FFFFFF",
        "fillOpacity": 0,
        "weight": 0.1,
    }

highlight_function = lambda x: {
    "fillColor": "#000000", #couleuru tout
    "color": "#000000",   #couleur des bords
    "fillOpacity": 0.75,
    "weight": 0.3,
}






add_data_GeoJson_Monde(monde)

folium.LayerControl().add_to(monde)



monde.save("html\\onycroit.html")



region = json.load(open("./carte/regions.geojson"))


data2 = garderValeur(final2, "nom_pays_court", 'FRANCE')

liste11 = ['75','77','78','91','92','93','94','95']
liste24 = ['18','28','36','37','41','45']
liste27 = ['21','25','39','58','70','71','89','90']
liste28 = ['14','27','50','61','76']
liste32 = ['59','60','62','80']
liste44 = ['08','10','51','52','54','55','57','67','68','88']
liste52 = ['44','49','53','72','85']
liste53 = ['22','29','35','56']
liste75 = ['16','17','19','23','24','33','40','47','64','79','86','87']
liste76 = ['09','11','12','30','31','32','34','46','48','65','66','81','82']
liste84 = ['01','03','07','15','26','38','42','43','63','69','73','74']
liste93 = ['04','05','06','13','83','84']
liste94 = ['02']


a = data2["cp_service"]
a = list(a)
listeDepartements = []
for un in a :
    deux = un[:2]
    listeDepartements.append(deux)

oups = []
for un in listeDepartements :
    if un in liste11 :
        oups.append('11')
    elif un in liste24 : 
        oups.append('24')
    elif un in liste27 :
        oups.append('27')
    elif un in liste28 :
        oups.append('28')
    elif un in liste32 :
        oups.append('32')
    elif un in liste44 :
        oups.append('44')
    elif un in liste52 :
        oups.append('52')
    elif un in liste53 :
        oups.append('53')
    elif un in liste75 :
        oups.append('75')
    elif un in liste76 :
        oups.append('76')
    elif un in liste84 :
        oups.append('84')
    elif un in liste93 :
        oups.append('93')
    elif un in liste94 :
        oups.append('94')
    else :
        oups.append('')

data2['cp2'] = oups


###########################                nb stage              ##################################

listeregion = ['11','24','27','28','32','44','52','53','75','76','84','93','94']
nbstage = [oups.count('11'),oups.count('24'),oups.count('27'),oups.count('28'),oups.count('32'),oups.count('44'),oups.count('52'),oups.count('53'),oups.count('75'),oups.count('76'),oups.count('84'),oups.count('93'),oups.count('94')]

dfcarte = pd.DataFrame({
    "Region" : listeregion,
    "Unite" : nbstage
    }) 


pret2 = []
for a in range (0,len(listeregion)) :
    dic = { "nbstage" : nbstage[a]}
    pret2.append(dic)

for aaa in range(len(pret2)) :
    region["features"][aaa]["properties"].update(pret2[aaa])

#########################                 top structure            ######################################

listeStruc = []
for r in listeregion :
    if r in oups :
        dataframe = garderValeur(data2, 'cp2', r)
        top = Top(dataframe,'denom_social','Exercice',1)
        toptop = top["nom_entreprise"]
        for unun in toptop :
            listeStruc.append(unun)
    else :
        listeStruc.append("Pas de donnée")

pret2 = []
for az in range (0,len(listeregion)) :
    dic2 = { "topstructure" : listeStruc[az]}
    pret2.append(dic2)

for aa2 in range(len(pret2)) :
    region["features"][aa2]["properties"].update(pret2[aa2])
    
    
#########################          nombre de structure d'acceuil        ####################################

nbStruc = []
for rr in listeregion :
    if rr in oups :
        dataframe = garderValeur(data2, 'cp2', rr)
        liste = dataframe['denom_social']
        listev2 = []
        for ishishish in liste :
            listev2.append(ishishish)
        listev3 = np.unique(listev2)
        shesh = len(listev3)
        nbStruc.append(shesh)
    else :
        nbStruc.append("0")

pret3 = []
for azz in range (0,len(listeregion)) :
    dic3 = { "nbstructure" : nbStruc[azz]}
    pret3.append(dic3)

for aa3 in range(len(pret3)) :
    region["features"][aa3]["properties"].update(pret3[aa3])


#################################             carte              ################################

regionmap = folium.Map(location = [48, 2],zoom_start=5,min_zoom=5)

folium.Choropleth(
    geo_data = region,
    data = dfcarte,
    name="choropleth",
    columns = ["Region","Unite"],
    key_on="feature.properties.code",
    color = "blue",
    fill_color='YlOrRd',
    legend_name='Nombre de stages',
    fill_opacity=0.6,
    line_opacity=0.5,
).add_to(regionmap)

style_function = lambda x: {
        "color": "#FFFFFF",
        "fillOpacity": 0,
        "weight": 0.1,
    }

highlight_function = lambda x: {
    "fillColor": "#000000", #couleur tout
    "color": "#000000",   #couleur des bords
    "fillOpacity": 0.75,
    "weight": 0.3,
}



add_data_GeoJson_Region(regionmap)

folium.LayerControl().add_to(regionmap)


regionmap.save("html\\/region.html")




commune = json.load(open("./carte/communes.geojson"))
merge = json.load(open("./carte/communecp.json"))
data = pd.read_csv('Base_AREXIS.csv', sep=';')
listeDep = [16,17,86,79,33,24,19,23,24,40,47,64,87]
merge2 = []

for uneCommune in merge:
    if round(uneCommune['Code_postal']/1000,0) in listeDep:
        merge2.append(uneCommune)

merge=merge2
listeCodePostal = []
b = []
for i in merge :
    listeCodePostal.append(i['Code_postal'])
    b.append(i['Code_commune_INSEE'])

acom = []
for i in range(len(commune["features"])):
    acom.append((commune["features"][i]["properties"]["code"]))

aacom = [0] * len(acom)


compteur = 0
for i in acom :
    for ii in b :
        if str(i) == str(ii) :
            ish = b.index(ii)
            aacom[compteur] = str(listeCodePostal[ish])
    compteur += 1
  
    
pret = []
for a in range(len(acom)) :
    dic = { "codepostal" : aacom[a]}
    pret.append(dic)

for aa in range(len(pret)) :
    commune["features"][aa]["properties"].update(pret[aa])
    
    
    #################################################################################################


df = creerDataFrame(data,"cp_service")

a1 = aacom
a2 = [0] * (len(a1))

nbstage = df["Nombre de stages"]
nompays = df["Colonne"]
b2 = []
b1 = []

###########################                nb stage              ##################################

for unStage in nbstage :
    b2.append(unStage)

for ishh in nompays :
    b1.append(ishh)
    
compteur = 0
compteur2 = 0

for aaa in a1 : 
    for bbb in b1 :
        if str(aaa) == str(bbb) :
            a2[compteur] = b2[compteur2]
        compteur2 += 1
    compteur +=1
    compteur2 = 0

dffifi = pd.DataFrame({
    "Pays" : a1,
    "Unite" : a2
    }) 



pret = []
for a in range (0,len(a1)) :
    dic = { "nbstage" : a2[a]}
    pret.append(dic)

for aa in range(len(pret)) :
    commune["features"][aa]["properties"].update(pret[aa])
    
  
#########################                 top structure            ######################################

a3 = []
for un in a1 :
    if un in b1 :
        dataframe = garderValeur(data, 'cp_service', un)
        top = Top(dataframe,'denom_social','Exercice',1)
        toptop = top["nom_entreprise"]
        for unun in toptop :
            a3.append(unun)
    else :
        a3.append("Pas de donnée")

pret2 = []
for az in range (0,len(a1)) :
    dic2 = { "topstructure" : a3[az]}
    pret2.append(dic2)

for aa2 in range(len(pret2)) :
    commune["features"][aa2]["properties"].update(pret2[aa2])

 
#########################          nombre de structure d'acceuil        ####################################
a4 = []
for prout in a1 :
    if prout in b1 :
        dataframe = garderValeur(data, 'cp_service', prout)
        liste = dataframe['denom_social']
        listev2 = []
        for undenom in liste :
            listev2.append(undenom)
        listev3 = np.unique(listev2)
        sheeesh = len(listev3)
        a4.append(sheeesh)
    else : 
        a4.append("0")

pret3 = []
for azz in range (0,len(a1)) :
    dic3 = { "nbstructure" : a4[azz]}
    pret3.append(dic3)

for aa3 in range(len(pret3)) :
    commune["features"][aa3]["properties"].update(pret3[aa3])   
  
    
  
######################       carte      #############################################################
    
communemap = folium.Map(location = [45, 1],zoom_start=6,min_zoom=6)

folium.Choropleth(
    geo_data = commune,
    data = dffifi,
    name="choropleth",
    columns = ["Pays","Unite"],
    key_on="feature.properties.codepostal",
    color = "blue",
    fill_color='YlOrRd',
    legend_name='Nombre de stages',
    fill_opacity=0.6,
    line_opacity=0.5,
).add_to(communemap)

style_function = lambda x: {
        "color": "#FFFFFF",
        "fillOpacity": 0,
        "weight": 0.1,
    }

highlight_function = lambda x: {
    "fillColor": "#000000", #couleuru tout
    "color": "#000000",   #couleur des bords
    "fillOpacity": 0.75,
    "weight": 0.3,
}


add_data_GeoJson_Commune(communemap)

folium.LayerControl().add_to(communemap)



communemap.save("html\\commune.html") 


#Creation des images pour les medailles

if len(final2)!=0:
    medailles = Top(final2,"denom_social","Exercice",3)
else:
    ar = np.array([["DONNEES MANQUANTES", 0], ["DONNEES MANQUANTES", 0], ["DONNEES MANQUANTES", 0]])
    medailles = pd.DataFrame(ar, index = ['0', '1', '2'], columns = ['nom_entreprise','Exercice'])

img = Image.open('./image/Medailles.jpg') 
  
I1 = ImageDraw.Draw(img) 
  
Place1 = medailles["nom_entreprise"][0]
Place2 = medailles["nom_entreprise"][1]
Place3 = medailles["nom_entreprise"][2]

myFont = ImageFont.truetype("Roboto-BlackItalic.ttf", 30)

I1.text((200, 100), Place1, fill=(0, 0, 0), font=myFont) 
I1.text((200, 280), Place2, fill=(0, 0, 0), font=myFont) 
I1.text((200, 460), Place3, fill=(0, 0, 0), font=myFont) 
  
img.save("./image/car2.png") 


drapeau = enleverValeur(final2,"nom_pays_court","FRANCE")



best = Top(drapeau,'nom_pays_court','Exercice',3)



dfo = best

dfo.drop(dfo[dfo['nom_entreprise'] == ''].index , inplace=True)


rajout_de_lignes = pd.DataFrame([[""]], columns=['nom_entreprise'])
dfo = pd.concat([dfo,rajout_de_lignes], ignore_index=True)
dfo = pd.concat([dfo,rajout_de_lignes], ignore_index=True)
dfo = pd.concat([dfo,rajout_de_lignes], ignore_index=True)

listePaysPodium = ["CANADA", "ETATS_UNIS","ROYAUME_UNIS","ITALIE","ESPAGNE","NORVEGE","PORTUGAL","CHINE","ALLEMAGNE","BELGIQUE","INDE","AUSTRALIE","ROUMANIE","MADAGASCAR","BLANC"]

CANADA=Image.open('./image/canada.png') 
ETATS_UNIS=Image.open('./image/ETATS_UNIS.png') 
ROYAUME_UNIS=Image.open('./image/ROYAUME_UNIS.png') 
ITALIE=Image.open('./image/italie.png') 
ESPAGNE=Image.open('./image/espagne.png') 
NORVEGE=Image.open('./image/norvege.png') 
PORTUGAL=Image.open('./image/portugal.png') 
CHINE=Image.open('./image/chine.png') 
ALLEMAGNE=Image.open('./image/allemagne.png') 
BELGIQUE=Image.open('./image/belgique.png') 
INDE= Image.open('./image/inde.png') 
AUSTRALIE= Image.open('./image/australie.png') 
ROUMANIE= Image.open('./image/roumanie.png') 
MADAGASCAR = Image.open('./image/madagascar.png') 
BLANC = Image.open('./image/Blanc.png') 

imgP = Image.open('./image/podium.jpg') 

#imgP.show()

# On redimensionne la taille de l'image du podium ainsi que des drapeaux

height = imgP.size[0] 
width = imgP.size[1]  
  
width = width + 1500
height = height + 1200

imgP = imgP.resize((width ,height))

CANADA = CANADA.resize((480 ,437))
ETATS_UNIS = ETATS_UNIS.resize((480 ,437))
ROYAUME_UNIS = ROYAUME_UNIS.resize((480 ,437))
ITALIE = ITALIE.resize((480 ,437))
ESPAGNE = ESPAGNE.resize((480 ,437))
NORVEGE = NORVEGE.resize((480 ,437))
PORTUGAL = PORTUGAL.resize((480 ,437))
CHINE = CHINE.resize((480 ,437))
ALLEMAGNE = ALLEMAGNE.resize((480 ,437))
BELGIQUE = BELGIQUE.resize((480 ,437))
INDE = INDE.resize((480 ,437))
AUSTRALIE = AUSTRALIE.resize((480 ,437))
ROUMANIE = ROUMANIE.resize((480 ,437))
MADAGASCAR = MADAGASCAR.resize((480 ,437))
BLANC = BLANC.resize((480 ,437))


dfo.replace({"ETATS-UNIS": "ETATS_UNIS", "ROYAUME-UNI": "ROYAUME_UNIS"}, inplace=(True))



if str(dfo["nom_entreprise"][0]) in listePaysPodium:
    pou1 = str(dfo["nom_entreprise"][0])
else:
    pou1 = "BLANC"
if str(dfo["nom_entreprise"][1]) in listePaysPodium:
    pou2 = str(dfo["nom_entreprise"][1])
else:
    pou2 = "BLANC"
if str(dfo["nom_entreprise"][2]) in listePaysPodium:
    pou3 = str(dfo["nom_entreprise"][2])
else:
    pou3 = "BLANC"

position1 = pou1
position2 = pou2
position3 = pou3


for podiumL in listePaysPodium:
    if position2 in listePaysPodium:
        if position2 == podiumL:
            position2=Image.open("./image/" + str(position2) + ".png") 
            position2 = position2.resize((480 ,437))
            imgP.paste(position2, (180,630))
    # else:
    #     imgP.text((0, 0), "", fill=(0, 0, 0), font=myFont) 
            
    if position1 in listePaysPodium:
        if position1 == podiumL:
            position1=Image.open("./image/" + str(position1) + ".png") 
            position1 = position1.resize((480 ,437))
            imgP.paste(position1, (730,330))
        # else:
        #       imgP.text((0, 0), "", fill=(0, 0, 0), font=myFont) 
           
   
    if position3 in listePaysPodium:
        if position3 == podiumL:
            position3=Image.open("./image/" + str(position3) + ".png") 
            position3 = position3.resize((480 ,437))
            imgP.paste(position3, (1270,800))
        # else:
        #     imgP.text((0, 0), "", fill=(0, 0, 0), font=myFont) 
            
    
        

# imgP.paste(position2, (180,300))
# imgP.paste(position1, (730,100))
# imgP.paste(position3, (1350,400))

#imgP.show() 


imgP.save("./image/car3.png")