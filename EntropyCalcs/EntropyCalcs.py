import collections
import io
import sys
import matplotlib.pyplot as plt
from scipy.stats import entropy


def calc_shannon_entropy(data):
    bases = collections.Counter([temp_base for temp_base in data])
    distribution = [x / sum(bases.values()) for x in bases.values()]
    entropy_value = entropy(distribution, base=2)

    return entropy_value


def diplay_entropy(thefile, chunk_size=700):
    srtpt, endpt = 0x0, 0x0
    counter = 0
    chunk_values = []
    chunk_indranges = []
    chunk_ent_values = []

    with open(thefile, 'rb') as file:
        data = file.read()

    for index, value in enumerate(data):

        value_in_hex = ('0x%02x' % value)
        chunk_values.append(value_in_hex)
        counter += 1
        if counter == chunk_size:
            endpt = index
            chunk_indranges.append('0x%08x 0x%08x' % (srtpt, endpt))
            chunk_ent_values.append(calc_shannon_entropy(chunk_values))
            srtpt = endpt + 1
            counter = 0
            chunk_values = []

    fig = plt.figure(figsize=(16, 4.5))
    plt.plot(chunk_indranges, chunk_ent_values, color='green', marker='o')
    plt.xlim([0, 100])
    plt.xticks(rotation=90)
    plt.title('Entropy for each ' + str(chunk_size) + ' Bytes chunk')
    plt.xlabel('Chunks Range')
    plt.ylabel('Entropy')
    plt.show()

    return chunk_indranges, chunk_ent_values


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) > 1:
        if arguments[1] in ['help', '--help', '-help', '-h', '--h']:
            print('python -f filename -c chunksize_in_Bytes:default:700')

        elif len(arguments) == 3 and arguments[1] == '-f':
            print('python -f filename -c 700')
            if arguments[2] and isinstance(arguments[2], str):
                diplay_entropy(arguments[2])
        elif len(arguments) == 5 and arguments[1] == '-f' and arguments[3] == '-c':
            print('python -f filename -c ' + str(arguments[4]))
            if arguments[2] and isinstance(arguments[2], str) and arguments[4]:
                try:
                    arguments[4] = int(arguments[4])
                except ValueError:
                    print("The chunk size should be an integer number")
                    sys.exit(1)
                diplay_entropy(arguments[2], arguments[4])
        else:
            print("Usage: python -f filename -c chunksize_in_Bytes:default:700")
