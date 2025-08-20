import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

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

def scale_features(features, method='standard'):
    features_for_clustering = ['Recency', 'Frequency', 'CLV', 'TotalQuantity', 'AvgOrderValue', 'PurchaseFrequencyMonthly']
    X = features[features_for_clustering]
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
    else:
        raise ValueError("method must be 'standard' or 'minmax'")

def remove_outliers(features, X_scaled_df, outlier_fraction=0.05):
    # Calcola la distanza euclidea dal centroide
    centroid = X_scaled_df.mean(axis=0)
    distances = np.linalg.norm(X_scaled_df - centroid, axis=1)
    threshold = np.percentile(distances, 100 * (1 - outlier_fraction))
    mask = distances <= threshold
    # Filtra sia features che X_scaled_df
    return features[mask].reset_index(drop=True), X_scaled_df[mask].reset_index(drop=True)

def get_preprocessed_data(file_path="Online_Retail.csv", scaling_method='standard'):
    df_clean = load_and_clean_data(file_path)
    customer_features = compute_rfm_features(df_clean)
    X_scaled_df = scale_features(customer_features, method=scaling_method)
    # Rimuovi il 5% dei dati più outlier
    customer_features, X_scaled_df = remove_outliers(customer_features, X_scaled_df, outlier_fraction=0.05)
    return customer_features, X_scaled_df


