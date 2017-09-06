import numpy as np
import random as rd
# 0-AP, 1-høyre, 2- frp,3- sv, 4-sp, 5-krf, 6-venstre, 7- MDG, 8-Rødt,9 andre
partier=np.array([ 'AP', 'høyre', '2- frp','3- sv', '4-sp', '5-krf', '6-venstre', '7- MDG', '8-Rødt','9 andre'])

def mandat_fra_pct_fylke(pct, ant_stemmer, ant_dirm,weight=[], div_14=True):
	st_tall=0.01*pct*ant_stemmer
	
	kvot=np.copy(st_tall)/1.4
	if div_14:
		kvot=st_tall/1.4
	else:
		kvot=np.copy(st_tall)
	lenp=len(pct)
	ant_dirm=int(ant_dirm)
	kvot_s=np.zeros([lenp,ant_dirm])
	mandater_s=np.zeros([lenp,ant_dirm])
	for i in np.arange(ant_dirm):
		ind_max=[j for j in np.arange(lenp) if kvot[j]==np.max(kvot)]
		if (len(ind_max)>1 and i==(ant_dirm-1)):
			print('Advarsel: siste mandatet fikk likt resultat for partier')
			print(partier[ind_max])
		ind_corr=ind_max[0]
		if (i==0):
			mandater_s[ind_corr,0]=1
		else:
			mandater_s[:,i]=mandater_s[:,i-1]
			mandater_s[ind_corr,i]+=1
		
		kvot[ind_corr]=st_tall[ind_corr]/((mandater_s[ind_corr,i])*2+1)
		kvot_s[:,i]=kvot
		
	return mandater_s,kvot_s,st_tall

def mandat_fra_stt_fylke(st_tall, ant_dirm,weight=[]):
	#st_tall=0.01*pct*ant_stemmer
	kvot=st_tall/1.4
	lenp=len(st_tall)
	ant_dirm=int(ant_dirm)
	kvot_s=np.zeros([lenp,ant_dirm])
	mandater_s=np.zeros([lenp,ant_dirm])
	for i in np.arange(ant_dirm):
		ind_max=[j for j in np.arange(lenp) if kvot[j]==np.max(kvot)]
		if (len(ind_max)>1 and i==(ant_dirm-1)):
			print('Advarsel: siste mandatet fikk likt resultat for partier')
			print(partier[ind_max])
		ind_corr=ind_max[0]
		if (i==0):
			mandater_s[ind_corr,0]=1
		else:
			mandater_s[:,i]=mandater_s[:,i-1]
			mandater_s[ind_corr,i]+=1
		
		kvot[ind_corr]=st_tall[ind_corr]/((mandater_s[ind_corr,i])*2+1)
		kvot_s[:,i]=kvot
		
	return mandater_s,kvot_s,st_tall






def mandater_fra_stemmetall(st_tall,ant_dirm):
	kvot=st_tall/1.4
	lenp=len(pct)
	kvot_s=np.zeros([lenp,ant_dirm])
	mandater_s=np.zeros([lenp,ant_dirm])
	for i in np.arange(ant_dirm):
		kvot_s[:,i]=kvot
		ind_max=[j for j in np.arange(lenp) if kvot[j]==np.max(kvot)]
		if (len(ind_max)>1 and i==(ant_dirm-1)):
			print('Advarsel: siste mandatet fikk likt resultat for partier')
			print(partier[ind_max])
		ind_corr=ind_max[0]
		if (i==0):
			mandater_s[ind_corr,0]=1
		else:
			mandater_s[:,i]=mandater_s[:,i-1]
			mandater_s[ind_corr,i]+=1
		kvot[ind_corr]=st_tall[ind_corr]/((mandater_s[ind_corr,i])*2+1)
	return mandater_s,kvot_s
	
		
def pert_mandatb(pct, std, ant_stemmer,ant_dirm, its):
	lenp=len(pct)
	mand_s=np.zeros([lenp,its])
	kvot_s=np.zeros([lenp,its])
	st_tall=np.zeros([lenp,its])
	for i in np.arange(its):
		pert_pct=rd.gauss(pct,std)
		pert_pct=pert_pct*100./sum(pert_pct)
		for k in np.arange(len(pert_pct)):
			if (pert_pct[k]<0): pert_pct[k]=0.001
		#print(pert_pct)
		mand,kvot,st_talli=mandat_fra_pct_fylke(pert_pct,ant_stemmer, ant_dirm)
		mand_s[:,i]=mand[:,-1]
		st_tall[:,i]=st_talli
		kvot_s[:,i]=kvot[:,-1]
	return mand_s,kvot_s,st_tall



pct=np.array([29.0, 	#ap
	26.6,		#høyre
	13.3,		#frp
	4.2,		#sv
	5.8,		#sp
	3.1,		#krf
	4.5,		#venstre
	3.7,		#mdg
	1.8,		#rødt
	1.4])		#andre


