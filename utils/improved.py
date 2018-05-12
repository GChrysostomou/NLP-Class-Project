from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from nltk.corpus import brown
import random
from nltk.corpus import cess_esp

random.seed(12412412)

class improved_system(object):

    def __init__(self, language, trainset):
        self.language = language
        
        if self.language == "english":

            self.model = RandomForestClassifier(bootstrap = True, random_state = 124)
            self.freq_vocab = {}
            
            # Using the brown corpus to  obtain frequencies
            a =  brown.categories()
            
            for i in range(len(a)):
                file = brown.words(categories=a[i])
                for word in file:
                    if word not in self.freq_vocab:
                        self.freq_vocab[word] = 1
                    else:
                        self.freq_vocab[word] += 1
           
            # obtain frequencies from our train dataset
            self.pos_tag = {}
            for sent in trainset:

                word = sent["target_word"]    
                if word in self.freq_vocab:
                    self.freq_vocab[word] += 1
                else:
                    self.freq_vocab[word] = 1
                    
            # create alphabet dictionary
            self.alphabet = sorted("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ".split(" "))
            self.alphabet.append(" ")
            self.alphabet.append("")
            self.alphabet = {word: i for i, word in enumerate(self.alphabet)}
            
        else: # if its spanish

            self.model = ExtraTreesClassifier(criterion = "entropy", random_state = 124)

            # create a frequency vocabulary from corpus and training data
            self.freq_vocab_s = {}
            word = cess_esp.words()
            
            for item in word:
                if item in self.freq_vocab_s:
                    self.freq_vocab_s[item] += 1
                else:
                    self.freq_vocab_s[item] = 1
                        
            for sent in trainset:
                 word = sent["target_word"]    
                 if word in self.freq_vocab_s:
                     self.freq_vocab_s[word] += 1
                 else:
                     self.freq_vocab_s[word] = 1
            
                        
                        
    def extract_features(self, word, sentence):
        
        if self.language == "english":
            
            # character number
            len_chars = len(word)
            
            # vowels in english
            vowel = "a e i o u y".split(" ")
            # syllable vowel-consonant sequences from observation
            syllables = "V CV VC CVC CCV CCVC CVCC".split(" ")
                        
            syl = ""
            
            number_of_syllables = 0
            
            curword = "0."
            
            # obtaining syllables and creating current word representation
            # by mapping each string to its alphabetical position in the
            # dictionary
            for char in word.lower():
    
                if char in vowel:
                    syl += "V"
                    
                if char not in vowel:
                    syl += "C"
                    
                if char == " ":
                    syl += ""
                
                    
                if syl in syllables:
                    number_of_syllables += 1
                    syl = ""
                    
                
                tok = str(char).upper()
                if tok in self.alphabet:
                    curword += str(self.alphabet[tok])
                else:
                    curword += "37"
                    
            curword = float(curword)
                
            # obtaining word probabilities
            if word in self.freq_vocab:
                prob_w = self.freq_vocab[word]/len(self.freq_vocab)
            else:
                prob_w = 1/len(self.freq_vocab)
                
                        
            return[len_chars, number_of_syllables, prob_w, curword]
        
        else:
            # number of characters
            len_chars = len(word)
            
            # syllable sequences of vowel-consonant from observations
            syllables = "V CV VC CVC CCV CVVC CCCV CVV CCVC".split(" ")
            
            # vowels in spanish
            vowel = "a e i o u".split(" ")
            
            syl = ""
            
            number_of_syllables = 0
            
            # extract syllable numbers
            for char in word.lower():
    
                if char in vowel:
                    syl += "V"
                    
                if char not in vowel:
                    syl += "C"
                    
                if char == " ":
                    syl += ""
                    
                if syl in syllables:
                    number_of_syllables += 1
                    syl = ""
                    
                           
            # extract word probability
            if word in self.freq_vocab_s:
                prob_w = self.freq_vocab_s[word]/len(self.freq_vocab_s)
            else:
                prob_w = 1/len(self.freq_vocab_s)
                
            
            return [len_chars, prob_w, number_of_syllables]
        
                    
    def train(self, trainset):
        X = []
        y = []
        for sent in trainset:
           
            X.append(self.extract_features(sent['target_word'], sent['sentence']))
            y.append(sent['gold_label'])

        self.model.fit(X, y)

    def test(self, devset):
        X = []
        for sent in devset:
            X.append(self.extract_features(sent['target_word'], sent['sentence']))

        return self.model.predict(X)
#        
