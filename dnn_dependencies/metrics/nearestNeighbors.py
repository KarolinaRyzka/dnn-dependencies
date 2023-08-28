import sqlite3
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

np.random.seed(42)

# get all rows from database
conn = sqlite3.connect(database="models.db")
df: DataFrame = pd.read_sql("SELECT * FROM scores", conn)
conn.close()

conn2 = sqlite3.connect(database="example.db")
df.to_sql(
    name="Model Stats", con=conn2, if_exists="replace", index=True, index_label="ID"
)
conn2.execute("ALTER TABLE Model Stats ADD PRIMARY KEY (ID);")
conn2.close()

df2: DataFrame = pd.read_sql("SELECT * FROM example", conn)


metadataDF: DataFrame = df[["Model Name", "Model Filepath"]]

df.drop(columns=["Model Name", "Model Filepath"], inplace=True)
print(len(df))

# unsupervised nearest neighbors

nearestNeighbors = NearestNeighbors(
    n_neighbors=df.shape[0], algorithm="kd_tree", metric="euclidean"
).fit(X=df)

distances, indices = nearestNeighbors.kneighbors([df.iloc[1667]])
# Print the results
print("Nearest Neighbors and their Distances for bert:")
for i in range(len(indices[0])):
    neighborIndex = indices[0][i]
    distance = distances[0][i]
    print(f"Model Index: {neighborIndex}, Distance: {distance}")


quit()
pca = PCA(n_components=3)
transformedX = pca.fit_transform(X=df)


# print(pca.get_feature_names_out(transformedX))


kmeans = KMeans(n_clusters=30, n_init="auto")
labels = kmeans.fit_predict(X=transformedX)

pca_components = pca.components_


# Plot the data points
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(
    transformedX[:, 0],
    transformedX[:, 1],
    transformedX[:, 2],
    c=labels,
    cmap="viridis",
    edgecolor="k",
    s=50,
)

ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_zlabel("Principal Component 3")
ax.set_title("K-Means Clustering with PCA (3 Components)")
plt.legend()
plt.show()
plt.show()
