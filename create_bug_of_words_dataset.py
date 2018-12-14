'''
This module gets amazonjobs data from a local postgres database
and creates a bug of words.

sys.path.extend([
     'C:\\Users\\George\\PycharmProjects\\amazonjobs'
    ,'C:/Users/George/PycharmProjects/amazonjobs'])
PyDev console: starting.
Python 3.7.1 (default, Oct 23 2018, 22:56:47) [MSC v.1912 64 bit (AMD64)] on win32
'''
import json
import re
from datetime import datetime
import operator
import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import psycopg2

QUERY = """select * from amazon.amazonjobs_2;"""


def open_database_connection(database):
    '''
    Opens connection with database
    :param database: database name
    :return: connection
    '''
    conn = None
    if database == 'postgres':
        dbname, user, host, password = 'postgres', 'postgres', 'localhost', 'postgres'
    else:
        print("No database selected")
    try:
        conn = psycopg2.connect(
            "host=%(host)s "
            "user=%(user)s "
            "password=%(password)s "
            "dbname=%(dbname)s"
            % {
                'host': host,
                'user': user,
                'password': password,
                'dbname': dbname
            }
        )
        print('>>>>>> Database connected successfully')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def fetch_results_to_dataframe(conn, query):
    '''
    Executes query and transforms results to dataframe
    :param conn: connection
    :param query: QUERY
    :return: dataframe
    '''
    try:
        cur = conn.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        rows = cur.fetchall()
        print('>>>>>> Result fetched')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if rows and rows[0][0] is not None:
        rows_array = np.array(rows)
        to_df = pd.DataFrame(rows_array, columns=column_names)
        print('>>>>>> Result transformed to dataframe')
    else:
        print('No result fetched!')
    return to_df


def add_qualifications_column(row, column):
    '''
    Not sure what this does as it is not used anywhere!
    :param row:
    :param column:
    :return:
    '''
    to_list = json.loads(row['listings'])
    to_string = to_list[column]['elements'][0]
    return to_string


def create_bag_of_words(dataset, column):
    '''
    Create bag of words
    :param dataset: dataframe
    :param column: dataframe column to be analyzed
    :return: bag of words as dataframe
    '''
    corpus = []
    for i in range(0, len(dataset)):
        job_description = re.sub('[^a-zA-Z]', ' ', dataset[column][i])
        job_description = job_description.lower()
        job_description = job_description.split()
        job_description = [
            word for word in job_description if not word in set(
                stopwords.words('english')
            )
        ]
        job_description = ' '.join(job_description)
        corpus.append(job_description)

    count_vectorizer = CountVectorizer(max_features=100)
    to_array = count_vectorizer.fit_transform(corpus).toarray()
    columns = count_vectorizer.vocabulary_

    sorted_columns = sorted(columns.items(), key=operator.itemgetter(1))
    sorted_columns = [x[0] for x in sorted_columns]
    word_freq = pd.DataFrame(to_array, columns=sorted_columns)

    dataset_joined = dataset.join(word_freq)
    return dataset_joined


def main():
    '''
    :return: bag of words printed
    '''
    script_start_time = datetime.now()
    conn = open_database_connection('postgres')
    amazonjobs_df = fetch_results_to_dataframe(conn, QUERY)
    conn.close()
    bag_of_words = create_bag_of_words(amazonjobs_df, 'listings')
    print(bag_of_words.head(20))
    print(">>>>>> Executed in %s seconds" % (datetime.now() - script_start_time))


if __name__ == '__main__':
    main()
