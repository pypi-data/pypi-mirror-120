import fairies as fa

def get_tongyin():
    tongyin = fa.read_json('same_pinyin.json')
    return tongyin

def get_tongxing():
    tongxing = fa.read_json('same_pinyin.json')
    return tongxing

def get_hanzi():
    hanzi = fa.read_txt('hanzi.txt')[0]
    return hanzi 
