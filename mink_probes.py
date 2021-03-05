from Bio import Seq, SeqIO

def kmers(s, k):
    return set([s[i:i+k] for i in range(len(s)-(k-1))])

def find_probe(kmers_list):
    first_kmer = kmers_list.pop(0)
    result = first_kmer.difference(*kmers_list)
    kmers_list.append(first_kmer)
    if len(result) != 0:
        return result.pop()
    else:
        return None


def min_k_probes(fasta_file_name):
    seq_generator=SeqIO.parse(open(fasta_file_name),"fasta")
    sequence_list = list(s.seq for s in seq_generator)
    queries = len(sequence_list)
    max_mer_length = len(min(sequence_list, key=len))
    temporary_result_list = []
    l = 0
    p = max_mer_length - 1
    mer_leangth =(l+p)//2
    final_result_list = []
    final_mer_k = max_mer_length

    while(l < p):
        print(f"Szukam {mer_leangth}-merów")
        kmer_list_of_sets = []
        temporary_result_list = []
        for i in range(queries):
            kmer_list_of_sets.append(kmers(sequence_list[i], mer_leangth))
        for i in range(queries):
            probe = find_probe(kmer_list_of_sets)
            if probe == None:
                break
            else:
                temporary_result_list.append(probe.reverse_complement())
        if (len(temporary_result_list) < queries):
            print("Sonda nie istnieje")
            l = mer_leangth + 1
            mer_leangth = (l+p)//2
        else:
            print("Sonda instnieje")
            if mer_leangth < final_mer_k:
                final_mer_k = mer_leangth
                final_result_list = temporary_result_list
            p = mer_leangth
            mer_leangth = (l+p)//2
    return final_result_list

print(min_k_probes('test_fasta.fa'))
