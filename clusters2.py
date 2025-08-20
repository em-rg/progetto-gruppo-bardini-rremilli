import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path, encoding='latin1')
    # Remove rows with missing CustomerID
    df_clean = df.dropna(subset=['CustomerID'])
    # Remove negative quantities (returns)
    df_clean = df_clean[df_clean['Quantity'] > 0]
    # Remove negative unit prices
    df_clean = df_clean[df_clean['UnitPrice'] > 0]
    # Convert InvoiceDate to datetime
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    # Create TotalAmount column
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    return df_clean

def compute_rfm_features(df_clean):
    latest_date = df_clean['InvoiceDate'].max()
    rfm = df_clean.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (latest_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',  # Frequency
        'TotalAmount': 'sum'  # Monetary = Customer Lifetime Value
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'CLV']

    # Numero totale di acquisti
    num_orders = df_clean.groupby('CustomerID')['InvoiceNo'].nunique().reset_index(name='NumOrders')
    # Quantità totale acquistata
    total_quantity = df_clean.groupby('CustomerID')['Quantity'].sum().reset_index(name='TotalQuantity')
    # Spesa media
    avg_order_value = df_clean.groupby('CustomerID')['TotalAmount'].mean().reset_index(name='AvgOrderValue')
    # Frequenza di acquisto mensile
    customer_lifetime = df_clean.groupby('CustomerID')['InvoiceDate'].agg(lambda x: (x.max() - x.min()).days + 1 if len(x) > 1 else 1).reset_index(name='CustomerLifetime')
    purchase_freq_monthly = num_orders.copy()
    purchase_freq_monthly['PurchaseFrequencyMonthly'] = purchase_freq_monthly['NumOrders'] / (customer_lifetime['CustomerLifetime'] / 30)
    purchase_freq_monthly['PurchaseFrequencyMonthly'] = purchase_freq_monthly['PurchaseFrequencyMonthly'].clip(upper=30)

    # Paese di appartenenza (one hot encoding)
    customer_country = df_clean.groupby(['CustomerID', 'Country']).size().reset_index(name='CountryCount')
    customer_country = customer_country.sort_values(['CustomerID', 'CountryCount'], ascending=[True, False])
    customer_country = customer_country.drop_duplicates('CustomerID')
    customer_country = customer_country[['CustomerID', 'Country']]
    country_dummies = pd.get_dummies(customer_country['Country'], prefix='Country')
    customer_country = pd.concat([customer_country[['CustomerID']], country_dummies], axis=1)

    # Merge di tutte le feature
    features = rfm.merge(num_orders, on='CustomerID')
    features = features.merge(total_quantity, on='CustomerID')
    features = features.merge(avg_order_value, on='CustomerID')
    features = features.merge(purchase_freq_monthly[['CustomerID', 'PurchaseFrequencyMonthly']], on='CustomerID')
    features = features.merge(customer_country, on='CustomerID')

    return features

def scale_features(features, method='standard', handle_outliers=True):
    features_for_clustering = ['Recency', 'Frequency', 'CLV', 'TotalQuantity', 'AvgOrderValue', 'PurchaseFrequencyMonthly']
    X = features[features_for_clustering].copy()
    
    # Handle outliers if specified - cap values at 99th percentile
    if handle_outliers:
        for col in X.columns:
            cap_value = X[col].quantile(0.99)
            X[col] = X[col].clip(upper=cap_value)
    
    # Apply scaling
    if method == 'standard':
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=features_for_clustering)
        return X_scaled_df
    elif method == 'minmax':
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=features_for_clustering)
        return X_scaled_df
    elif method == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=features_for_clustering)
        return X_scaled_df
    else:
        raise ValueError("method must be 'standard', 'minmax', or 'robust'")

def get_preprocessed_data(file_path="Online_Retail.csv", scaling_method='standard'):
    df_clean = load_and_clean_data(file_path)
    customer_features = compute_rfm_features(df_clean)
    X_scaled_df = scale_features(customer_features, method=scaling_method)
    return customer_features, X_scaled_df

##Cluster 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import pandas as pd
import os
import numpy as np

# Ottieni il percorso assoluto del file CSV
file_path = os.path.join(os.path.dirname(__file__), "Online_Retail.csv")

# Carica e scala i dati con diversi metodi di scaling
# Utilizzando tre diversi metodi di scaling per confronto
customer_features, X_standard_scaled = get_preprocessed_data(file_path=file_path, scaling_method='standard')
_, X_minmax_scaled = get_preprocessed_data(file_path=file_path, scaling_method='minmax')
_, X_robust_scaled = get_preprocessed_data(file_path=file_path, scaling_method='robust')

# Confronto dei metodi di scalatura
X_scaled_df = X_robust_scaled  # Usa RobustScaler per default perché gestisce meglio gli outlier

# Analisi correlazione tra feature
plt.figure(figsize=(12, 10))
corr_matrix = X_scaled_df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlazione tra feature dopo scalatura')
plt.tight_layout()
plt.savefig('feature_correlation.png')
plt.show()

# Identificazione feature altamente correlate (>0.7) che possono influenzare il clustering
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

# Determinazione numero ottimale di cluster (Elbow Method e Silhouette Score)

inertia = []
sil_scores = []
K_range = range(2, 11)

# Valutazione del numero ottimale di cluster usando solo l'inertia e il Silhouette Score
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled_df)
    inertia.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_scaled_df, labels))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('n_clusters')
plt.ylabel('Inertia')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(K_range, sil_scores, marker='o')
plt.title('Silhouette Score (higher is better)')
plt.xlabel('n_clusters')
plt.ylabel('Silhouette Score')
plt.grid(True)

plt.tight_layout()
plt.savefig('cluster_evaluation.png')
plt.show()

# Scegli il numero di cluster ottimale basato sul Silhouette Score
best_k = K_range[sil_scores.index(max(sil_scores))]

# Risultati ottimali secondo il Silhouette Score
# Silhouette Score (più alto è meglio): valori più alti indicano cluster meglio separati

# KMeans clustering con best_k e più inizializzazioni per stabilità
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=20, max_iter=500)
kmeans_labels = kmeans.fit_predict(X_scaled_df)

# Valuta la qualità del clustering
silhouette_avg = silhouette_score(X_scaled_df, kmeans_labels)

# La qualità del clustering è determinata da:
# - Silhouette Score: (valori più alti indicano cluster ben separati, range: -1 a 1)

# Ottimizzazione dei parametri DBSCAN
from sklearn.neighbors import NearestNeighbors

# Determine optimal eps parameter using k-distance graph
neighbors = NearestNeighbors(n_neighbors=10)
neighbors_fit = neighbors.fit(X_scaled_df)
distances, indices = neighbors_fit.kneighbors(X_scaled_df)
distances = np.sort(distances[:, 9])  # 10th nearest neighbor

plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.title('K-distance Graph (k=10)')
plt.xlabel('Points sorted by distance')
plt.ylabel('Distance to 10th nearest neighbor')
plt.grid(True)
# Find elbow point approximately
elbow_index = np.argmax(distances[1:] - distances[:-1]) + 1 if len(distances) > 1 else 0
optimal_eps = distances[elbow_index]
plt.axhline(y=optimal_eps, color='r', linestyle='--', 
            label=f'Optimal eps ≈ {optimal_eps:.2f}')
plt.legend()
plt.savefig('dbscan_kdistance_plot.png')
plt.show()

# DBSCAN clustering con parametri ottimizzati
dbscan = DBSCAN(eps=optimal_eps, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled_df)

# Conteggio dei cluster e dei punti rumore
n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

# Riduzione dimensionale per visualizzazione
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_df)
# PCA permette di visualizzare i cluster in 2D

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

# Analisi dei cluster KMeans
clustered = customer_features.copy()
clustered['Cluster'] = kmeans_labels

# Statistiche medie per cluster
cluster_stats = clustered.groupby('Cluster')[['Recency', 'Frequency', 'CLV', 'TotalQuantity', 'AvgOrderValue', 'PurchaseFrequencyMonthly']].mean()

# Calcola statistiche dettagliate per ogni feature e cluster
cluster_detailed_stats = {}
for feature in ['Recency', 'Frequency', 'CLV', 'TotalQuantity', 'AvgOrderValue', 'PurchaseFrequencyMonthly']:
    feature_stats = {}
    for cluster in range(best_k):
        cluster_data = clustered[clustered['Cluster'] == cluster][feature]
        feature_stats[cluster] = {
            'mean': cluster_data.mean(),
            'median': cluster_data.median(),
            'min': cluster_data.min(),
            'max': cluster_data.max(),
            'percentile_25': cluster_data.quantile(0.25),
            'percentile_75': cluster_data.quantile(0.75)
        }
    cluster_detailed_stats[feature] = feature_stats

# Analisi più dettagliata dei cluster
# Identificazione cluster: abituali, occasionali, alto valore, ecc.
features_importance = {
    'Recency': {'low': 'recenti', 'high': 'non recenti', 'weight': 0.8},
    'Frequency': {'low': 'bassa frequenza', 'high': 'alta frequenza', 'weight': 0.9},
    'CLV': {'low': 'basso valore', 'high': 'alto valore', 'weight': 1.0},
    'PurchaseFrequencyMonthly': {'low': 'acquisti rari', 'high': 'acquisti frequenti', 'weight': 0.7},
    'AvgOrderValue': {'low': 'spesa media bassa', 'high': 'spesa media alta', 'weight': 0.8},
    'TotalQuantity': {'low': 'pochi prodotti', 'high': 'molti prodotti', 'weight': 0.6}
}

# Interpretazione avanzata dei cluster (KMeans)
cluster_descriptions = {}
cluster_profiles = {}

# Calcola i percentili per ogni feature per una classificazione più robusta
percentiles = {}
for feature in features_importance.keys():
    percentiles[feature] = {
        'low': cluster_stats[feature].quantile(0.33),
        'high': cluster_stats[feature].quantile(0.67)
    }

# Categorizza ogni cluster in base ai suoi valori relativi
for idx, row in cluster_stats.iterrows():
    profile = []
    scores = {
        'recency': 0,
        'frequency': 0,
        'value': 0
    }
    
    # Analizza ogni feature
    for feature, importance in features_importance.items():
        val = row[feature]
        if feature == 'Recency':  # Per Recency, valori più bassi sono migliori
            if val < percentiles[feature]['low']:
                profile.append(importance['low'])
                scores['recency'] += importance['weight']
            elif val > percentiles[feature]['high']:
                profile.append(importance['high'])
                scores['recency'] -= importance['weight']
        else:  # Per altre feature, valori più alti sono migliori
            if val > percentiles[feature]['high']:
                profile.append(importance['high'])
                if feature in ['Frequency', 'PurchaseFrequencyMonthly']:
                    scores['frequency'] += importance['weight']
                if feature in ['CLV', 'AvgOrderValue']:
                    scores['value'] += importance['weight']
            elif val < percentiles[feature]['low']:
                profile.append(importance['low'])
                if feature in ['Frequency', 'PurchaseFrequencyMonthly']:
                    scores['frequency'] -= importance['weight']
                if feature in ['CLV', 'AvgOrderValue']:
                    scores['value'] -= importance['weight']
    
    # Categorizzazione in tipi di clienti standard
    description = []
    if scores['frequency'] > 1.0 and scores['recency'] > 0.5:
        description.append("Clienti abituali")
    if scores['frequency'] < -1.0 and scores['recency'] < -0.5:
        description.append("Clienti occasionali")
    if scores['value'] > 1.0:
        description.append("Clienti ad alto valore")
    if scores['value'] < -1.0:
        description.append("Clienti a basso valore")
    if scores['frequency'] > 0 and scores['value'] > 0 and scores['recency'] > 0:
        description.append("Clienti fedeli")
    if scores['frequency'] < 0 and scores['value'] > 0.8:
        description.append("Grandi acquirenti sporadici")
    
    # Se nessuna categoria specifica è stata assegnata
    if not description:
        if scores['frequency'] > 0:
            description.append("Clienti attivi")
        elif scores['value'] > 0:
            description.append("Clienti di valore medio")
        else:
            description.append("Clienti standard")
    
    # Salva il profilo completo e la descrizione
    cluster_profiles[idx] = ", ".join(profile)
    cluster_descriptions[idx] = ", ".join(description)


# Aggiungi le descrizioni al dataframe
clustered['Cluster_Description'] = clustered['Cluster'].map(cluster_descriptions)

# Analisi geografica per cluster
country_cols = [col for col in customer_features.columns if col.startswith('Country_')]
geo_stats = clustered.groupby('Cluster')[country_cols].mean()


# Evidenzia cluster con forte presenza in un paese
for cluster_id, row in geo_stats.iterrows():
    top_country = row.idxmax()


# Visualizzazioni avanzate
import seaborn as sns
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

# 1. Analisi distribuzione delle feature per cluster
plt.figure(figsize=(20, 12))
features_to_plot = ['Recency', 'Frequency', 'CLV', 'AvgOrderValue', 'PurchaseFrequencyMonthly', 'TotalQuantity']

for i, feature in enumerate(features_to_plot):
    plt.subplot(2, 3, i+1)
    for cluster in range(best_k):
        sns.kdeplot(clustered[clustered['Cluster'] == cluster][feature], 
                   label=f'Cluster {cluster}: {cluster_descriptions[cluster]}')
    plt.title(f'Distribuzione di {feature} per cluster')
    plt.legend()
plt.tight_layout()
plt.savefig('cluster_distributions.png')
plt.show()

# 2. Box plot delle feature per cluster
plt.figure(figsize=(20, 15))
for i, feature in enumerate(features_to_plot):
    plt.subplot(2, 3, i+1)
    sns.boxplot(x='Cluster', y=feature, data=clustered)
    plt.title(f'Box plot di {feature} per cluster')
plt.tight_layout()
plt.savefig('cluster_boxplots.png')
plt.show()

# 3. Scatter plot matrice per le feature principali con colori per cluster
selected_features = ['Recency', 'Frequency', 'CLV']
sns.pairplot(clustered[selected_features + ['Cluster']], 
            hue='Cluster', 
            palette='tab10',
            height=3)
plt.suptitle('Matrice di scatter plot per le feature principali', y=1.02)
plt.savefig('cluster_pairplot.png')
plt.show()

# 4. Radar Chart per visualizzare il profilo di ogni cluster
from math import pi

# Prepara i dati per il radar chart
radar_df = cluster_stats.copy()
radar_df = (radar_df - radar_df.min()) / (radar_df.max() - radar_df.min())  # Normalizza 0-1
categories = list(radar_df.columns)
N = len(categories)

# Angoli per il radar chart
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # Chiudi il cerchio

# Prepara la figura
plt.figure(figsize=(15, 10))

# Colori per i cluster
colors = plt.cm.tab10(np.linspace(0, 1, best_k))

# Crea un subplot per ogni cluster
for i, cluster in enumerate(radar_df.index):
    ax = plt.subplot(2, (best_k+1)//2, i+1, polar=True)
    values = radar_df.loc[cluster].values.tolist()
    values += values[:1]  # Chiudi il cerchio
    
    # Disegna il poligono e riempilo
    ax.plot(angles, values, color=colors[i], linewidth=2)
    ax.fill(angles, values, color=colors[i], alpha=0.25)
    
    # Etichette
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title(f'Cluster {cluster}: {cluster_descriptions[cluster]}', size=11)
    
    # Y labels
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels(["0.25", "0.50", "0.75"])
    ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('cluster_radar_charts.png')
plt.show()

# 5. Visualizzazione 3D con PCA a 3 componenti
from mpl_toolkits.mplot3d import Axes3D

# Applica PCA con 3 componenti
pca3d = PCA(n_components=3)
X_pca3d = pca3d.fit_transform(X_scaled_df)

# Crea la figura
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Visualizza i punti
scatter = ax.scatter(X_pca3d[:, 0], X_pca3d[:, 1], X_pca3d[:, 2], 
                    c=kmeans_labels, cmap='tab10', s=30, alpha=0.7)

# Aggiungi una legenda
legend_handles = []
for i in range(best_k):
    legend_handles.append(mpatches.Patch(color=plt.cm.tab10(i/10), 
                                         label=f'Cluster {i}: {cluster_descriptions[i]}'))
ax.legend(handles=legend_handles, loc='best')

# Etichette
ax.set_xlabel('PCA 1')
ax.set_ylabel('PCA 2')
ax.set_zlabel('PCA 3')
ax.set_title('Visualizzazione 3D dei cluster con PCA')

plt.savefig('cluster_3d_pca.png')
plt.show()

# 6. Distribuzione geografica
# Seleziona i primi N paesi più rappresentati
top_n_countries = 10
top_countries = geo_stats.mean().sort_values(ascending=False).head(top_n_countries).index

plt.figure(figsize=(15, 8))
heatmap_data = geo_stats[top_countries].T
sns.heatmap(heatmap_data, annot=True, cmap='YlOrRd', fmt='.2f')
plt.title(f'Distribuzione dei top {top_n_countries} paesi per cluster')
plt.ylabel('Paese')
plt.xlabel('Cluster')
plt.savefig('cluster_country_heatmap.png')
plt.show()

# Esporta i risultati in CSV
clustered.to_csv('Online_Retail_clustered.csv', index=False)

# Genera un report testuale
report = f"""
# REPORT ANALISI CLUSTERING CLIENTI ONLINE RETAIL

## Sommario
- Numero di clienti analizzati: {len(clustered)}
- Numero ottimale di cluster (K-Means): {best_k} (determinato dal Silhouette Score: {silhouette_avg:.3f})
- Metodo di scaling utilizzato: RobustScaler
- Feature utilizzate per il clustering: Recency, Frequency, CLV, TotalQuantity, AvgOrderValue, PurchaseFrequencyMonthly

## Descrizione dei Cluster

"""

for cluster_id in range(best_k):
    cluster_size = (clustered['Cluster'] == cluster_id).sum()
    cluster_percent = cluster_size / len(clustered) * 100
    
    report += f"### Cluster {cluster_id}: {cluster_descriptions[cluster_id]}\n"
    report += f"- Dimensione: {cluster_size} clienti ({cluster_percent:.1f}% del totale)\n"
    report += f"- Caratteristiche principali:\n"
    
    for feature in ['Recency', 'Frequency', 'CLV', 'AvgOrderValue', 'PurchaseFrequencyMonthly', 'TotalQuantity']:
        avg_value = cluster_stats.loc[cluster_id, feature]
        overall_avg = cluster_stats[feature].mean()
        diff_percent = (avg_value - overall_avg) / overall_avg * 100
        
        if diff_percent > 20:
            status = "MOLTO SOPRA"
        elif diff_percent > 5:
            status = "SOPRA"
        elif diff_percent < -20:
            status = "MOLTO SOTTO"
        elif diff_percent < -5:
            status = "SOTTO"
        else:
            status = "NELLA MEDIA"
            
        report += f"  - {feature}: {avg_value:.2f} ({status} la media di {overall_avg:.2f}, {diff_percent:.1f}%)\n"
    
    # Aggiungi informazioni geografiche
    top_country = geo_stats.loc[cluster_id].idxmax().replace('Country_', '')
    top_country_value = geo_stats.loc[cluster_id].max()
    report += f"- Paese principale: {top_country} ({top_country_value:.2f})\n\n"

# Definisci la directory corrente per i file di output
output_dir = os.path.dirname(__file__)

# Salva il report in un file di testo
report_path = os.path.join(output_dir, 'cluster_analysis_report.txt')
with open(report_path, 'w') as f:
    f.write(report)

# Salva il dataset con i cluster
clustered_csv_path = os.path.join(output_dir, 'Online_Retail_clustered.csv')
clustered.to_csv(clustered_csv_path, index=False)

# Salva i modelli per uso futuro
import joblib
kmeans_model_path = os.path.join(output_dir, 'kmeans_model.pkl')
joblib.dump(kmeans, kmeans_model_path)
# - {kmeans_model_path} (modello KMeans salvato)


# Profili dei cluster identificati:
for cluster_id in range(best_k):
    cluster_size = (clustered['Cluster'] == cluster_id).sum()
    cluster_percent = cluster_size / len(clustered) * 100
    # Cluster {cluster_id} ({cluster_percent:.1f}%): {cluster_descriptions[cluster_id]}