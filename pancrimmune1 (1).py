# -*- coding: utf-8 -*-
"""PancrImmune1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PF2ymotZpVHHwilHzbLs6w8Om769qvpW
"""

!pip install viper-in-python scanpy anndata pandas numpy

import pandas as pd
import os

# Set data paths
data_location = "/Users/lzy/Desktop/"
metadata_file = os.path.join(data_location, "PancrImmune1-metadata.tsv")
modified_metadata_file = os.path.join(data_location, "PancrImmune1-metadata_modified.tsv")

# Check if the file exists
def check_file(file_path):
    if os.path.exists(file_path):
        print(f"{file_path} exists.")
    else:
        print(f"Error: {file_path} does not exist.")

# Check the original file
check_file(metadata_file)

# Read the metadata file
metadata = pd.read_csv(metadata_file, sep='\t', header=None, low_memory=False)
print(f"Original metadata rows: {len(metadata)}")

# Remove the extra row (assuming the extra row is at the beginning or end)
metadata = metadata.drop(metadata.index[0])  # Remove the first row; if it's the last row, use metadata.drop(metadata.index[-1])
print(f"Modified metadata rows: {len(metadata)}")

# Save the modified metadata file
metadata.to_csv(modified_metadata_file, sep='\t', index=False, header=False)

# Check the modified file
check_file(modified_metadata_file)

# View basic information about the metadata and clustering data
metadata.info()
clusters.info()

# Check for missing values
print(metadata.isnull().sum())
print(clusters.isnull().sum())

import pyviper
import scanpy as sc
import anndata
import pandas as pd
import numpy as np
import random
import warnings

warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")  # for jit decorator issue with sc.pp.neighbors

# Set data paths
data_location = "/Users/lzy/Desktop/"
matrix_file = data_location + "expression_matrix.mtx.gz"
metadata_file = data_location + "PancrImmune1-metadata_modified.tsv"  # Use the modified metadata file
cluster_file = data_location + "PancrImmune1-cluster.tsv"

# Read gene expression signature
gene_expr_signature = sc.read_mtx(matrix_file).T  # Transpose matrix to have cells as rows and genes as columns
barcodes = pd.read_csv(metadata_file, header=None, sep='\t')
features = pd.read_csv(cluster_file, header=None, sep='\t')

# Add barcodes and gene information
gene_expr_signature.obs['barcode'] = barcodes[0].values
gene_expr_signature.var['gene'] = features[1].values
gene_expr_signature.var_names = gene_expr_signature.var['gene']
gene_expr_signature.obs_names = gene_expr_signature.obs['barcode']

print(gene_expr_signature)

# Compute nearest neighbors
sc.pp.neighbors(gene_expr_signature, n_neighbors=10)

# Compute UMAP
sc.tl.umap(gene_expr_signature)

# Plot UMAP
sc.pl.umap(gene_expr_signature, color=['donor', 'sex', 'cell_type__ontology_label'])

# Cluster using Leiden algorithm
sc.tl.leiden(gene_expr_signature, resolution=0.1)

# Plot clustering result
sc.pl.umap(gene_expr_signature, color='leiden')



