from collections import OrderedDict 


def breast_factor_score(factors):
    score=0

    breast_factors = OrderedDict([
    ('family_history',["no","yes"] ),       #no,yes 
    ('sex', ["male","female"]),
    ('menarche_age',  [ '-11', '11', '12', '13', '14', '15', '15+']),
    ('children', [ '0', '1', '2', '>2']),
    ('age_of_first_birth',  ['-','-20', '20-24', '25-29', '29+']),
    ('oral_contraception',  [ 'never', 'former', 'current']),
    ('mht',  ['never/former', 'current e-type', 'current other/unknown type (including combined type)']), #menopause hormone replacement
    ('bmi', ['-18.5', '18.5-25', '25-30', '30+']), #body mass index
    ('alcohol',  [ '0', '-5', '5-15', '15-25', '25-35', '35-45', '45+']), #alcohol intake in grams/day
    ('age_of_menopause',  ['-', '-40', '40-44', '45-49', '50-54', '54+']),
    ('height', [ '-152.91', '152.91-159.65', '159.65-165.96', '165.96-172.70', '172.70+']), #in cms
    ('gene_type',["no","brca2","brca1","brca1+2"])
    ])
    

    #print(breast_factors)
    for factor in factors:
        
        score =score + breast_factors[factor].index(factors[factor])
    return score



