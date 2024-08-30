from Sim_Comp_Intrication import Von_Neumann_Entropy

def Distribute_Elements(generated_partitions, element) :

    # Browse partitons one by one
    for partition in generated_partitions :

        # Adds a new partition composed of the seed 
        # partiton + "element" : [[e1], [e2]] --> [[e1], [e2], [e3]]
        yield partition + [[element]]

        # Browse partitions' subsets
        for i, subset in enumerate(partition) :
            # Adds a partition composed of the subset + "element" :
            # [[e1], [e2]] --> [[e1, e3], [e2]]
            yield partition[:i]  +[subset + [element]] + partition[i+1:]

def Partition_Generator(elements) :
    # Creates a generator that browse partitions one by one
    generated_partitions = iter([[]])

    # Browse the elements of the list give as argument
    for el in elements :
        # Creates the generator that browse partitions of the ensemble e; = [e1, e2, ..., ei]
        generated_partitions = Distribute_Elements(generated_partitions, el)
    
    return generated_partitions

def Get_Nb_Qbit(state) :
    from math import log2
    return int(log2(len(state)))

def Element_Generator(state) :
    nb_qbits = Get_Nb_Qbit(state)
    elements = []

    for qb in range(nb_qbits) :
        elements.append(qb)
    
    return elements

def Von_Neumann_Partitions(state) :
    v_n_partitions = []
    elements = Element_Generator(state)
    generated_partitions = Partition_Generator(elements)
    for partition in generated_partitions :
        v_n_partition = []
        if len(partition) == 2 :
            sysA, sysB = partition[0], partition[1]
            if len(sysB) > len(sysA) :
                buffer = sysA
                sysA = sysB
                sysB = buffer
            v_n_e = Von_Neumann_Entropy(Get_Nb_Qbit(state), state, sysA, sysB)
            v_n_partition.append(sysA)
            v_n_partition.append(sysB)
            v_n_partition.append(v_n_e)
            v_n_partitions.append(v_n_partition)
    v_n_partitions.sort(reverse = True, key = lambda row: row[2][1])
    return v_n_partitions

def Display_Von_neumann_Partitions(state) :
    elements = Element_Generator(state)
    generated_partitions = Partition_Generator(elements)
    for partition in generated_partitions :
        if len(partition) == 2 :
            sysA, sysB = partition[0], partition[1]
            v_n_e = Von_Neumann_Entropy(get_nb_qbit(state), state, sysA, sysB)

            print("Sys A : ", sysA, "| Sys B : ", sysB, "-->", v_n_e)

def One_To_One_Partitions_Generator(elements) :
    one_to_one_partitions = []
    start = 0
    nb_elements = len(elements)
    while start < nb_elements :
        for i in range(start + 1, nb_elements) :
            one_to_one_partitions.append([[elements[start]], [elements[i]]])
        start = start + 1
    return one_to_one_partitions

def One_To_One_Von_Neumann(state) :
    v_n_one_to_one_partitions = []
    elements = Element_Generator(state)
    one_to_one_partitions = One_To_One_Partitions_Generator(elements)
    for partition in one_to_one_partitions :
        v_n_one_to_one_partition = []
        if len(partition) == 2 :
            sysA, sysB = partition[0], partition[1]
            v_n_e = Von_Neumann_Entropy(Get_Nb_Qbit(state), state, sysA, sysB)
            v_n_one_to_one_partition.append(sysA)
            v_n_one_to_one_partition.append(sysB)
            v_n_one_to_one_partition.append(v_n_e)
            v_n_one_to_one_partitions.append(v_n_one_to_one_partition)
    return v_n_one_to_one_partitions
#--------------------------------#