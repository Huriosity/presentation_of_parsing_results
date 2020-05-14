from tkinter import *
from tkinter import filedialog
from docx import Document
import nltk

from tkinter import messagebox
from operator import itemgetter
import requests
import json
from tkinter import *
file_name = []
file_name.append('')

def calculation(line):
    list_words = []
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Charset': 'UTF-8'
    }

    params = (
        ('targetType', 'pos-token'),
        ('targetType', 'spelling-correction-token'),
        ('targetType', 'syntax-relation'),
        ('apikey', 'b11e0cc09d4d7b3c4c56116688dd27beae454257'),
    )
    line = line.replace('\n', ' ')
    data = '[ { "text" : "' + str(line) + '" } ]'

    response = requests.post('http://api.ispras.ru/texterra/v1/nlp', headers=headers, params=params,
                             data=data.encode('utf-8'))
    parsed_string = json.loads(response.text)
    position = parsed_string[0]['annotations']['pos-token']
    word = parsed_string[0]['annotations']['spelling-correction-token']
    syntax = parsed_string[0]['annotations']['syntax-relation']
    print(word)
    i = 0
    while i < len(word):
        name_word = word[i]['value']
        char = position[i]['value']['characters']
        if position[i]['value']['tag'] == 'PUNCT':
            i += 1
            continue
        syntax_word = syntax[i]['value']
        param = ''
        if syntax_word:
            if syntax_word['type']:
                param = syntax_word['type']
        tags = [position[i]['value']['tag']]
        for j in char:
            tags.append(j['tag'])
        if param:
            tags.append(param)
        list_words.append({'name': name_word, 'param': tags})
        i += 1
    list_tuple = []
    i = len(list_words)-1
    while i >= 0:
        list_tuple.append((list_words[i]['name'], list_words[i]['param'][0]))
        i -= 1
    return list_tuple[::-1]

def get_filename():
    global file_name
    file_name[0] = filedialog.askopenfilename(filetypes=(("Документ Microsoft Word", "*.docx"),))
    file_path_entry.insert(0, file_name[0])

grammar = r"""
    P: {<IN>}
    VP: {<V.*|MD>}
    NP: {<A|PR.*|A|S.*>+}          
    PP: {<IN><NP>}              
    VP: {<V.*><NP|RB|PP|CLAUSE>+$} 
    CLAUSE: {<NP><VP>}          
    """
def result_picture():
    path = file_path_entry.get().replace('\n', '')
    document = Document(path)
    document.save(path)

    message = ""
    for para in document.paragraphs:
        message += para.text
        
    if message != '':
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
        doc = calculation(message)
        print(doc)
        new_doc = []
        for item in doc:
            if item[1] != ',' and item[1] != '.':
                new_doc.append(item)
        grammar = r"""
         P: {<IN>}
         VP: {<V.*|MD>}
         NP: {<A|PR.*|A|S.*>+}          
         PP: {<IN><NP>}              
         VP: {<V.*><NP|RB|PP|CLAUSE>+$} 
         CLAUSE: {<NP><VP>}          
         """
        cp = nltk.RegexpParser(grammar).parse(new_doc).draw()

root = Tk()
root.title("Lab 3")
root.resizable(width=True, height=True)
root.geometry("580x250+300+300")

open_file_btn = Button(text="Открыть файл", command=get_filename)
open_file_btn.grid(row=0, column=0)

file_path_entry = Entry(root,width=40)
file_path_entry.grid(row=0, column=1)
Button(text="Submit", width=10, command=result_picture).grid(row=0, column=2)

root.mainloop()
