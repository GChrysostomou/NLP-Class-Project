from sklearn.neural_network import MLPClassifier
from nltk.corpus import brown
import random
from nltk.corpus import cess_esp

random.seed(12412412)

class Baseline(object):

    def __init__(self, language, trainset):
        self.language = language
        
        if self.language == "english":
#            nlp = spacy.load('en')
            self.model = MLPClassifier()
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
           
            
            self.pos_tag = {}
            for sent in trainset:

                word = sent["target_word"]    
                if word in self.freq_vocab:
                    self.freq_vocab[word] += 1
                else:
                    self.freq_vocab[word] = 1
                    
                    
            self.alphabet = sorted("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ".split(" "))
            self.alphabet.append(" ")
            self.alphabet.append("")
            self.alphabet = {word: i for i, word in enumerate(self.alphabet)}
            
        else: # if its spanish

            self.model = MLPClassifier()

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
                        

                        
            self.alphabet = sorted("A B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z".split(" "))
            self.alphabet.append(" ")
            self.alphabet.append("")
            self.alphabet = {word: i for i, word in enumerate(self.alphabet)}
                        
                        
    def extract_features(self, word, sentence):
        
        if self.language == "english":
            
            len_chars = len(word)
            
            vowel = "a e i o u y".split(" ")
            syllables = "V CV VC CVC CCV CCVC CVCC".split(" ")
            vowel_seq = "0."
            
            double_vow = 0
            double_vowel = ""
            
            syl = ""
            
            number_of_syllables = 0
            
            curword = "0."
            
            for char in word.lower():
    
                if char in vowel:
                    vowel_seq += "1"
                    syl += "V"
                    double_vowel += "V"
                    
                if char not in vowel:
                    vowel_seq += "0"
                    syl += "C"
                    double_vowel += "C"
                    
                if char == " ":
                    syl += ""
                    double_vowel += ""
                    
                if "CCC" in double_vowel:
                    double_vow += 1
                    double_vowel = ""
                
                    
                if syl in syllables:
                    number_of_syllables += 1
                    syl = ""
                    
                
                tok = str(char).upper()
                if tok in self.alphabet:
                    curword += str(self.alphabet[tok])
                else:
                    curword += "37"
                    
            curword = float(curword)
                
            #print(word, double_vow)
            #vowel_seq = float(vowel_seq)
            
            if word in self.freq_vocab:
                prob_w = self.freq_vocab[word]/len(self.freq_vocab)
            else:
                prob_w = 1/len(self.freq_vocab)
                
                        
            return[len_chars, number_of_syllables,prob_w, curword, double_vow]
        
        else:
            
            len_chars = len(word)
            
            #syllables = "V CV VC CVC CCV CCCV CVCC".split(" ")
            syllables = "V CV VC CVC CCV CVVC CCCV CVV CCVC".split(" ")


            vowel = "a e i o u".split(" ")
            vowel_seq = "0."
            
            double_vow = 0
            double_vowel = ""
            
            syl = ""
            
            curword = "0."
            
            number_of_syllables = 0
            
            for char in word.lower():
    
                if char in vowel:
                    vowel_seq += "1"
                    syl += "V"
                    double_vowel += "V"
                    
                if char not in vowel:
                    vowel_seq += "0"
                    syl += "C"
                    double_vowel += "C"
                    
                if char == " ":
                    syl += ""
                    double_vowel += ""
                    
                if "CCC" in double_vowel:
                    double_vow += 1
                    double_vowel = ""
                
                    
                if syl in syllables:
                    number_of_syllables += 1
                    syl = ""
                    
                tok = str(char).upper()
                if tok in self.alphabet:
                    curword += str(self.alphabet[tok])
                else:
                    curword += "37"
                    
            curword = float(curword)
                    
            vowel_seq = float(vowel_seq)
            
            if word in self.freq_vocab_s:
                prob_w = self.freq_vocab_s[word]/len(self.freq_vocab_s)
            else:
                prob_w = 1/len(self.freq_vocab_s)
                
            #return [len_chars, prob_w, number_of_syllables]
            return [len_chars, number_of_syllables, prob_w, curword]
        
                    
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
