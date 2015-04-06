ones = {j:i for i, j in enumerate(('zero','one','two','three','four','five','six','seven','eight','nine','|\|/|\|/|',
                                   'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'))}
tens = {j:10*i for i, j in enumerate(('|\|/|\|/|','ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety'))}
places = { j : 1000**(i+1) for i, j in enumerate(('thousand','million','billlion','trillion','quadrillion'))}
places['hundred'] = 100


def convertToNum(toConvert):
    num  = 0
    tnum = 0
    multiplier = 1
    words = toConvert.split(' ')
    for index, i in enumerate(words[::-1]):
        if ones.has_key(i):
            tnum += ones[i]
            
        elif tens.has_key(i):
            tnum += tens[i]
            
        elif places.has_key(i):

            num += tnum * multiplier
            tnum = 0
                
            if multiplier is 1:
                multiplier = places[i]
            elif tnum == 0:
                multiplier *= places[i]
            elif multiplier < places[i]:
                multiplier = places[i]            
            elif multiplier >= places[i]:
                multiplier *= places[i]
        else:
            return None
                
    num += tnum * multiplier
    tnum = 0
    return num


operations =  ('plus','minus','times','divided by','to the power of')
replacements = ('+','-','*','\\','^')
def calculate(string):
    string=string.replace('what is','')
    string=string.replace('calculate','')
    for i, op in enumerate(operations):
        string = string.replace(op,replacements[i])
    for i in replacements:
        string = string.replace('%s'%i,'~%s~'%i)
    parts = string.split('~')
    print parts
    func = ''
    for i in parts:
        i = i.replace('^', '**')
        i = i.replace(' ', '')
        if not(i.isdigit() or i in replacements):
            asNum = convertToNum(i)
            if asNum is not None:
                i = str(asNum)
        if i.isdigit() or i in replacements:
            func += i
    try:
        print func
        return eval(func)
    except:
        return 'error'


