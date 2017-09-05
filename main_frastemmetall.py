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
itterations=100

#############################################
# SKRIV INN NAVN PÅ UTFIL:
#############################################
filen_ut='uttest2'



#############################################
# Evt endre std:
#############################################
std=np.array([1.,2,1.2,1.4,1.9,1.5,2.1,2.7,2.5,1.1])
#############################################
# IKKE REDIGER:
#############################################

print('Laster inn data fra:',filen)
print('Skriver ut data til filer som begynner med:',filen_ut)

pct_fylker, st_tall_f,partier,fylker,hele_l=import_data(filen)
its=1
ant_dirm_fylker=np.array([9,17,19,7,7,9,7,6,4,6,14,16,4,9,10,5,9,6,5])-1
# generate st. dev matrix
std_f=np.zeros([19,10])
for i in np.arange(19):
	std_f[i,:]=std

ind_mdg=partier.index("MDG")
hele_l=np.asarray(hele_l).astype(np.float)

utjm,ordr,utjm_r,ordr_r, mand_dir_r,mand_dir_its=utjevning(pct_fylker,std_f,st_tall_f,ant_dirm_fylker,its)#,lnd_pct=hele_l)
gj=np.sum(utjm,axis=2)
sum_tot=np.sum(utjm,axis=0)
ab0=np.nansum(sum_tot/sum_tot,axis=1)
print(ab0)
for i in np.arange(19):
	print('%18s'%fylker[i], gj[i,:])

for i in np.arange(19):
	print('dir: %20s'%fylker[i], mand_dir_r[i,:])
for i in np.arange(19):
	print('%20s'%fylker[i], utjm_r[i,:])
print(np.sum(utjm_r, axis=0))
print(np.sum(mand_dir_r,axis=0))

print_to_file(filen_ut,pct_fylker, st_tall_f, mand_dir_its, utjm, ordr, utjm_r, mand_dir_r, ordr, partier, fylker)
