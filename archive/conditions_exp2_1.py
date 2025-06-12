

# Unique frequencies: c(60,70,82,96,112,132,154,180)
# Corresponding amplitudes: c(1.8504290,1.7169685,1.5297598,1.3364225,1.1252199,0.9135997,0.7058705,0.5512779,0.4983731,0.6439145,1.1297519)

unique_conditions_practice = [
{'ST1_1':[82,132,82]},
{'ST1_4':[112,70,112]},
{'ST2_1':[82,132,132]},
{'ST2_6':[154,96,96]},
{'DT1_4':[112,70,132]},
{'DT2_5':[96,154,180]},
{'DT2_2':[132,82,70]},
{'DT2_3':[70,112,132]}
]

unique_conditions_test = [
{'ST1_1':[82,132,82]},{'ST1_2':[132,82,132]},{'ST1_3':[70,112,70]},
{'ST1_4':[112,70,112]},{'ST1_5':[96,154,96]},{'ST1_6':[154,96,154]},

{'ST2_1':[82,132,132]},{'ST2_2':[132,82,82]},{'ST2_3':[70,112,112]},
{'ST2_4':[112,70,70]},{'ST2_5':[96,154,154]},{'ST2_6':[154,96,96]},

{'DT1_1':[82,132,70]},{'DT1_2':[132,82,154]},{'DT1_3':[70,112,60]},
{'DT1_4':[112,70,132]},{'DT1_5':[96,154,82]},{'DT1_6':[154,96,180]},

{'DT2_1':[82,132,154]},{'DT2_2':[132,82,70]},{'DT2_3':[70,112,132]},
{'DT2_4':[112,70,60]},{'DT2_5':[96,154,180]},{'DT2_6':[154,96,82]}
]

ordered_Hz = ['60','70','82','96','112','132','154','180']

trial_template = {
    'condition':0,
    'Same_or_Diff':0,
    'seqPos':0,
    'T1_hz':0,
    'T2_hz':0,
    'T3_hz':0, 
    'resp_T':0
}

def dict_maker(unique_conditions,nRep):
    conditions =[]
    resp_T_list = [1,2,3] 
    for resp_T in resp_T_list:
        for rep_x in range(nRep):
            for x in unique_conditions:
                x_condi_templ = trial_template.copy()
                x_condi_name = list(x)[0]
                S_or_D = x_condi_name[0]
                S_or_D = "Same" if S_or_D=="S" else "Different"
                seqPos = 1 if x_condi_name[2]=="1" else 2
                
                T1_hz = x[x_condi_name][0]
                T1_id = ordered_Hz.index(str(T1_hz))
                T2_hz = x[x_condi_name][1]
                T2_id = ordered_Hz.index(str(T2_hz))
                T3_hz = x[x_condi_name][2]
                T3_id = ordered_Hz.index(str(T3_hz))

                templ_update = {
                        'condition':x_condi_name, 'Same_or_Diff':S_or_D,'seqPos':seqPos,
                        'T1_hz':T1_hz,'T2_hz':T2_hz, 'T3_hz':T3_hz, 'resp_T':resp_T
                        }
                x_condi_templ.update(templ_update)
                conditions.append(x_condi_templ)
    return conditions

conditions_practice = dict_maker(unique_conditions=unique_conditions_practice,nRep=2)
conditions_test = dict_maker(unique_conditions=unique_conditions_test,nRep=5)

print(len(conditions_practice))
print(len(conditions_test))

