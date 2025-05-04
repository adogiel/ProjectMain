"""
Emotion and Reason in Political Language
-- Replication Package
Gennaro and Ash
2021

Description:
- This script is assigning lda topics to corp_congress_gpo/_hein based on global lda model


"""

# from gensim import models
import gensim
import logging
logging.basicConfig(format='%(asctime)s  %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO)
import sys
sys.path.append("/cluster/work/lawecon/Work/goessmann/python_common/")
import database_connection as db
from psycopg2 import extras

# get from argv if gpo or hein should be assigned
if sys.argv[1] == 'gpo' or sys.argv[1] == 'hein':
    dataset = sys.argv[1]
    # dataset = 'gpo' sys.argv[1] == 1 else None
    # dataset = 'hein' if sys.argv[1] == 2 else None
    modulo_int = sys.argv[2] if sys.argv[2] else 0
    batch_int = sys.argv[3] if sys.argv[3] else 0
else:
    logging.info(f'there was no valid argv provided, argv was {sys.argv[1]}, type {type(sys.argv[1])}')
    exit()

# load lda model
logging.info('loading lda model')
lda_mallet = gensim.models.wrappers.LdaMallet.load('lda_models/lda_gpo_and_hein_128_topics.pkl')
lda_gensim = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_mallet)

# check on how many bags of words are there
con, cur = db.connect()
cur.execute(f"SELECT COUNT(bag_of_words_gpo_and_hein) FROM corp_congress_{dataset} where {dataset}_id%{modulo_int} = {batch_int}")
rows = cur.fetchall()
corpus_limit = rows[0][0]
con.close()

# get all from server with server side cursor
logging.info('opening server side db connection')
sql = f"""
SELECT
    bag_of_words_gpo_and_hein,
    {dataset}_id
FROM 
    corp_congress_{dataset}
WHERE 
    bag_of_words_gpo_and_hein is not null and
    {dataset}_id%{modulo_int} = {batch_int}
"""

class BowIterator:
    def __init__(self, sql, length):
        self.sql = sql
        # length needs to be set manually since server side cursors do not have a length
        # this saves some time in the lda training, since gensim does not need a full
        # iteration just to obtain the length of the iterable
        self.length = length

    def __iter__(self): 
        counter = 0
        con, cur = db.connect(cursor_type='server')
        cur.itersize = 2000
        cur.execute(sql)
        rows = iter(cur)
        for row in rows:
            id = row[1]
            bow = row[0]
            yield (id, bow)

    def __len__(self):
        return self.length

corpus = BowIterator(sql, corpus_limit)

# create empty array for results
result_rows = list()

# starting assignment
logging.info('starting assignment')
for id, bow in corpus:
    document_topics = [[int(topic), float(score)] for topic, score in lda_gensim.get_document_topics(bow)]
    result_rows.append((id, document_topics))
logging.info('finished assignment')

# write results to database
logging.info('writing results to database')
con, cur = db.connect(cursor_type='client', scrollable=False)
sql = f"""
WITH data (id, lda_document_topics) AS
    (VALUES %s) 
UPDATE
    corp_congress_{dataset}
SET
    lda_topics_gpo_and_hein_128_mallet = data.lda_document_topics
FROM
    data
WHERE 
    corp_congress_{dataset}.{dataset}_id = data.id
"""
extras.execute_values(cur, sql, result_rows, page_size=2000)
con.commit()
con.close()
logging.info('finished writing to database, closed connection')