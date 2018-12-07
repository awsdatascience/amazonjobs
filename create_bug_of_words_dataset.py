import json
import psycopg2
import numpy as np
import pandas as pd
import re
# import nltk
import operator
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

QUERY = """select * from amazon.amazonjobs_2;"""


def open_database_connection(database):
    conn = None
    if database == 'postgres':
        dbname, user, host, password = 'postgres', 'postgres', 'localhost', 'postgres'
    else:
        print("No database selected")
    try:
        conn = psycopg2.connect(
            "host=%(host)s user=%(user)s password=%(password)s dbname=%(dbname)s"
            % {
                'host': host,
                'user': user,
                'password': password,
                'dbname': dbname
            }
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def fetch_results_to_dataframe(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if rows and rows[0][0] != None:
        rows_array = np.array(rows)
        df = pd.DataFrame(rows_array, columns=column_names)
        return df
    else:
        print('>>>>>> No result fetched!')


def add_qualifications_column(row, column):
    to_list = json.loads(row['listings'])
    to_string = to_list[column]['elements'][0]
    return to_string


def create_bag_of_words(dataset, column):
    # from nltk.stem.porter import PorterStemmer
    corpus = []
    for i in range(0, len(dataset)):
        job_description = re.sub('[^a-zA-Z]', ' ', dataset[column][i])
        job_description = job_description.lower()
        job_description = job_description.split()
        # ps = PorterStemmer()
        # job_description = [ps.stem(word) for word in job_description if not word in set(stopwords.words('english'))]
        job_description = [word for word in job_description if not word in set(stopwords.words('english'))]
        job_description = ' '.join(job_description)
        corpus.append(job_description)

    cv = CountVectorizer(max_features=100)
    X = cv.fit_transform(corpus).toarray()
    columns = cv.vocabulary_

    sorted_columns = sorted(columns.items(), key=operator.itemgetter(1))
    sorted_columns = [x[0] for x in sorted_columns]
    word_freq = pd.DataFrame(X, columns=sorted_columns)

    dataset_joined = dataset.join(word_freq)
    return dataset_joined


def main():
    conn = open_database_connection('postgres')
    amazonjobs_df = fetch_results_to_dataframe(conn, QUERY)
    conn.close()
    bag_of_words = create_bag_of_words(amazonjobs_df, 'listings')


if __name__ == '__main__':
    main()
