# main: importer stemmetall, opp til 4% beregn fordeling, beregn perturberte mandater
from import_data import import_data_sttall, print_to_file, import_data
from utjevning import *

############################################
# SKRIV INN NAVN PÅ FIL FOR Å LESE RESULTATER:
#############################################
filen='Fylkesfordelinger4.csv'

#############################################
# SKRIV INN ANTALL ITTERASJONER:
#############################################
its=10

#############################################
# SKRIV INN NAVN PÅ UTFIL:
#############################################
filen_ut='uttest2'


#############################################
# JUSTER PROSENT MED ØVERSTE LINJE:
#############################################
just_pct=True # True eller False: hvis True justerer den pct med øverste linje
#############################################
# Evt endre std:
#############################################
std=np.array([1.,2,1.2,1.4,1.9,1.5,2.1,2.7,2.5,1.1])
#############################################
# IKKE REDIGER:
#############################################

print('----------------------------------------------------------')
print('Laster inn data fra:',filen)
print('Skriver ut data til filer som begynner med:',filen_ut)
print('----------------------------------------------------------')
print('Kjører ',its,' itterasjoner')
pct_fylker, st_tall_f,partier,fylker,hele_l=import_data(filen)
print('----------------------------------------------------------')
print('Partier:',partier)

ant_dirm_fylker=np.array([9,17,19,7,7,9,7,6,4,6,14,16,4,9,10,5,9,6,5])-1
# generate st. dev matrix
ant_fylk=len(fylker)
ant_part=len(partier)
std_f=np.zeros([ant_fylk,ant_part])
for i in np.arange(ant_fylk):
	std_f[i,:]=std

ind_mdg=partier.index("MDG")
hele_l=np.asarray(hele_l).astype(np.float)



################### JUSTERER MED LANDSGJSNITT:
if (just_pct):
	pct_fylker_ny=np.copy(pct_fylker)
	st_tall_lands_dist=np.zeros(pct_fylker.shape)
	for i in np.arange(ant_fylk):
		st_tall_lands_dist[i,:]=pct_fylker[i,:]*st_tall_f[i]/100
	
	
	pct_land_gammel=np.sum(st_tall_lands_dist,axis=0)/np.sum(st_tall_lands_dist)*100
	st_tall_lands_dist_ny=np.zeros(st_tall_lands_dist.shape)
	for i in np.arange(ant_part):
		st_tall_lands_dist_ny[:,i]=st_tall_lands_dist[:,i]*hele_l[i]/pct_land_gammel[i]
	pct_test=np.zeros(hele_l.shape)
	for i in np.arange(ant_part):
		pct_test[i]=np.sum(st_tall_lands_dist_ny[:,i])/np.sum(st_tall_lands_dist_ny)*100
	
	for i in np.arange(ant_fylk):
		pct_fylker_ny[i,:]=st_tall_lands_dist_ny[i,:]/np.sum(st_tall_lands_dist_ny[i,:])

	"""
	hele_landet_test=np.zeros(pct_fylker.shape)
	for i in np.arange(len(pct_fylker[:,0])):
		hele_landet_test[i,:]=pct_fylker_ny[i,:]*st_tall_f[i]/100

	pct_land_test=np.sum(hele_landet_test,axis=0)/np.sum(hele_landet_test)*100
	"""
	
	pct_fylker=pct_fylker_ny
	


	print(pct_test)
	print(hele_l)
	print(pct_land_gammel)



utjm,ordr,utjm_r,ordr_r, mand_dir_r,mand_dir_its=utjevning(pct_fylker,std_f,st_tall_f,ant_dirm_fylker,its)#,lnd_pct=hele_l)


st_tall_pr_fylke=np.zeros(pct_fylker.shape)


gj=np.mean(utjm,axis=2)

sum_tot=np.sum(utjm,axis=0)
sum_tot_mdg=sum_tot[ind_mdg,:]
ab0=np.nansum(sum_tot/sum_tot,axis=1)

utjmMDG4=utjm[:,:,sum_tot_mdg>0]
gj_MDG4=np.mean(utjmMDG4,axis=2)
print('Antall ganger de forskjellige partiene får utjevningsmandat:')
print(ab0)
print('Gjennomsnitt utjevningsmandater mdg over 4:')
for i in np.arange(ant_fylk):
	print('%18s'%fylker[i], np.rint(100*gj_MDG4[i,:]))#,decimals=1))

print('Gjennomsnitt utjevningsmandater forskjell:')
for i in np.arange(ant_fylk):
	print('%18s'%fylker[i], np.rint(100*(gj_MDG4[i,:]-gj[i,:])))#,decimals=1))
print('DIREKTEMANDATER FOR UPERTURBERT:')
for i in np.arange(ant_fylk):
	print('dir: %20s'%fylker[i], mand_dir_r[i,:])
print('UTJEVNINGSMANDATER FOR UPERTURBERT:')
for i in np.arange(ant_fylk):
	print('%20s'%fylker[i], utjm_r[i,:])
print('Utjevningsmandater UPERTURBERT:')
print(np.sum(utjm_r, axis=0))
print('Direktemandat UPERTURBERT')
print(np.sum(mand_dir_r,axis=0))


print_to_file(filen_ut,pct_fylker, st_tall_f, mand_dir_its, utjm, ordr, utjm_r, mand_dir_r, ordr_r, partier, fylker)
