import numpy as np
from mandatberegning import *
import random as rd

def utjevning(pct_fylker,std_fylker,stemmetall_fylker,ant_dirm_fylker,its,lnd_pct=[]):
	# henter ut nyttig info:
	ant_fylk=len(pct_fylker[:,1])
	ant_part=len(pct_fylker[1,:])
	# lager arrayer
	mand_s_dir=np.zeros([ant_fylk,ant_part,its])		# direkte mandater iterasjoner
	direktemandater_rett=np.zeros([ant_fylk,ant_part])	# direkte mandater uperturbert
	sluttkvotient_fylker=np.zeros([ant_fylk,ant_part,its])	# sluttkvotient etter direktemandater
	kvotienter_dirmand_rett=np.zeros([ant_fylk,ant_part])	# sluttkvotienter etter direktemandater, uperturbert
	stemmer_fylker=np.zeros([ant_fylk,ant_part,its])	# stemmetall fylker/partier
	stemmer_fylker_rett=np.zeros([ant_fylk,ant_part])	# stemmetall fylker/partier uperturbert
	utjevningsmandater=np.zeros([ant_fylk,ant_part,its])	# utjevningsmandater perturbert
	order_utj=np.zeros([ant_fylk,2,its])  #holder rekkefølgen på utjevningsmandatene


	# Regner ut direkte mandater for rett fordeling og perturbert:
	for i in np.arange(ant_fylk):
		mand_s_dir[i,:,:],sluttkvotient_fylker[i,:,:],stemmer_fylker[i,:,:]=pert_mandatb(pct_fylker[i,:], 
							std_fylker[i,:], 
							stemmetall_fylker[i],
							ant_dirm_fylker[i], 
							its)
		# regn ut direkte mandater:
		d1,d2,d3=mandat_fra_pct_fylke(pct_fylker[i,:],stemmetall_fylker[i],ant_dirm_fylker[i])
		direktemandater_rett[i,:]=d1[:,-1]
		kvotienter_dirmand_rett[i,:]=d2[:,-1]
		stemmer_fylker_rett[i,:]=d3
	# beregner utjevning for hver itterasjon:
	for it in np.arange(its): # gjør utjevningen for hver itterasjon
		mand_fin,ordr=utj_mand_fra_fordeling(mand_s_dir[:,:,it],stemmer_fylker[:,:,it],ant_dirm_fylker)
		utjevningsmandater[:,:,it]=mand_fin
		order_utj[:,:,it]=ordr
	
	utjevningsmandater_rett,ordr_rett=utj_mand_fra_fordeling(direktemandater_rett,stemmer_fylker_rett,ant_dirm_fylker, printTV=False,lnd_pct=lnd_pct)
	# gir ut:(1) utjevningsmandater(itterasjoner), (2) rekkefølge utjevningsmandater(itterasjoner)
	# (3) utjevningsmandater (rett fordeling), (4) rekkefølge utjevningsmandater, (5) direktemandater (rett fordeling,
	# (6) direktemandater (itterasjoner)
	return utjevningsmandater,order_utj, utjevningsmandater_rett,ordr_rett, direktemandater_rett,mand_s_dir

######################################
# Metode for å regne ut utjevningsmandater fra stemmetall i alle fylkene:
# Inn: direktemandater (allerede utdelt), stemme_matrise, ant_direktemandater_pr_fylke, debugging 
######################################

def utj_mand_fra_fordeling(mand_s_dir,stemmer_fylker,ant_dirm_fylker, printTV=False,lnd_pct=[]):
	# regn ut hvor mange utjevningsmandater hvert parti skal ha:
	ant_fylk=mand_s_dir.shape[0]
	ant_part=mand_s_dir.shape[1]
	# stemmetall hele landet:
	st_tall=np.sum(stemmer_fylker, axis=0)#1.4
	# pct (for å regne ut under og over sperregrensa)
	pct=st_tall/np.sum(st_tall)*100
	#print(pct)
	if (len(lnd_pct)>0):
		pct=lnd_pct
		st_tall=lnd_pct*np.sum(st_tall)

	# Hvis et parti har under 4% skal det ikke være med videre
	st_tall[pct<4.]=0 	# Hvis et parti ikke er over 4% skal det ikke med
	utjTV=pct>=4.		# Holder på hvilke partier som skal ha utjevningsmandat
	pct_utj=st_tall/np.sum(st_tall)*100 # regner ut pct på nytt

	# Regner ut ny landsbasis fordeling:
	

	mand_dist=np.sum(mand_s_dir[:,:], axis=0) # distriktsmandatene
	mand_dist_d=np.copy(mand_dist) # for comparison

	rm=np.sum(mand_dist[pct<4.])  # Mandater fra partier under sperregrensa skal ikke deles ut
	mand_dist_d[pct<4.]=0  # Setter disse mandatene til null i mand_dist (skal ikke med som negative)
	mand,kvot,st_t=mandat_fra_pct_fylke(pct_utj,np.sum(st_tall),169-rm, div_14=False) 
	#mand_dist=np.sum(mand_s_dir[:,:], axis=0) # distriktsmandatene
	
	mand_utj_ant=mand[:,-1]-mand_dist_d  # sammenlikner distriktsmandater og "rett fordeling"
	#mand_dist[mand_utj_ant<0]=0
	if printTV:
		print('MANDATER')
		print(mand_utj_ant)
		print(mand_dist_d)
		print(mand[:,-1])

	rerun=[(mand_utj_ant[ii]<0) for ii in np.arange(len(mand_utj_ant))] #sjekker om noen partier har for mange
	while ( np.any(rerun)):
		# setter stemmetall for de partiene som har fått "for mange" mandater til 0 
		st_tall[mand_utj_ant<0]=0.
		# regner ut ny prosent for fordelingen:
		pct_utj=st_tall/np.sum(st_tall)*100
		utjTV[mand_utj_ant<0]=False
		#trekker fra mandater som er tildelt partier som har fått for mye:	
		rm=rm+np.sum(mand_dist[mand_utj_ant<0])
		mand_dist_d[mand_utj_ant<0]=0
		#print(rm)
		mand,kvot,st_t=mandat_fra_pct_fylke(pct_utj,np.sum(st_tall),169-rm,div_14=False)
		mand_utj_ant=mand[:,-1]-mand_dist_d
		if printTV:
			print('MANDATER - loop')
			print(mand_utj_ant)
			print(mand_dist)
			print(mand[:,-1])
		utjTV[mand_utj_ant<0]=False
		rerun=[(mand_utj_ant[ii]<0) for ii in np.arange(len(mand_utj_ant))]
	if printTV:
		print('----------------------*************-----------------------------------------')
		print(utjTV)
		print('----------------------*************-----------------------------------------')
		print(mand_utj_ant)

	# Regner ut kvotienter gjennmsnittlig antall stemmer per direktemandat:
	#gj_st_per_m=np.sum(stemmer_fylker[:,:],axis=1)/ant_dirm_fylker
	gj_st_per_m=np.sum(stemmer_fylker[:,:],axis=1)/ant_dirm_fylker
	# rest kvotient i per fylke:
	rest_kvot=np.zeros(stemmer_fylker.shape)
	for j in np.arange(ant_fylk):
		for k in np.arange(ant_part):
			if (mand_s_dir[j,k]==0): rest_kvot[j,k]=stemmer_fylker[j,k]
			else: rest_kvot[j,k]=stemmer_fylker[j,k]/(mand_s_dir[j,k]*2+1)
			
	## regner ut justert kvotient: Deler på gjennomsnittlig antall stemmer per direktemandat:
	just_kvot=np.zeros([ant_fylk,ant_part])
	for j in np.arange(ant_fylk):
		just_kvot[j,:]=rest_kvot[j,:]/gj_st_per_m[j]*1000
		for k in np.arange(ant_part):
			if (mand_utj_ant[k]<=0): just_kvot[j,k]=0 # hvis mandatet ikke skal med: kvotient 0
			if (pct[k]<4.): just_kvot[j,k]=0	  # hvis under 4% : kvotient 0
	
	# Klar til å beregne utjevningsmandater:
	utjevningsm_final=np.zeros([ant_fylk,ant_part])
	
	order_utj=np.zeros([ant_fylk,2])
	
	# beregner for 19 fylker:
	for j in np.arange(ant_fylk):
		# Finner index for den største kvotienten:
		max_ind=np.argmax(just_kvot) # finds the maximum
		ifylk,ipart=np.unravel_index(just_kvot.argmax(),just_kvot.shape) # finner fylke og parti
		#print(just_kvot[ifylk,ipart])
		# SJEKKER FOR FEIL:
		if (just_kvot[ifylk,ipart]==0):
			print('FEILMELDING: beregningen av mandat nr: ',j,' ga kun null som kvotient')
		# Trekker fra et mandat på det relevante partiet:
		mand_utj_ant[ipart]=mand_utj_ant[ipart]-1
		# Setter alle kvotientene i fylket lik 0 (det skal ikke deles ut flere mandater i fylket):
		just_kvot[ifylk,:]=0 # fylke tatt
		# Lagrer mandatet:
		utjevningsm_final[ifylk,ipart]+=1  # legger til et utjevningsmandat
		# Sjekker om partiet skal ha flere mandater, hvis ikke blir alle kvotientene 0
		if (mand_utj_ant[ipart]<=0): just_kvot[:,ipart]=0 # partiet skal ikke ha flere mandater
		# Lagrer rekkefølge:
		order_utj[j,0]=ifylk
		order_utj[j,1]=ipart
	return utjevningsm_final,order_utj


# Lage en variant med gitt fordeling mellom partiene. 
# dele på 1.4 første runde
# Lage et program som skriver til 
