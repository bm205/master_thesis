import master_thesis.config as config
from master_thesis.processing import Processer


if __name__ == "__main__":
    # num_of_tax = input("Enter number of taxonomies, either 1, 2, or 4:")
    # print("Username is: " + num_of_tax)
    if config.NUMRER_OF_TAXONOMIES == 4:
        print("TAX_1 = cm, TAX_2 = pcs, TAX_3 = drg, TAX_4 = hcpcs")
        print("Weights: 0.25 each")
        Processer.process_4_tax()

    elif config.NUMRER_OF_TAXONOMIES == 1:
        print('1 Taxonomy')
        Processer.process_1_tax()

    elif config.NUMRER_OF_TAXONOMIES == 2:
        print('2 Taxonomies')
        print(f'weights: {config.WEIGHTS[0]}:{config.WEIGHTS[1]}')
        Processer.process_2_tax()

    else:
        print("That is not a proper number. Please insert 1, 2 or 4.")
    
