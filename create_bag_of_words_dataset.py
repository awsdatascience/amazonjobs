'''
This module gets amazonjobs data from a local postgres database
and creates a bug of words.
Python 3.7.1 (default, Oct 23 2018, 22:56:47) [MSC v.1912 64 bit (AMD64)] on win32
import sys
sys.path.extend(
    [
     ''
     ,'C:\\Users\\vn689xm\\AppData\\Local\\conda\\conda\\envs\\amazonjobs\\python37.zip'
     ,'C:\\Users\\vn689xm\\AppData\\Local\\conda\\conda\\envs\\amazonjobs\\DLLs'
     ,'C:\\Users\\vn689xm\\AppData\\Local\\conda\\conda\\envs\\amazonjobs\\lib'
     ,'C:\\Users\\vn689xm\\AppData\\Local\\conda\\conda\\envs\\amazonjobs'
     ,'C:\\Users\\vn689xm\\AppData\\Local\\conda\\conda\\envs\\amazonjobs\\lib\\site-packages'
     ])
'''
import re
import os
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

# USER SPECIFIED PARAMETERS / REQUIRES INPUT
WORD_ACTIONS = pd.DataFrame([
    {'column_name': 'listings'
        , 'exclude_words': [
        "slsh"
        , "type"
        , "qualifications"
        , "elements"
        , "back"
        , "br"
        , "preferred"
        , "years"
        , "ability"
        , "experience"]
        , 'include_only_words': [
        "machinelearning"
        , "datamodeling"
        , "datawarehouse"
        , "bigdata"
        , "computerscience"
        , "python"
        , "java"
        , "scala"
        , "sql"
        , "excel"
        , "hadoop"
        , "rtech"
    ]
        , 'replace_string': [
        "machine learning"
        , "data modeling"
        , "data warehouse"
        , "big data"
        , "computer science"
    ]
     },
    {'column_name': 'role_description'
        , 'exclude_words': []
        , 'include_only_words': []
        , 'replace_string': []
     },
    {'column_name': 'title'
        , 'exclude_words': []
        , 'include_only_words': []
        , 'replace_string': []
     }
])


def open_database_connection(database):
    '''
    Opens connection with database
    :param database: database name
    :return: connection
    '''
    conn = None
    if database == 'postgres':
        dbname, user, host, password = 'postgres', 'postgres', 'localhost', '123'
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


def create_bag_of_words(dataset, column, max_features, exclude):
    '''
    Create bag of words
    :param dataset: dataframe
    :param column: dataframe column to be analyzed
    :param max_features: max columns of bag of words
    :param exclude: if true excludes words specified in WORD_ACTIONS['exclude_words']
        and if false includes only words specified in WORD_ACTIONS['includes_only_words']
    :return: bag of words as dataframe
    '''

    def apply_word_rules(list_of_words, exclude):
        '''
        Apply rules on list of words
        :param list_of_words:
        :param total_words_excluded:
        :param exclude: same as in create_bag_of_words()
        :return: list of words after rules applied
        '''
        list_of_words_rules_applied = list_of_words
        if exclude:
            if not WORD_ACTIONS.loc[
                WORD_ACTIONS['column_name'] == column, ['exclude_words']].values[0][0]:
                pass
            else:
                words_excluded = WORD_ACTIONS.loc[WORD_ACTIONS['column_name'] == column, ['exclude_words']
                ].values[0][0]
                list_of_words_rules_applied = [word for word in list_of_words if not word in set(words_excluded)]
        else:
            if not WORD_ACTIONS.loc[
                WORD_ACTIONS['column_name'] == column, ['include_only_words']].values[0][0]:
                pass
            else:
                words_included = WORD_ACTIONS.loc[WORD_ACTIONS['column_name'] == column, ['include_only_words']
                ].values[0][0]
                list_of_words_rules_applied = [word for word in list_of_words if word in set(words_included)]
        return list_of_words_rules_applied

    def replace_string(row):
        string_replaced = row
        if not WORD_ACTIONS.loc[
            WORD_ACTIONS['column_name'] == column, ['replace_string']].values[0][0]:
            pass
        else:
            list_of_words_to_merge = WORD_ACTIONS.loc[
                WORD_ACTIONS['column_name'] == column, ['replace_string']].values[0][0]
            for word in list_of_words_to_merge:
                merged = word.replace(' ', '')
                string_replaced = string_replaced.replace(word, merged)
        return string_replaced

    corpus = []
    for i in range(0, len(dataset)):
        # keeps only small and capital letters
        row = re.sub('[^a-zA-Z]', ' ', dataset[column][i])
        row = row.lower()
        row = row.replace(' r ', ' rtech ')
        # row = row.replace(' _string_ ', ' _newstring_ ')
        row = replace_string(row)
        row = row.split()
        row = [word for word in row if not word in set(stopwords.words('english'))]
        row = apply_word_rules(row, exclude)
        row = ' '.join(row)
        corpus.append(row)

    # excludes sinlge letter words as 'R' 
    count_vectorizer = CountVectorizer(max_features=max_features)
    to_array = count_vectorizer.fit_transform(corpus).toarray()
    columns = count_vectorizer.vocabulary_

    sorted_columns = sorted(columns.items(), key=operator.itemgetter(1))
    sorted_columns = [x[0] for x in sorted_columns]
    word_freq = pd.DataFrame(to_array, columns=sorted_columns)

    dataset_joined = dataset.join(word_freq)

    dataset_joined.to_csv(f'BOW_{column}_{max_features}.tsv'
                          , sep='\t', encoding='utf-8')
    print('>>>>>> Result exported: ' + f'{os.getcwd()}\BOW_{column}_{max_features}.tsv')
    return dataset_joined


def main():
    '''
    :return: bag of words printed
    '''
    script_start_time = datetime.now()
    conn = open_database_connection('postgres')
    amazonjobs_df = fetch_results_to_dataframe(conn, QUERY)
    conn.close()
    # USER SPECIFIED PARAMETERS / REQUIRES INPUT
    bag_of_words = create_bag_of_words(amazonjobs_df, 'listings', 10, exclude=False)
    print(bag_of_words.head(20))
    print(">>>>>> Executed in %s seconds" % (datetime.now() - script_start_time))


if __name__ == '__main__':
    main()
