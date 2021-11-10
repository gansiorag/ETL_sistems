
"""
This module make

Author Gansior Alexandr mail - gansior@gansior.ru tel - +79173383804
"""

def count_bits_1(n):
    num_bits=0
    yy = bin(abs(n))
    for k in yy:
        if k == '1': num_bits +=1
    return num_bits


def count_bits(n,sim):
    return n.count(sim)


if __name__ == '__main__':
    print(count_bits('asdsaasdf','as'))

