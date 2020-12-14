# name: Phuong Truong
# finalproject.py

import math

def clean_text(txt):
    """returns a list containing the words in txt after it has been “cleaned”.
    """
    s = txt.lower()

    s = s.replace('.', '')
    s = s.replace(',', '')
    s = s.replace('?', '')
    s = s.replace('!', '')
    s = s.replace(';','')
    s = s.replace(':','')
    s = s.split()
    return s

def stem(s):
    """accepts a string as a parameter. The function should then return the stem of s.
    """
    if s[-2:] == 'es':
        s = s[:-2]
    elif s[-2:] == 'ed':
        s = s[:-2]
    elif s[-2:] == 'er':
        s = s[:-2]
    elif s[-2:] == 'ly':
        s = s[:-2]
    elif s[-3:] == 'ing':
        if len(s) > 4 and s[-4] == s[-5]:
            s = s[:-4]
        elif len(s) == 4:
            s = s
        else:
            s = s[:-3]
    elif s[-1:] == 'y':
        s = s[:-1] + 'i'
    elif s[-1:] == 'e':
        s = s[:-1]
    elif s[-1:] == 's':
        s = s[:-1]
    else:
        s = s
        
    suffix_1 = ['s','y','e']
    suffix_2 = ['es','ed','er','ly']
    suffix_3 = ['ing']
    if s[-1:] in suffix_1:
        stem_rest = stem(s[:-1])
        return stem_rest
    elif s[-2:] in suffix_2:
        stem_rest = stem(s[:-2])
        return stem_rest
    elif s[-3:] in suffix_3:
        stem_rest = stem(s[:-3])
        return stem_rest
    return s

def compare_dictionaries(d1,d2):
    """It should take two feature dictionaries d1 and d2 as inputs, 
    compute and return their log similarity score.
    """
    score = 0
    total = sum(d1.values())
    for key in d2:
        if key in d1:
            score += math.log((d1[key]/total))*d2[key]
        else:
            score += math.log((0.5/total))*d2[key]
    return score

    
class TextModel:
    def __init__(self, model_name):
        """Accept a string model_name as a parameter and initialize three attributes:
           name, words, and word_lengths.
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation: ' + str(len(self.punctuation))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
       to all of the dictionaries in this text model.
        """
        word_list = clean_text(s)

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        word_length = [len(w) for w in word_list]
        for l in word_length:
            if l not in self.word_lengths:
                self.word_lengths[l] = 1
            else:
                self.word_lengths[l] += 1

        c = s.split()
        sentence = []
        count = 0
        for word in c:
            if word[-1] in '.?!':
                count +=1
                sentence += [count]
                count = 0
            else:
                count +=1

        for length in sentence:
            if length not in self.sentence_lengths:
                self.sentence_lengths[length] = 1
            else:
                self.sentence_lengths[length] +=1


        stem_list = [stem(w) for w in word_list]
        for word in stem_list:
            if word not in self.stems:
                self.stems[word] = 1
            else:
                self.stems[word] += 1

        punctuations = []
        for word in c:
            if word[-1] in '.?!:-,;':
                punctuations += word[-1]

        for p in punctuations:
            if p not in self.punctuation:
                self.punctuation[p] = 1
            else:
                self.punctuation[p] += 1

    def add_file(self, filename):
        """Adds all of the text in the file identified by filename to the model."""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        content = f.read()
        self.add_string(content)
        f.close()

    def save_model(self):
        """Saves the TextModel object self by writing its various feature dictionaries to files.
        """
        word_dict = self.words
        word_lengths_dict = self.word_lengths
        stems_dict = self.stems
        sentence_lengths_dict = self.sentence_lengths
        punctuation_dict = self.punctuation
        f1 = open(self.name + '_' + 'words', 'w')
        f2 = open(self.name + '_' + 'word_lengths', 'w')
        f3 = open(self.name + '_' + 'stems', 'w')
        f4 = open(self.name + '_' + 'sentence_lengths', 'w')
        f5 = open(self.name + '_' + 'punctuation', 'w')
        f1.write(str(word_dict))
        f2.write(str(word_lengths_dict))
        f3.write(str(stems_dict))
        f4.write(str(sentence_lengths_dict))
        f5.write(str(punctuation_dict))
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()

    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from their files and
           assigns them to the attributes of the called TextModel.
        """
        f1 = open(self.name + '_' + 'words', 'r')
        f2 = open(self.name + '_' + 'word_lengths', 'r')
        f3 = open(self.name + '_' + 'stems', 'r')
        f4 = open(self.name + '_' + 'sentence_lengths', 'r')
        f5 = open(self.name + '_' + 'punctuation', 'r')
        word_dict_str = f1.read()
        word_lengths_dict_str = f2.read()
        stems_dict_str = f3.read()
        sentence_lengths_dict_str = f4.read()
        punctuation_dict_str = f5.read()
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()

        word_dict = dict(eval(word_dict_str))
        word_lengths_dict = dict(eval(word_lengths_dict_str))
        stems_dict = dict(eval(stems_dict_str))
        sentence_lengths_dict = dict(eval(sentence_lengths_dict_str))
        punctuation_dict = dict(eval(punctuation_dict_str))

        self.words = word_dict
        self.word_lengths = word_lengths_dict
        self.stems = stems_dict
        self.sentence_lengths = sentence_lengths_dict
        self.punctuation = punctuation_dict

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the similarity of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        return [word_score, word_lengths_score, stems_score, sentence_lengths_score, punctuation_score]

    def classify(self, source1, source2):
        """ompares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2)
           and determines which of these other TextModels is the more likely source of the called TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print('scores for ', source1.name,': ', scores1)
        print('scores for ', source2.name,': ', scores2)

        higher_1 = 0
        higher_2 = 0
        if scores1[1] > scores2[1]:
            higher_1 += 1
        elif scores1[1] < scores2[1]:
            higher_2 += 1
        elif scores1[2] > scores2[2]:
            higher_1 +=1
        elif scores1[2] < scores2[2]:
            higher_2 +=1
        elif scores1[3] > scores2[3]:
            higher_1 +=1
        elif scores1[3] < scores2[3]:
            higher_2 +=1
        elif scores1[4] > scores2[4]:
            higher_1 +=1
        elif scores1[4] < scores2[4]:
            higher_2 +=1
        elif scores1[5] > scores2[5]:
            higher_1 +=1
        elif scores1[5] < scores2[5]:
            higher_2 +=1
        else:
            higher_1 = higher_1
            higher_2 = higher_2

        if higher_1 > higher_2:
            print(self.name,'is more likely to have come from',source1.name)
        elif higher_1 < higher_2:
            print(self.name,'is more likely to have come from',source2.name)


def test():
    """test if mystery is more likely to come from source1 or source2.
    """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
        

def run_tests():
    """test if new files is more likely to have come from which sources.
    """
    source1 = TextModel('NYTimes')
    source1.add_file('New York Times.txt')

    source2 = TextModel('WSJ')
    source2.add_file('WSJ.txt')

    new1 = TextModel('BostonGlobe')
    new1.add_file('Boston Globe.txt')
    new1.classify(source1, source2)

    new2 = TextModel('CNN')
    new2.add_file('CNN.txt')
    new2.classify(source1, source2)

    new3 = TextModel('Forbes')
    new3.add_file('Forbes.txt')
    new3.classify(source1, source2)

    new4 = TextModel('FoxNews')
    new4.add_file('Fox News.txt')
    new4.classify(source1, source2)

    test1 = TextModel('test_nytimes')
    test1.add_file('test nytimes.txt')
    test1.classify(source1, source2)

    test2 = TextModel('test_wsj')
    test2.add_file('test wsj.txt')
    test2.classify(source1, source2)

    

        
