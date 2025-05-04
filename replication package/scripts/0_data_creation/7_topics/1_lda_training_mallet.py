"""
Emotion and Reason in Political Language
-- Replication Package
Gennaro and Ash
2021

Description:
- This script is assigning training a lda model from the data in corp_congress_gpo and corp_congress_gpo with the common global dictionary corp_congress_gpo_and_hein_dictionary

"""

# increase mallet memory 
import os
os.environ['MALLET_XMX'] = '50g'

# from gensim import models
from gensim.models.wrappers import LdaMallet
from gensim.models.coherencemodel import CoherenceModel
path_to_mallet_binary = "/cluster/apps/mallet/2.0.8/x86_64/bin/mallet"
import logging
logging.basicConfig(format='%(asctime)s  %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO)
import sys
import psycopg2
import uuid

# getting numbers of workers from argument calling the script
workers = int(sys.argv[1])

########################################################################################################################
# get dictionary
logging.info('opening db connection')
con = psycopg2.connect(host='id-hdb-psgr-cp7.ethz.ch',  dbname='led')
cur = con.cursor()
# con, cur = db.connect()
logging.info('obtaining dictionary')
sql = """
SELECT
    token_id,
    token
FROM 
    corp_congress_gpo_and_hein_dictionary
ORDER BY
    token_id ASC
"""
cur.execute(sql)
rows = cur.fetchall()
token2id = {row[1]: row[0] for row in rows}
id2token = {row[0]: row[1] for row in rows}
con.close()

########################################################################################################################
# check on how many bags of words there are for server side cursor (which does not know how many results there are)
con = psycopg2.connect(host='id-hdb-psgr-cp7.ethz.ch',  dbname='led')
cur = con.cursor()
cur.execute("""
SELECT 
    sum(cnt) 
FROM (
    SELECT 
        COUNT(bag_of_words_gpo_and_hein) as cnt
    FROM 
        corp_congress_gpo 
    UNION 
    SELECT 
        COUNT(bag_of_words_gpo_and_hein) as cnt
    FROM 
        corp_congress_hein
) AS FOO
""")
rows = cur.fetchall()
corpus_limit = rows[0][0]
# TODO IF NOT TESTING: REMOVE/COMMENT LIMIT OVERWRITING
# corpus_limit = 1000
con.close()

########################################################################################################################
# get all bags of words from server with server side cursor
logging.info('opening server side db connection')
sql = """
SELECT
    bag_of_words_gpo_and_hein
FROM 
    corp_congress_gpo
WHERE 
    bag_of_words_gpo_and_hein is not null
UNION
SELECT
    bag_of_words_gpo_and_hein
FROM 
    corp_congress_hein
WHERE 
    bag_of_words_gpo_and_hein is not null
-- TODO IF NOT TESTING: REMOVE/COMMENT LIMIT
-- LIMIT 1000
"""

class BowIterable:
    def __init__(self, sql, length):
        self.sql = sql
        # length needs to be set manually since server side cursors do not have a length
        # this saves some time in the lda training, since gensim does not need a full
        # iteration just to obtain the length of the iterable
        self.length = length

    def __iter__(self): 
        counter = 0
        con = psycopg2.connect(host='id-hdb-psgr-cp7.ethz.ch',  dbname='led')
        cur = con.cursor(f'lda_training_mallet_gpo_and_hein_cursor_{uuid.uuid4()}', scrollable=True)
        cur.itersize = 2000
        cur.execute(sql)
        rows = iter(cur)
        for row in rows:
            bow = row[0]
            yield bow

    def __len__(self):
        return self.length

corpus = BowIterable(sql, corpus_limit)

########################################################################################################################
# define function to perform training and coherence score for different numbers of topics
# of you don't need the coherence score, get rid of that as it consumes some time
# if you just need to train one model, use the same integer for start and stop
def train_and_measure(id2token, corpus, start, stop, step, workers):
    """
    Compute u_mass coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    stop : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    num_topic = []
    for num_topics in range(start, stop+1, step):

        logging.info(f'performing lda training with {num_topics} topics and {workers} workers')
        model = LdaMallet(
                          path_to_mallet_binary, 
                          corpus,
                          id2word = id2token,
                          num_topics = num_topics,
                          workers = workers
                         )

        logging.info('saving lda model')
        model.save('lda_models/lda_gpo_and_hein_%03d_topics.pkl'%(num_topics))
        
        # report coherence score
        logging.info('calculating coherence score (model training is finished already)')
        coherence_model_lda = CoherenceModel(model=model, corpus=corpus, dictionary=id2token, coherence='u_mass')
        coherence_lda = coherence_model_lda.get_coherence()
        logging.info(f'\n    COHERENCE OUTPUT: trained model with {num_topics} topics')
        logging.info(f'    COHERENCE SCORE: {coherence_lda}\n')
        num_topic.append(num_topics)
        coherence_values.append(coherence_model_lda.get_coherence())

    return num_topic,coherence_values

########################################################################################################################
# perform lda training
num_topic, coherence_values = train_and_measure(
                                                id2token = id2token, 
                                                corpus = corpus, 
                                                start = 128,
                                                stop = 128,  
                                                step = 10,
                                                workers = workers
                                                )

########################################################################################################################
# plot coherence measure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.plot(num_topic, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.savefig('coherence_values.png')
