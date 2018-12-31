# K-Means Clustering

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

# Importing the dataset
dataset = pd.read_csv(
        'C:\\Users\\vn689xm\\BOW_title_1000.tsv'
        , sep = '\t'
        , encoding='utf-8'
        )
X = dataset.iloc[:, 11:263].values
#X_columns = dataset.iloc[:, [11, 12]].columns

# Kmeans
# Using the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 20):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 20), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Fitting K-Means to the dataset
kmeans = KMeans(n_clusters = 12, init = 'k-means++', random_state = 42)
y_data = kmeans.fit_predict(X)

# HC
# Using the dendrogram to find the optimal number of clusters
import scipy.cluster.hierarchy as sch
dendrogram = sch.dendrogram(sch.linkage(X, method = 'ward'))
plt.title('Dendrogram')
plt.xlabel('Customers')
plt.ylabel('Euclidean distances')
plt.show()

# Fitting Hierarchical Clustering to the dataset
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters = 8, affinity = 'euclidean', linkage = 'ward')
y_data = hc.fit_predict(X)

# Add clusters to initial dataset
clusters = np.asarray(y_data)
dataset['cluster'] = clusters
amazonjobs_df = dataset.iloc[:, 1:11]
amazonjobs_df['cluster'] = clusters

# Export results to tsv
import os
amazonjobs_df.to_csv('Results_.tsv', sep='\t', encoding='utf-8')
print('>>>>>> Result exported: ' + f'{os.getcwd()}\Results_.tsv')
