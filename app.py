import os
from flask import Flask
from flask import request
from flask import render_template
from operator import attrgetter
import sqlite3 as lite
import re
import copy
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    q = request.args.get('q') or ""
    if len(q) > 20:
        q = q[0:20]
    permutations = []
    words = []

    if q is not None:
        q = q.lower()
        curr_len = len(q)
    else:
        curr_len = 0
    curr_idx = 0

    while curr_len > 0:
        if curr_idx + curr_len <= len(q):
            permutations.append(q[curr_idx:curr_idx+curr_len].upper())
            curr_idx += 1
        else:
            curr_len -= 1
            curr_idx = 0

    try:
        con = lite.connect('dictionary.db')
        con.row_factory = lite.Row

        cur = con.cursor()
        cur.execute('SELECT DISTINCT(UPPER(word)) as word FROM words WHERE UPPER(word) IN (\"'+'\",\"'.join(permutations)+'\") AND LENGTH(word) > 1')

        rows = cur.fetchall()

        for row in rows:
            words.append(row["word"])
    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

    #Determine results using q and words
    results = [[]]

    if q is not None:
        for i in range(0,len(q)):
            for ri in range(0,len(results)):
                r = results[ri]
                if reslen(r) == i:
                    current_r = copy.copy(r)
                    r.append({"w":str(q[i]),"score":0})
                    for w in words:
                        if reslen(current_r)+len(w) <= len(q) and w == q[i:i+len(w)].upper():
                            new = copy.copy(current_r)
                            new.append({"w":str(w),"score":len(w)})
                            results.append(new)

    return render_template('main.html',results=sorted(results,key=lambda x:resscore(x),reverse=True),query=q,words=words)

def reslen(result):
    length = 0
    if result is not None:
        for r in result:
            length += len(r['w'])
    else:
        length = -1
    return length

def resscore(result):
    score = 0.0
    if len(result) > 0:
        for r in result:
            score += r['score']
        score = score/len(result)
    return score

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
