import pickle

class Trie:

    def __init__(self):
        self.root = {'*': '*'}

    def addWord(self, word):
        currNode = self.root
        for letter in word:
            if letter not in currNode:
                currNode[letter] = {}
            currNode = currNode[letter]
        currNode['*'] = '*'

    def does_word_exist(self, word):
        currNode = self.root
        for letter in word:
            if letter not in currNode:
                return False
            currNode = currNode[letter]
        return '*' in currNode

    def list_words(self, trie):
        my_list = []
        for k,v in trie.items():
            if k != '*':
                for el in self.list_words(v):
                    my_list.append(k+el)
            else:
                my_list.append('')
        return my_list

    #Function below was a reference from stackoverflow. https://stackoverflow.com/questions/15709261/how-to-implement-the-remove-function-of-a-trie-in-python
    def words_with_prefix(self, prefix: str):
        '''
        return all possible words with common prefix
        '''
        node = self.root
        for c in prefix:
            if c not in node:
                return []
            node = node[c]
        ans = []
        self._words_with_prefix_helper(node, prefix, ans)
        return ans

    def _words_with_prefix_helper(self, node, prefix, ans):
        for k in node:
            if k == '*':
                ans.append(prefix)
                continue
            self._words_with_prefix_helper(node[k], prefix + k, ans)

    def remove_word(self, word):
        current_dict = self.root
        for letter in word:
            current_dict = current_dict.get(letter, None)
            if current_dict is None:
                break
        else:
            del current_dict['*']

#trie = Trie()
# pickle_out = open('trie.pickle', 'wb')
# pickle.dump(trie, pickle_out)
# pickle_out.close()
# words = []
# #
# def useTrie(choice: str):
#     if choice == 'a' or choice == 'A':
#         word = input('What word would you like to add to the tree? ')
#         print()
#         if (trie.does_word_exist(word) == False):
#             words.append(word)
#             trie.addWord(word)
#             print(words)
#             print()
#         else:
#             print("This word already exists in the tree!")
#             print()
#
#     elif choice == 'c' or choice == 'C':
#         wordToCheck = input('What word would you like to check? ')
#         print()
#         print(trie.does_word_exist(wordToCheck))
#         print()
#
#     elif choice == 'r' or choice == 'R':
#         wordtoRec = input('What is part of the word that you would like a recommendation for? ')
#         print()
#         lowerWordToRec = wordtoRec.lower()
#         print(trie.words_with_prefix(lowerWordToRec))
#         print()
#
#     elif choice == 'd' or choice == 'D':
#         try:
#             wordToDelete = input('What word would you like to delete? ')
#             words.remove(wordToDelete)
#             trie.remove_word(wordToDelete)
#             print(words)
#         except:
#             print('That word does not exist in the trie!')
#     elif choice == 'l' or choice == 'L':
#         print('Here is a list of all words in the trie!')
#         print()
#         lt = trie.list_words(trie.root)
#         lt.remove('')
#         print(lt)
#     else:
#         print('Please use the given commands!')
#         print()
#
#
# while True:
#     x = input('Choice. ')
#     useTrie(choice=x)