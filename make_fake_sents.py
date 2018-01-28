import random
import string
import sys

# for matching words, need to check if the found word is the word itself, or
# it is included in the longer word. ex) find('are') actually points to 'aware'

# pronoun
# pronoun : possessive
# pronoun : person - oject
entity = ['i', 'my', 'me', 'you', 'your', 'he', 'his', 'him',
        'she', 'her', 'it', 'its', 'we', 'our', 'us',
        'you', 'your', 'they', 'them', 'this', 'these', 'that', 'those',
        'who', 'what', 'which', 'whom', 'whose', 'something', 'anything',
        'nothing', 'someone', 'anyone', 'none']
reflexive = ['myself', 'youself', 'himeself', 'herself', 'itself', 'outselves',
            'yourselves', 'themselves']
_where = ['somewhere', 'anywhere', 'nowhere']
interrogative = ['where', 'when', 'why', 'how']

# conjunction
conj = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'either', 'not only',
        'but also', 'neither', 'both', 'whether', 'just as', 'as much', 'rather']

# subordination conjunction
sub_ordi = ['although', 'as far as', 'as if', 'as long as',
        'as soon as', 'as though', 'because', 'before',
        'even if', 'even though', 'every time', 'if',
        'in order that', 'since', 'so that', 'than', 'though',
        'unless', 'until', 'whenever', 'wherever', 'whereas', 'while']
# preposition
prepos = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along',
        'alongside', 'amid', 'midst', 'mid', 'amidst', 'among', 'amongst',
        'apropos', 'apud', 'around', 'at', 'astride', 'atop', 'ontop', 'bar',
        'before', 'afore', 'behind', 'below', 'beneath', 'neath', 'beside',
        'besides', 'between', 'beyond', 'by', 'circa', 'come', 'despite',
        'down', 'during', 'except', 'for', 'from', 'inside', 'into', 'less',
        'like', 'minus', 'near', 'nearer', 'nearest', 'notwithstanding', 'of',
        'off', 'on', 'onto', 'opposite', 'out', 'outside', 'over', 'past',
        'per', 'plus', 'post', 'pre', 'qua', 're', 'sans', 'save', 'short',
        'since', 'than', 'through', 'throughout', 'thru', 'thruout', 'till',
        'to', 'toward', 'towards', 'under', 'underneath', 'unlike', 'until',
        'til', 'unto', 'up', 'upon', 'upside', 'versus', 'via', 'vice', 'with',
        'within', 'without', 'worth',
# postposition
        'ago', 'apart', 'aside', 'away', 'hence']

# auxiliary verb
aux = ['be', 'dare', 'can', 'do', 'need', 'ought', 'must', 'shall',
        'could', 'might', 'would',
#aux_future
        'will']

speech_classes = [entity, reflexive, _where, interrogative
        conj, sub_ordi, prepos, aux]

# 품사에 따른 fake sent generation
def part_of_speech(sent):
    # shuffle in order to search in random order
    for _ in range(len(speech_classes)):
        random.shuffle(speech_classes)

    is_changed = False # check whether sentence is changed

    for class_i in speech_classes:
        if is_changed == True:
            break
        for phrase in class_i:
            if is_changed == True:
                break
            words = phrase.split() # split phrase
            indices = []
            for w in words:
                pos = sent.find(w)
                if pos != -1 and sent[pos] == w: # check exact match
                    indices.append(pos)
            if len(i) == len(words): # successfully found phrase
                # get random class, except the current class
                r_class = random.randint(0, len(speech_classes)-1)
                # get random phrase
                r_phrase = random.randint(0, len(speech_classes[r_class])-1)
                new_phrase = speech_classes[r_class][r_phrase].split()
                for i in indices:
                    if len(new_phrase) < 1:
                        # delete? or pass?
                        break
                    else:
                        sent[i] = new_phrase[0]
                        sent.pop(0)
                is_changed = True
                break

    if is_changed == False:
        return None
    else:
        sys.exit("ERROR in function part_of_speech, make_fake_sents.py")

# swap word
def swap(sent):
    # get number of times to swap
    num = random.randint(2, max(2, len(sent)/2-1))

    # get sub-sentence to swap
    indices = random.sample(range(len(sent)), num)
    subsent = []
    for i in indices:
        subsent.append(sent[i])
    #swap
    for _ in range(len(subsent)/2):
        random.shuffle(subsent)
    for i, w in zip(indices, subsent):
        sent[i] = w
    return sent

# find combined phrase or separated multiple words
# args : [arg, arg, ...]
# arg : ["word", "word", ...]
# sub_word : if None, it find exact match.
#     if 0, this function finds the word that exactly matches argument
#     if 1, find the word that includes the argument word.
#     ex) find('are') <--> aware
def find_mult(sent, args, sub_word = None):
    i = [] # store words position
    pos = 0
    iterator = 0
    for arg in args: # search for words in args
        for w in arg:
            pos = sent.find(w, pos)
            if pos != -1: # if find any word in arg, break
                if sub_word == None: # default option
                    if sent[pos] == w: # check exact match
                        i.append(pos)
                        break
                else:
                    if sub_word[iterator] == 0: # perform exact match
                        if sent[pos] == w:
                            i.append(pos)
                            break
                    else:
                        i.append(pos)
                        break
        iterator += 1
    if len(i) < len(args):
        return None
    else:
        return i

# swap phrase within the sentence
def swap_phrase(sent, args):
    indices = find_mult(sent, args)
    if indices is not None:
        subsent = []
        for i in indices:
            subsent.append(sent[indices[i]])
        random.shuffle(subsent)
        for i in indices:
            sent[indices[i]] = subsent[0]
            subsent.pop(0) # pop top element
        return sent
    else:
        return None

# change tense
def tense(sent):
    # simple present
    progressive = ['ing']
    present ['now']
    past = ['yesterday', 'the other day', 'had', 'been', 'did', 'done']
    future = ['tomorrow', 'will']
    past_perfect = ['would have', 'could have', 'might have', 'should have']
    future_perfect = ['will have']

    # check if changed
    is_changed = False

    #initialize args
    be_past = [['was', 'were'], progressive]
    be_cont = [['am', 'is', 'are'], progressive]
    will_cont = ['will', 'be', progressive]
    be_past_perf = ['had', 'been', progressive]
    be_present_perf = [['have', 'has'], 'been', progressive]
    be_future_perf = ['will', 'have', 'been', progressive]
    # arguments to pass
    args = [be_past, be_cont, will_cont, be_past_perf, be_present_perf,
        be_future_perf]

    for _ in range(len(args)):
        random.shuffle(args)

    for arg in args:
        out = swap_phrase(sent, arg)
        if out is not None:
            return out
            break

    if is_changed == False:
        return None
    else:
        sys.exit("ERROR in function tense, make_fake_sents.py")


# swap words, wrapping grammar consideration(part of speech, tense)
def grammar_swap(sent):
    funcs = {
        'grammar_swap' : lambda sent : grammar_swap(fake_sent),
        'duplicate' : lambda sent : replace(fake_sent),
        'delete' : lambda sent : delete(fake_sent),
    }
    for _in range(5):
        random.shuffle(funcs)
    for f in funcs:
        out = f(sent)
        if out == None:
            continue
        else:
            return out # successfully swapped
    # swap failed
    return None



# duplicate words
# sent format : ["word", "word", ...]
def duplicate(sent):
    # get the position of the word to be duplicated
    r_pos = random.randint(0, len(sent)-1)
    # get the number of duplication
    r_num = random.randint(1, 3)

    duplicate = [sent[r_pos] for _ in range(r_num)] # get the list to insert
    sent[r_pos:r_pos] = duplicate # insert
    return sent


# delete words(conjunction, preposition, noun/pronoun)
def delete(sent):
    # get the number of words to be deleted
    # gurantee that the processed output is at least 3-gram
    is_change = r_num = random.randint(1, max(2, len(sent)-3))
    # shuffle
    for _ in range(10):
        random.shuffle(entity)
        random.shuffle(_thing)
        random.shuffle(_where)
        random.shuffle(prepos)
    refs = [entity, _thing, _where, prepos]
    for _ in range(5):
        random.shuffle(refs)
    for ref in refs:
        if r_num <=0:
            break
        for w in ref:
            if r_num <=0:
                break
            if sent.find(w) != -1 and r_num > 0:
                sent.remove('w')
                r_num -= r_num
    if r_num == is_change:
        return None
    else:
        return sent

# truncate special tokens, punctuation, dots, etc. then split
def truncate(sent):
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    def remove_token(text):
        while text.find('<eos>') != -1:
            text = text.replace('<eos>', '')
        while text.find('<unk>') != -1:
            text = text.replace('<unk>', '')
        while text.find('<pad>') != -1:
            text = text.replace('<pad>', '')
        return text.strip()
    def remove_dot(text):
        while text.find('.') != -1:
            rext = text.replace('.', '')
        return text.strip()

    def lower(text):
        return text.lower()
    return remove_punc(remove_token(remove_dot(lower(sent)))).split()


# make fake paragraph
# para format : ["sentence", "sentce", ...]
def make_fake(paragraph):
    para = [truncate(s) for s in paragraph] # split and process para
    out_para = []
    for sent in para:
        if len(sent) < 3:
            print("sentence length is shorter than 3")
            continue

        fake_sent = sent

        # decide which function to use
        r = [random.randint(0, 3) for _ in range(0,3)]
        if 1 in r:
            pass
        else: # must call at least one function
            r[random.sample(range(3))] = 1

        funcs = {
            'grammar_swap' : lambda sent : grammar_swap(fake_sent),
            'duplicate' : lambda sent : replace(fake_sent),
            'delete' : lambda sent : delete(fake_sent),
        }
        is_change = False
        for r_i, f in zip(r, funcs):
            if r == 1:
                temp = f(fake_sent)
                if temp != None:
                    fake_sent = temp
                    is_change = True
        if is_change == True:
            out_para.append(fake_sent)

    return out_para
