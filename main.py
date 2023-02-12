from pandas.core.window.common import defaultdict
import itertools as iter


item_counts = defaultdict(int)
pair_counts = defaultdict(int)
with open("C:\\Users\\ACER\\Downloads\\Illinois Classes\\CS412\\Project 1\\categories.txt") as f:
    lines = f.readlines()
freq = 772


def get_1_itemset():  # get all frequent one itemsets from files with semicolon being the seperator between entries
    for line in lines:
        line = line.replace("\n", "")
        for item in line.split(";"):
            item_counts[item] += 1
    return item_counts


def frequent_1items():  # generate frequent 1-itemsets by remmoving any sets with frequency less than frequency
    frequent = defaultdict(int)
    itemset = get_1_itemset()
    for item in itemset:
        if itemset[item] > freq:
            frequent[item] = itemset[item]
    return frequent


def print_itemsets(itemsets):  # Print items to file
    with open("C:\\Users\\ACER\\Downloads\\Illinois Classes\\CS412\\patterns2.txt", 'w') as file:
        for dictionary in itemsets:
            for j, v in dictionary.items():
                file.write(f"{v}:{j}\n")


def last_dict_not_empty(list_of_dictionaries, dict_index):  # check if the last itemset list is empty
    return bool(list_of_dictionaries[dict_index])


def find_candidates(itemset_list, new_dictionary):  # find the k-itemset candidates from k-1 itemsets
    last_dict_index = len(itemset_list) - 1
    last_dict = itemset_list[last_dict_index]
    for itemset1 in last_dict:
        for itemset2 in last_dict:
            if itemset1 == itemset2:
                continue
            if type(itemset1) is str:
                new_candidate = tuple((itemset1,) + (itemset2,))
            else:
                new_candidate = compare_and_join(itemset1, itemset2)
            if new_candidate is not None:
                if has_infrequenet_subsets(last_dict, new_candidate):
                    continue
                else:
                    new_dictionary[tuple(sorted(new_candidate))]
    return new_dict


def compare_and_join(itemset_1, itemset_2):  # compare the items and if they are equal, except the last
    # item in the second combination, generate a new itemset combination
    item_size = len(itemset_1)
    counter = 0
    while counter != item_size:
        if counter == item_size - 1:
            new_itemset = itemset_1 + (itemset_2[item_size - 1],)
            return new_itemset
        if itemset_1[counter] != itemset_2[counter]:
            break
        counter += 1
    return None


def has_infrequenet_subsets(last_list, candidate_itemset):  # check that all k-1 itemset combinations of the candidate
    # are frequent
    combo_length = len(candidate_itemset) - 1
    k_minus1_candidates = list(iter.combinations(candidate_itemset, combo_length))
    for x in k_minus1_candidates:
        if len(x) == 1:
            if x[0] not in last_list:
                return True
        else:
            x = tuple(sorted(x))
            if x not in last_list:
                return True
    return False


def count_occurances(new_list, size):  # count the occurrences of itemsets by scanning database and increasing the
    # corresponding dictionary item for the itemset
    transaction_items = list()
    for line in lines:
        line = line.replace("\n", "")
        for item in line.split(";"):
            transaction_items.append(item)
        line_candidates = (tuple(iter.combinations(sorted(transaction_items), size)))
        for i in new_list:
            if i in line_candidates:
                new_list[i] += 1
        transaction_items = list()


def delete_infrequet(items_list, frequency):  # delete infrequent items from the new k-itemset list
    clean_list = defaultdict(int)
    for i in items_list:
        if items_list[i] < frequency:
            continue
        else:
            clean_list[i] = items_list[i]
    return clean_list


if __name__ == '__main__':
    list_of_dicts = list()
    one_itemsets = frequent_1items()
    list_of_dicts.append(one_itemsets)
    k = 1
    while last_dict_not_empty(list_of_dicts, k-1):
        # while the last itemset is not empty, get the k-itemset
        new_dict = defaultdict(int)
        new_dict = find_candidates(list_of_dicts, new_dict)
        count_occurances(new_dict, k+1)
        new_dict = delete_infrequet(new_dict, freq)
        list_of_dicts.append(new_dict)
        k += 1
    print(list_of_dicts)
    print(f"File contains {len(list_of_dicts[0])} frequent 1-itemsets, {len(list_of_dicts[1])} frequent 2-itemsets, "
          f"and {len(list_of_dicts[2])} frequent 3-itemsets")
