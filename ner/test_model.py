import spacy

nlp = spacy.load('ner/output/model-last')

def calculate_risk(entity_text, label):
    score = 0
    reason = ''
    
    if label == 'LAW_JURISDICTION':
        text_lower = entity_text.lower()
        if 'delaware' in text_lower:
            score = 10
            reason = 'Governing law is Delaware (Standard/Low Risk for US Contracts).'
        elif 'new york' in text_lower:
            score = 30
            reason = 'Governing law is New York (Standard business jurisdiction).'
        else:
            score = 75
            reason = 'Non-standard or foreign jurisdiction detected. High compliance risk.'
            
        if 'terminate' in text_lower and '30-day' in text_lower:
            score += 15
            reason += ' Short notice termination clause added (+15 Risk).'
            
    return min(score, 100), reason

text = 'This Agreement shall be governed by the laws of the State of Delaware. Either party may terminate this agreement with a 30-day prior written notice.'
doc = nlp(text)

print('\n' + '='*50)
print('       AI CONTRACT RISK INTELLIGENCE REPORT       ')
print('='*50)

if not doc.ents:
    print('No severe risk entities extracted by NLP Model.')
else:
    for ent in doc.ents:
        score, reason = calculate_risk(ent.text, ent.label_)
        
        print(f'\nDetected Clause: "{ent.text}"')
        print(f'Classification : {ent.label_}')
        print(f'Risk Score     : {score}/100')
        
        if score < 40:
            print('Risk Assessment: LOW RISK🟢')
        elif score < 70:
            print('Risk Assessment: MEDIUM RISK🟡')
        else:
            print('Risk Assessment: HIGH RISK🔴')
            
        print(f'Analysis Reason: {reason}')
print('='*50 + '\n')
