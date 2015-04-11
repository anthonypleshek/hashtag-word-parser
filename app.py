from flask import Flask
from flask import request
import sqlite3 as lite
import re
import copy
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    q = request.args.get('q') or None
    returnval = ""
    permutations = []
    words = []

    curr_len = len(q)
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
        # cur.execute('SELECT word FROM words WHERE word LIKE \"%'+q+'%\"')
        # print 'SELECT word FROM words WHERE word IN (\"'+'\",\"'.join(permutations)+'\")'
        cur.execute('SELECT DISTINCT(UPPER(word)) as word FROM words WHERE UPPER(word) IN (\"'+'\",\"'.join(permutations)+'\")')

        rows = cur.fetchall()

        for row in rows:
            returnval += row["word"] + "\n"
            words.append(row["word"])
    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if con:
            con.close()

    #Determine results using q and words
    results = [[]]

    for i in range(0,len(q)):
        for ri in range(0,len(results)):
            r = results[ri]
            if reslen(r) == i:
                current_r = copy.copy(r)
                r.append([q[i],0])
                for w in words:
                    if w[0] == q[i].upper() and reslen(current_r)+len(w) <= len(q):
                    # if reslen(current_r)+len(w) <= len(q):
                        print q[i:i+len(w)].upper() + " =?= " + w
                        if w == q[i:i+len(w)].upper():
                            new = copy.copy(current_r)
                            new.append([w,len(w)])
                            results.append(new)


    # for word in words:
    #     # if word.startswith(q[0].upper()):
    #     if q.upper().startswith(word):
    #         results.append([(word,True)])
    #
    # for result in results:
    #     matchwords(results,result,words,q[len(results[0][0]):])

    print results

    # return returnval
    return returnval + '<br><br><br><br><br><br>' + json.dumps(results)

def reslen(result):
    length = 0
    if result is not None:
        for r in result:
            length += len(r[0])
    else:
        length = -1
    return length

# def matchwords(results,result,words,query):
#     for word in words:
#         # if word.startswith(query[0]):
#         if query.upper().startswith(word) and result is not None:
#             results.append(result.append([(word,True)]))

if __name__ == '__main__':
    app.debug=True
    app.run()
