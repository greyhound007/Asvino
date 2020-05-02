from collections import OrderedDict 


def breast_factor_score(factors):
    score=1

    breast_factors = OrderedDict([
    ('family_history',{'1d50+':1.8,'1d50-':3.3,'2d':1.5,'2+1d':3.6,'no':1} ),       #no,yes 
    ('age', {'-30':.44,'30-40':1.47,'40-50':2.38,'50-60':3.56,'60+':3.82}),
    ('menarche_age',  {'-12':1.21, '12-13':1.1, '14+':1}),
    ('age_of_first_birth',  {'-':3.76,'-20':1, '20-24':1.63, '25-29':2.61, '30-34':2.53,'35+':4.12}),
    ('mht',  {'never/former':1, 'current e-type':1.1, 'current other/unknown type (including combined type)':1.3}), #menopause hormone replacement
    ('alcohol',  {'0':.96, '1':1.02, '2':1.04, '2+':1.2}), #alcohol intake in grams/day
    ('age_of_menopause',  {'-':1, '-55':1, '55+':1.5}),
    ('height', {'-156.4':1, '156.4-160':1.37, '160-163.4':1.34, '163.4-167':1.43, '167+':1.27}), #in cms
    ('gene_type',{"no":1,"40+":200,"40-":15,}),
    ('radiation_exposure',{'Repeated fluoroscopy':1.6,'Radiation therapy for Hodgkin disease':5.2,'no':1})
    ])
    
  

    #print(breast_factors)
    for factor in factors:
        
        score = score* breast_factors[factor][factors[factor]]
    return score


