from flask import Flask 
from flask_restful import Resource, Api, abort
import os
import pickle
import boto3

app = Flask(__name__)
api = Api(app)

s3 = boto3.resource(service_name='s3', region_name='us-east-2')
s3Client = boto3.client('s3')

class GlobalTrieCMDOnly(Resource):
    def get(self, command):
        if command == 'list':
            my_pickle = pickle.loads(s3.Bucket("newtrieclibucket").Object("trie.pickle").get()['Body'].read())
            words = my_pickle.list_words(my_pickle.root)
            words.remove('')
            return words

class GlobalTrieUpdate(Resource):
    def get(self, command, word):
        if (command == 'check'):
            my_pickle = pickle.loads(s3.Bucket("newtrieclibucket").Object("trie.pickle").get()['Body'].read())
            exist = my_pickle.does_word_exist(word)
            return exist
        elif (command == 'recommend'):
            my_pickle = pickle.loads(s3.Bucket('newtrieclibucket').Object('trie.pickle').get()['Body'].read())
            words = my_pickle.words_with_prefix(word)   
            return words
        elif (command == 'add'):
            my_pickle = pickle.loads(s3.Bucket("newtrieclibucket").Object("trie.pickle").get()['Body'].read())
            my_pickle.addWord(word)
            pickle_out = open('trie.pickle', 'wb')
            pickle.dump(my_pickle, pickle_out)
            pickle_out.close()
            s3Client.upload_file('trie.pickle','newtrieclibucket', 'trie.pickle')
            return 'Word Added Successfully!'
        elif (command == 'remove'):
            try:
                my_pickle = pickle.loads(s3.Bucket("newtrieclibucket").Object("trie.pickle").get()['Body'].read())
                my_pickle.remove_word(word)
                pickle_out = open('trie.pickle', 'wb')
                pickle.dump(my_pickle, pickle_out)
                pickle_out.close()
                s3Client.upload_file(
                    'trie.pickle',
                    'newtrieclibucket', 'trie.pickle')
                return 'Word Removed Successfully!'
            except:
                return 'Word does not exist in Trie!'
            

api.add_resource(GlobalTrieCMDOnly, '/updatetrie/<string:command>')
api.add_resource(GlobalTrieUpdate, '/updatetrie/<string:command>/<string:word>')

if __name__ == '__main__':
    app.run()
