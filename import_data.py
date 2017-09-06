from utjevning import *


#######################################################################################
# Takes non binary csv file. Save file with semicolon dilimiter ; and put all relevant#
# files in rootdir.                                                                   #
# result is output into file with same name except with "_sorted.csv" appended        #
#######################################################################################
import os
import sys
import io
import re
import csv
from datetime import datetime
#reload(sys)
#sys.setdefaultencoding("latin-1")
ant_fylk=19
# Change to relevant folder
rootdir ='/home/sarambl/MDG/rodeRedigering_dørbank2017/files/' #directory to run
def initCVSfile(name,firstLine):
    with open(name,'w') as csvfile:
        filewriter=csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(firstLine)

def appendLineCVSfile(name,line):
    with open(name,'a') as csvfile:
        filewriter=csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(line)

def import_data(filename):
	#with(filename,'r') as csvfile:
	lol = list(csv.reader(io.open(filename, 'r'), delimiter=';'))
	#print (lol[1])
	nr_c=len(lol[0][0].split(','))
	data=np.zeros([19,nr_c-2])
	#data=lol[:][0].split(',')
	#lol_s=lol.split(',')
	first=lol[1][0]
	partier=lol[0][0].split(',')[1:-1]
	#print(partier)
	hele_l=lol[1][0].split(',')[1:-1]
	#print(hele_l)
	fylker=[]
	st_tall=np.zeros([19,1])
	for i in np.arange(19):
		line=lol[2+i][0].split(',')
		data[i,:]=line[1:-1]
		fylker.append(line[0])
		st_tall[i]=line[-1]
	#print(partier)

	#print(data)
	#print(fylker)
	data=np.asarray(data)
	st_tall=np.squeeze(np.asarray(st_tall)	)
	#print(st_tall.shape)
	return data,st_tall,partier, fylker, hele_l





def import_data_sttall(filename):
	lol = list(csv.reader(io.open(filename, 'r'), delimiter=';'))
	nr_c=len(lol[0][0].split(','))
	print(nr_c)
	st_tall=np.zeros([19,nr_c-1])
	first=lol[1][0]
	partier=lol[0][0].split(',')[1::]
	hele_l=lol[1][0].split(',')[1::]
	fylker=[]
	st_tall_fylk=np.zeros([19,1])
	for i in np.arange(19):
		line=lol[1+i][0].split(',')
		st_tall[i,:]=line[1::]
		fylker.append(line[0])
		st_tall_fylk=np.sum(st_tall[i,:])

	st_tall=np.asarray(st_tall)
	st_tall_fylk=np.asarray(st_tall)
	line=lol[21][0].split(',')
	st_pct=np.asarray(line[1::])
	return st_tall,st_tall_fylk, partier, fylker, st_pct 






def import_forhtall(filename):
	lol = list(csv.reader(io.open(filename, 'r'), delimiter=';'))
	nr_1=lol[0][0].split(',')
	print('MDGs oppslutning nasjonalt: ', nr_1[2])
	mdg_f=np.zeros([ant_fylk,1])
	for i in np.arange(ant_fylk):
		mdg_f[i]=lol[i+1][0].split(',')[2]
	return mdg_f

def generer_opps_rel(filename1,filename_rel):
	mdg_f=import_forhtall(filename_rel)
	pct_fylker, st_tall_f,partier,fylker=import_data(filename1)
	pct_fylker[:,1]=np.squeeze(mdg_f)
	return pct_fylker, st_tall_f, partier, fylker

def print_to_file(filename,pct, st_tall, ant_dirm_f, utjm_f, ordr, utj_rett, ant_dirm_rett, ordr_rett, partier, fylker):
	firstLine=[' ']+partier
	filen_rett_utj=filename+'_rett_utj.csv'
	filen_rett_dir=filename+'_rett_dir.csv'
	filen_its_utj=filename+'_its_utj.csv'
	filen_its_dir=filename+'_its_dir.csv'
	filen_its_ord=filename+'_its_ordr.csv'
	filen_rett_ord=filename+'_rett_ordr.csv'
	filen_its_ut_gj=filename+'_its_ut_gj.csv'
	initCVSfile(filen_rett_utj,firstLine)
	initCVSfile(filen_rett_dir,firstLine)
	initCVSfile(filen_its_utj,firstLine)
	initCVSfile(filen_its_dir,firstLine)
	initCVSfile(filen_its_ord,'')
	initCVSfile(filen_rett_ord,'')
	ant_its=utjm_f.shape[2]
	ant_part=utjm_f.shape[1]
	ant_fylk=utjm_f.shape[0]

	#Regner ut gjennomsnitt:
	utjm_f_gj=np.mean(utjm_f,axis=2)
	initCVSfile(filen_its_ut_gj,firstLine)
	
	fy_ordr=(np.asarray(ordr_rett[:,0]))
	par_ordr=(np.asarray(ordr_rett[:,1]))
	appendLineCVSfile(filen_rett_ord,[fylker[int(i)] for i in fy_ordr])
	appendLineCVSfile(filen_rett_ord,[partier[int(i)] for i in par_ordr])
	for f in np.arange(ant_fylk):
		line1=[fylker[f]]+utj_rett[f,:].tolist()
		line2=[fylker[f]]+ant_dirm_rett[f,:].tolist()
		line3=[fylker[f]]+utjm_f_gj[f,:].tolist()
		appendLineCVSfile(filen_rett_utj, line1)
		appendLineCVSfile(filen_rett_dir,line2)
		appendLineCVSfile(filen_its_ut_gj, line3)
		# rekkefolge
		
	for it in np.arange(ant_its):
		#print(ordr)
		ordr_it=(np.asarray(ordr[:,0,it]))
		#print(ordr_it)
		appendLineCVSfile(filen_its_ord,[fylker[int(i)] for i in ordr_it])
		ordr_it=np.asarray(ordr[:,1,it])
		appendLineCVSfile(filen_its_ord,[partier[int(i)] for i in ordr_it])
		#appendLineCVSfile(filen_ord,partier[ordr_it])
		appendLineCVSfile(filen_its_ord,[' '])
		for f in np.arange(ant_fylk):
			
			line1=[fylker[f]]+utjm_f[f,:,it].tolist()
			line2=[fylker[f]]+ant_dirm_f[f,:,it].tolist()
			appendLineCVSfile(filen_its_utj,line1)
			appendLineCVSfile(filen_its_dir,line2)
		
		appendLineCVSfile(filen_its_dir,[' '])
		appendLineCVSfile(filen_its_utj,[' '])
	
	
	
"""
mdg_f=import_forhtall('relativ_oppslutning.csv')
file_in='/home/sarambl/MDG/mandatting/Fylkesfordelinger3.csv'
file_rel='/home/sarambl/MDG/mandatting/relativ_oppslutning.csv'
pct_fylker, st_tall_f,partier,fylker=generer_opps_rel(file_in,file_rel)
#print(mdg_f)
#quit()

#pct_fylker, st_tall_f,partier,fylker=import_data('/home/sarambl/MDG/mandatting/Fylkesfordelinger.csv')
its=100
ant_dirm_fylker=np.array([9,17,19,7,7,9,7,6,4,6,14,16,4,9,10,5,9,6,5])-1
std=np.array([1.,2,1.2,1.4,1.9,1.5,2.1,2.7,2.5])
std_f=np.zeros([19,9])
for i in np.arange(19):
	std_f[i,:]=std
utjm,ordr,utjm_r,ordr_r, mand_dir_r,mand_dir_its=utjevning(pct_fylker,std_f,st_tall_f,ant_dirm_fylker,its)
gj=np.sum(utjm,axis=2)
sum_tot=np.sum(utjm,axis=0)
ab0=np.nansum(sum_tot/sum_tot,axis=1)
print(ab0)
for i in np.arange(19):
	print(fylker[i], gj[i,1])
#print(np.mean(utjm,axis=2))
print('------------------------------------------------------------------------------')
print(utjm_r)
print(ordr_r)
filename='uttest'

print_to_file(filename,pct_fylker, st_tall_f, mand_dir_its, utjm, ordr, utjm_r, mand_dir_r, ordr, partier, fylker)
"""
