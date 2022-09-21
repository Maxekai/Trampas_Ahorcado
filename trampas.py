import pandas as pd
from tkinter import *
fuera=[1,2,3,4,5,6,7,8,9,0,'.','1']
def detilde(s):
    s=str(s)
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ü", "u")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s.strip()


df=pd.read_table('CREA_total.TXT',delimiter='	',encoding = "ISO-8859-1",low_memory=False)
df=df.drop(columns='Frec.absoluta ')
df['     Orden']=df['     Orden'].apply(detilde)
df.columns=['Orden','Frecuencia']
df=df.drop(df.loc[1:100].index)
palabrasusadas=40000 #Usamos las 40000 palabras mas comunes
df=df.head(palabrasusadas) 
dataframes=[]
for i in range(3,13):
    dataframes.append(df[(df.Orden.str.len() == i)])

def checker(longitud):
    return dataframes[longitud-3]

root= Tk()
root.title('Trampa')
topframe=Frame(root)
topframe.grid(row=0,column=0)
midframe=Frame(root)
midframe.grid(row=1,column=0)
bottomframe=Frame(root)
bottomframe.grid(row=2,column=0)
resultframe=Frame(root)
resultframe.grid(row=3,column=0)

def GenerateBoxes():
    Letbox.create(Botones.wordlength)

def filtering(query):
    dff=checker(Botones.wordlength)
    dff=dff[dff['Orden'].str.match(str(query))]
    print(dff)
    resultcreation(dff['Orden'].head(150))
    

def resultcreation(series):
    for widgets in resultframe.winfo_children():
        widgets.destroy()
    listvals=series.tolist()
    for index, value in enumerate(listvals):
        Label(resultframe,text=value).grid(row=index%25,column=index//25)
    
class Buttons:
    x=IntVar()
    lengths=['3','4','5','6','7','8','9','10','11','12']
    def __init__(self):
        for index in range(len(self.lengths)):
            radiobutton=Radiobutton(topframe,text=self.lengths[index],variable=self.x,value=index,command=GenerateBoxes)
            radiobutton.grid(row=0,column=index)
    @property
    def wordlength(self):
        return self.x.get()+3


Botones=Buttons()


class LetterBoxes:
    def __init__(self):
        pass
    
    def create(self,wordlength):
        self.boxes=[]
        self.clear_frame()
        for i in range(wordlength):
            self.boxes.append(Entry(bottomframe,width=3,font=('Helvetica 20'),justify='center'))
            self.boxes[i].insert(0,'')
        for i in range(len(self.boxes)):
            self.boxes[i].grid(row=1,column=i)
        
    def clear_frame(self):
        for widgets in bottomframe.winfo_children():
            widgets.destroy()
    
    def search(self):
        query=[]
        for i in range(len(self.boxes)):
            if self.boxes[i].get() != '':
                query.append(self.boxes[i].get())
            else:
                query.append('.')
        query=','.join(query)
        query=query.replace(',','')
        print(query)
        filtering(query)
            
Letbox=LetterBoxes()
    
SearchButton=Button(midframe,text='Buscar',command=Letbox.search)
SearchButton.grid(row=0,column=0)
root.mainloop()