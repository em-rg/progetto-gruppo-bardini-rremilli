import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from preprocessing import get_preprocessed_data
import pandas as pd

# Carica e scala i dati
customer_features, X_scaled_df = get_preprocessed_data(scaling_method='standard')

# Determinazione numero ottimale di cluster (Elbow Method e Silhouette Score)
inertia = []
sil_scores = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled_df)
    inertia.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_scaled_df, labels))

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(K_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('n_clusters')
plt.ylabel('Inertia')

plt.subplot(1,2,2)
plt.plot(K_range, sil_scores, marker='o')
plt.title('Silhouette Score')
plt.xlabel('n_clusters')
plt.ylabel('Silhouette Score')
plt.tight_layout()
#plt.show()

print("Silhouette scores per k:", dict(zip(K_range, sil_scores)))

# Scegli il numero di cluster migliore (ad esempio quello con silhouette score massimo)
best_k = K_range[sil_scores.index(max(sil_scores))]
print(f"Best number of clusters by silhouette score: {best_k}")

# KMeans clustering con best_k
kmeans = KMeans(n_clusters=best_k, random_state=42)
kmeans_labels = kmeans.fit_predict(X_scaled_df)

# DBSCAN clustering
dbscan = DBSCAN(eps=2, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled_df)

# Riduzione dimensionale per visualizzazione
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_df)

# Visualizza KMeans
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.scatter(X_pca[:,0], X_pca[:,1], c=kmeans_labels, cmap='tab10', s=10)
plt.title('KMeans Clustering')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')

# Visualizza DBSCAN
plt.subplot(1,2,2)
plt.scatter(X_pca[:,0], X_pca[:,1], c=dbscan_labels, cmap='tab10', s=10)
plt.title('DBSCAN Clustering')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')

plt.tight_layout()
plt.show()

# Confronto risultati
print("KMeans cluster counts:", pd.Series(kmeans_labels).value_counts())
print("DBSCAN cluster counts:", pd.Series(dbscan_labels).value_counts())

# Analisi dei cluster KMeans
clustered = customer_features.copy()
clustered['Cluster'] = kmeans_labels

# Statistiche medie per cluster
cluster_stats = clustered.groupby('Cluster')[['Recency', 'Frequency', 'CLV', 'TotalQuantity', 'AvgOrderValue', 'PurchaseFrequencyMonthly']].mean()
print("\nCluster statistics (KMeans):")
print(cluster_stats)

# Identificazione cluster: abituali, occasionali, alto valore
# - Clienti abituali: alta Frequency, alta PurchaseFrequencyMonthly, bassa Recency
# - Clienti occasionali: bassa Frequency, bassa PurchaseFrequencyMonthly, alta Recency
# - Clienti alto valore: alta CLV, alta AvgOrderValue

print("\nCluster interpretation (KMeans):")
for idx, row in cluster_stats.iterrows():
    print(f"Cluster {idx}: ", end="")
    if row['Frequency'] > cluster_stats['Frequency'].mean() and row['PurchaseFrequencyMonthly'] > cluster_stats['PurchaseFrequencyMonthly'].mean():
        print("Clienti abituali", end=", ")
    if row['Frequency'] < cluster_stats['Frequency'].mean() and row['Recency'] > cluster_stats['Recency'].mean():
        print("Clienti occasionali", end=", ")
    if row['CLV'] > cluster_stats['CLV'].mean() and row['AvgOrderValue'] > cluster_stats['AvgOrderValue'].mean():
        print("Clienti ad alto valore", end=", ")
    print()

# Analisi geografica per cluster
country_cols = [col for col in customer_features.columns if col.startswith('Country_')]
geo_stats = clustered.groupby('Cluster')[country_cols].mean()
print("\nDistribuzione geografica media per cluster (KMeans):")
print(geo_stats)

# Evidenzia cluster con forte presenza in un paese
for cluster_id, row in geo_stats.iterrows():
    top_country = row.idxmax()
    print(f"Cluster {cluster_id} ha la maggiore presenza media in: {top_country.replace('Country_', '')}")
