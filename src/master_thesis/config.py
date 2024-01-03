# Write the taxonomies preferred from these taxonomies: 'cm','pcs','drg','hcpcs'
# TAXONOMIES = ['cm','pcs','drg','hcpcs']
TAXONOMIES = ['cm','pcs','drg']


# =================
# Choose number of IC,CS,SS
# =================
# IC = [1,2]
IC = 1
# CS = [1,2]
CS = 2
# SS = [1,2,3,4]
SS = 4


# ==================
# WEIGHTS in order of: 'cm' ,'pcs', 'drg','hcpcs'. Only one of all the below should be uncommented.
# ==================
# When there are 2 taxonomies (TAX_1:TAX_2). Uncomment one of them only:
# WEIGHTS = [0.8,0.2]
# WEIGHTS = [0.5,0.5]
# WEIGHTS = [0.2,0.8]
# WEIGHTS = customized (put any 3 ratios which sum to 1)
# ==================
# When there are 3 taxonomies (TAX_1:TAX_2:TAX_3). Uncomment one of them only:
# WEIGHTS = [0.33,0.33,0.33]
WEIGHTS = [0.5,0.25,0.25]
# WEIGHTS = [0.25,0.25,0.5]
# WEIGHTS = [0.25,0.5,0.25]
# WEIGHTS = customized (put any 3 ratios which sum to 1)
# ==================
# When there are 4 taxonomies (CM:PCS:DRG:HCPCS). Uncomment one of them only:
# WEIGHTS = [0.25,0.25,0.25,0.25]
# WEIGHTS = customized (put any 3 ratios which sum to 1)
# ==================


# ========================
# K in k-NN , uncomment one of the options
# ========================
# Find K using Cross Validation:
K = 'CV'
# Find K using Rule of Thumb (square root of the sample size):
# K = 'RoT'
