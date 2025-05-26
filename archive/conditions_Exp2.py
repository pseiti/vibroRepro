

# Unique frequencies: c(60,70,82,96,112,132,154,180)
# Corresponding amplitudes: c(1.8504290,1.7169685,1.5297598,1.3364225,1.1252199,0.9135997,0.7058705,0.5512779,0.4983731,0.6439145,1.1297519)


# conditions_practice = [
# {'ST1_high_1':[113,170,113]},{'ST1_high_2':[170,113,170]},{'ST1_high_3':[113,75,113]},{'ST1_high_5':[170,255,170]},
# {'ST2_high_1':[113,170,170]},{'ST2_high_2':[170,113,113]},{'ST2_high_3':[113,75,75]},{'ST2_high_5':[170,255,255]},
# {'DT1_high_1':[113,170,92]},{'DT1_high_2':[170,113,208]},{'DT1_high_3':[113,75,138]},{'DT1_high_5':[170,255,138]},
# {'DT2_high_1':[113,170,208]},{'DT2_high_2':[170,113,92]},{'DT2_high_3':[113,75,61]},{'DT2_high_5':[170,255,313]}]

unique_conditions_practice = [
{'ST1_high_1':[82,112,82]},{'ST1_high_4':[96,70,96]},
{'ST2_high_2':[112,82,82]},{'ST2_high_5':[96,132,132]},
{'DT1_high_3':[70,96,60]},{'DT1_high_6':[132,96,154]},
{'DT2_high_1':[82,112,132]},{'DT2_high_6':[132,96,82]},
{'ST1_low_1':[82,132,82]},{'ST1_low_4':[112,70,112]},
{'ST2_low_2':[132,82,82]},{'ST2_low_5':[96,154,154]},
{'DT1_low_3':[70,112,60]},{'DT1_low_6':[154,96,180]},
{'DT2_low_1':[82,132,154]},{'DT2_low_6':[154,96,82]}]

#unique_conditions_practice = [{'ST1_low_1':[82,112,82]},{'DT1_low_1':[70,112,60]}]


# unique_conditions_test = [
# {'DB_high_1':[60,82,70]},
# {'DB_high_2':[82,60,70]},
# {'DB_high_3':[70,96,82]},
# {'DB_high_4':[96,70,82]},
# {'DB_high_5':[82,112,96]},
# {'DB_high_6':[112,82,96]},
# {'DB_high_7':[96,132,112]},
# {'DB_high_8':[132,96,112]},
# {'DB_high_9':[112,154,132]},
# {'DB_high_10':[154,112,132]},
# {'DB_high_11':[132,180,154]},
# {'DB_high_12':[180,132,154]}
# ]


unique_conditions_test = [
{'DB_high_1_ss':[60,82,70]},{'DB_high_1_ll':[60,82,70]},
{'DB_high_1_sl':[60,82,70]},{'DB_high_1_ls':[60,82,70]},

{'DB_high_2_ss':[82,60,70]},{'DB_high_2_ll':[82,60,70]},
{'DB_high_2_sl':[82,60,70]},{'DB_high_2_ls':[82,60,70]},

{'DB_high_3_ss':[70,96,82]},{'DB_high_3_ll':[70,96,82]},
{'DB_high_3_sl':[70,96,82]},{'DB_high_3_ls':[70,96,82]},

# {'DB_high_4_ss':[96,70,82]},{'DB_high_4_ll':[96,70,82]},
# {'DB_high_4_sl':[96,70,82]},{'DB_high_4:ls':[96,70,82]},

# {'DB_high_5_ss':[82,112,96]},{'DB_high_5_ll':[82,112,96]},
# {'DB_high_5_sl':[82,112,96]},{'DB_high_5_ls':[82,112,96]},

# {'DB_high_6_ss':[112,82,96]},{'DB_high_6_ll':[112,82,96]},
# {'DB_high_6_sl':[112,82,96]},{'DB_high_6_ls':[112,82,96]},

# {'DB_high_7_ss':[96,132,112]},{'DB_high_7_ll':[96,132,112]},
# {'DB_high_7_sl':[96,132,112]},{'DB_high_7_ls':[96,132,112]},

# {'DB_high_8_ss':[132,96,112]},{'DB_high_8_ll':[132,96,112]},
# {'DB_high_8_sl':[132,96,112]},{'DB_high_8_ls':[132,96,112]},

# {'DB_high_9_ss':[112,154,132]},{'DB_high_9_ll':[112,154,132]},
# {'DB_high_9_sl':[112,154,132]},{'DB_high_9_ls':[112,154,132]},

# {'DB_high_10_ss':[154,112,132]},{'DB_high_10_ll':[154,112,132]},
# {'DB_high_10_sl':[154,112,132]},{'DB_high_10_ls':[154,112,132]},

# {'DB_high_11_ss':[132,180,154]},{'DB_high_11_ll':[132,180,154]},
# {'DB_high_11_sl':[132,180,154]},{'DB_high_11_ls':[132,180,154]},

# {'DB_high_12_ss':[180,132,154]},{'DB_high_12_ll':[180,132,154]},
# {'DB_high_12_sl':[180,132,154]},{'DB_high_12_ls':[180,132,154]}
]



#unique_conditions_test= [{'ST1_low_1':[82,112,82]},{'DT1_low_1':[70,112,60]}]

Hz_amp_mapping = {
	'60':1.778327198,
	'70':1.608381144,
	'82':1.426248320,
	'96':1.243820967,
	'112':1.074973366,
	'132':0.923375067,
	'154':0.832925483,
	'180':0.829096604
}
ordered_Hz = list(Hz_amp_mapping)
ordered_Amps = list(Hz_amp_mapping.values())
trial_template = {
	'condition':0,
	'ITS':0,
    'ITI1':0,
    'ITI2':0,
	'T1_hz':0,
	'T1_amp':0,
	'T2_hz':0,
	'T2_amp':0,
	'P_hz':0,
	'P_amp':0
}

def dict_maker(unique_conditions,nRep):
    conditions =[]
    for rep_x in range(nRep):
        for x in unique_conditions:
            x_condi_templ = trial_template.copy()
            x_condi_name = list(x)[0]
            ITS = "high" if x_condi_name[3]=="h" else "low"
            
            if x_condi_name[-2:]=="ss":
                ITI1 = 2500 
                ITI2 = 4000
            elif x_condi_name[-2:]=="ll":
                ITI1 = 3000
                ITI2 = 5000
            elif x_condi_name[-2:]=="sl":
                ITI1 = 2500
                ITI2 = 4500
            else:
                ITI1 = 3000
                ITI2 = 4500
            
            T1_hz = x[x_condi_name][0]
            T1_id = ordered_Hz.index(str(T1_hz))
            T1_amp = ordered_Amps[T1_id]
            T2_hz = x[x_condi_name][1]
            T2_id = ordered_Hz.index(str(T2_hz))
            T2_amp = ordered_Amps[T2_id]
            P_hz = x[x_condi_name][2]
            P_id = ordered_Hz.index(str(P_hz))
            P_amp = ordered_Amps[P_id]
            templ_update = {
                    'condition':x_condi_name,'ITS':ITS, 'ITI1':ITI1, 
                    'ITI2':ITI2,'T1_hz':T1_hz,'T1_amp':T1_amp,'T2_hz':T2_hz,
                    'T2_amp':T2_amp,'P_hz':P_hz,'P_amp':P_amp
                    }
            x_condi_templ.update(templ_update)
            conditions.append(x_condi_templ)
    return conditions

conditions_practice = dict_maker(unique_conditions=unique_conditions_practice,nRep=1)#2
conditions_test = dict_maker(unique_conditions=unique_conditions_test,nRep=1)#10

#print(conditions_test)

#print(conditions_test[0])




