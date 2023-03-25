import csv
import glob
import numpy as np

def Average250(csvreader,Numlin):#Calcute Average
    Avg=0
    Sum=0                   
    for row in csvreader:
        Numlin+=1
        Data.append(row)
        if Numlin <251:
            Sum+=float(row[0])
    Avg=Sum/250 #Average value
    return Avg

def Answer(TCE,TCEAvg,Bk,BKavg): #Calcute TCE results
    A1=0
    i=0
    Plus=0
    Final=0
    FinalSum=0
    for Num in TCE:
        A1=-np.log((float(Bk[i][0])-BKavg)/(float(Num)-TCEAvg))
        if i>0:
            Plus+=A1
            Final=Plus/2
        Plus=A1
        if np.isnan(Final)==False and i>1999 and i<9001:
            FinalSum+=Final
        i+=1
    return FinalSum

# Find all csv files in folder
extension = 'csv'
csvlist = glob.glob('*.{}'.format(extension))

#Combine all csv into a file 
Bk=[]
TCEAvg=[]
TCElist=[]
Numlin=0
Final=0
Docs=int(input ("The number of documents you want to average:"))
#Docs=2
for i in csvlist:
    with open(i, 'r') as file:
        Data=[]
        csvreader = csv.reader(file)
        if i=="bk.csv":  #Read background
            BKavg=Average250(csvreader,Numlin)
            Bk=Data
            print("Average of background : "+str(BKavg))
        else:
            if Numlin%10000==0:
                Numlin=0
            TCEAvg.append(Average250(csvreader,Numlin))                
            TCElist.append(Data)

LineAvgs=int(len(TCElist)/Docs)
if LineAvgs%2==1:
    LineAvgs+=1
TCESum=np.zeros(10000)
s=(LineAvgs,10000)
TCETol=np.zeros(s)
TCEDocAvg=np.zeros(LineAvgs)
m=0
n=0
for i in range(len(TCElist)):
    if n<Docs:
        for j in range(len(TCElist[0])):
            TCESum[j]+=float(TCElist[i][j][0])
        TCEDocAvg[m]+=TCEAvg[i]
        n+=1
    else:
        TCETol[m]=TCESum/Docs
        TCEDocAvg[m]=TCEDocAvg[m]/Docs
        TCESum=np.zeros(10000)
        m+=1
        for j in range(len(TCElist[0])):
            TCESum[j]+=float(TCElist[i][j][0])
        TCEDocAvg[m]+=TCEAvg[i]        
        n=1
if n==1:
    TCETol[m]=TCESum 
if n==2:
    TCETol[m]=TCESum/Docs
    TCEDocAvg[m]=TCEDocAvg[m]/Docs
file=open("answer.txt", "w")

for i in range(LineAvgs):
    Final=Answer(TCETol[i][:],TCEDocAvg[i],Bk,BKavg)   
    file.writelines(str(Final)+'\n')
file.close
input()