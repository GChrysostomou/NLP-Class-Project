#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:27:42 2018

@author: kokos
"""

from sklearn.ensemble import ExtraTreesClassifier
from nltk.corpus import brown
import random
from nltk.corpus import cess_esp

class feature_test_base(object):

    def __init__(self, language, trainset):
        self.language = language
        
        def syl(word):
            vowel = "a e i o u y".split(" ")
            syllables = "V CV VC CVC CCV CCVC CVCC".split(" ")
            syl = ""
            number_of_syllables = 0
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
            return number_of_syllables
        
        if self.language == "english":
            
            
            print("\n Word - length \n")
            
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += len(sent["target_word"])
                    s += 1
                else:
                    comp += len(sent["target_word"])
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.length =", simple)
            print("Complex word av.length =", comp)
            
            print("\n")
            
            print("\n Probability \n")
            
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
                    
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += self.freq_vocab[sent["target_word"]]/len(self.freq_vocab)
                    s += 1
                else:
                    comp += self.freq_vocab[sent["target_word"]]/len(self.freq_vocab)
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.prob =", simple)
            print("Complex word av.prob =", comp)
            
            print("\n")
            
            print("\n Syllables \n")
            
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += syl(sent["target_word"])
                    s += 1
                else:
                    comp += syl(sent["target_word"])
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.syllables =", simple)
            print("Complex word av.syllables =", comp)
            
        else: # if its spanish
            print("\n Word - length \n")
            
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += len(sent["target_word"])
                    s += 1
                else:
                    comp += len(sent["target_word"])
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.length =", simple)
            print("Complex word av.length =", comp)
            
            print("\n")
            
            print("\n Probability \n")
            
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
                     
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += self.freq_vocab_s[sent["target_word"]]/len(self.freq_vocab_s)
                    s += 1
                else:
                    comp += self.freq_vocab_s[sent["target_word"]]/len(self.freq_vocab_s)
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.prob =", simple)
            print("Complex word av.prob =", comp)
            
            print("\n")
            
            print("\n Syllables \n")
            
            comp = 0
            simple = 0
            
            c = 0
            s = 0
            
            
            for sent in trainset:
                if sent["gold_label"] == "0":
                    simple += syl(sent["target_word"])
                    s += 1
                else:
                    comp += syl(sent["target_word"])
                    c += 1
                    
            simple = simple/s
            comp = comp/c
            
            print("Simple word av.syllables =", simple)
            print("Complex word av.syllables =", comp)
#          