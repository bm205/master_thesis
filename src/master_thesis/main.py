import master_thesis.config as config
from master_thesis.processing import Processer


if __name__ == "__main__":
    # num_of_tax = input("Enter number of taxonomies, either 1, 2, or 4:")
    # print("Username is: " + num_of_tax)

    if not all(x in ['cm', 'pcs', 'drg', 'hcpcs'] for x in config.TAXONOMIES):
        raise ValueError('Wrong taxonomy name. One of the names is not a proper taxonomy name. Please fix it in the config file for TAXONOMIES.')

    if len(config.TAXONOMIES) == 1:
        if all(x in ['cm', 'pcs', 'drg', 'hcpcs'] for x in config.TAXONOMIES):
            print('1 Taxonomy')
            Processer.process_1_tax_train()
            
    elif len(config.TAXONOMIES) == 2:
        if all(x in ['cm', 'pcs', 'drg', 'hcpcs'] for x in config.TAXONOMIES):
            print('2 Taxonomies')
            print(f'weights: {config.WEIGHTS[0]}:{config.WEIGHTS[1]}')
            Processer.process_2_tax_new()
    
    elif len(config.TAXONOMIES) == 4:
        if all(x in ['cm', 'pcs', 'drg', 'hcpcs'] for x in config.TAXONOMIES):
            print('4 Taxonomies')
            print("TAX_1 = cm, TAX_2 = pcs, TAX_3 = drg, TAX_4 = hcpcs")
            print("Weights: 0.25 each")
            Processer.process_4_tax()

    else:
        raise ValueError("Wrong number of taxonomies. Please insert 1, 2 or 4 taxonomy names in the config file for TAXONOMIES.")
