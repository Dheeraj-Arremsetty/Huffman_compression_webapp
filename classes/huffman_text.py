from collections import defaultdict
import Tree
import heapq
import pickle
import pdb
import os
from PIL import Image

# import word_cloud
LEFT_CODE = "0"
RIGHT_CODE = "1"
HEAP_DATA = []
type = "word"
tree = defaultdict(str)
input_file_name = 'input_file.txt'

frequency = {}
huff_codes = {}  # defaultdict(list)
huff_code_to_value = {}
_data = ""
size = 0


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def read_image(input_file_path):
    input_file_path = "./input/umsltritons-logo.jpg"
    global size
    global _data
    im = Image.open(input_file_path, 'r')
    size = im.size
    pix_val = list(im.getdata())
    pix_val_flat = [x for sets in pix_val for x in sets]

    _data = pix_val_flat
    for val in pix_val_flat:
        frequency[val] = frequency.get(val, 0) + 1

    # _data = pix_val
    # for rgb in pix_val:
    #     frequency[rgb] = frequency.get(rgb, 0) + 1

    all_characters_data = sorted(frequency.items(), key=lambda x: x[1])
    # print all_characters_data
    return all_characters_data


def read_image2(input_file_path):
    import base64
    global _data, _all_data
    with open(input_file_path, "rb") as imageFile:
        _data = base64.b64encode(imageFile.read())
        print _data
    _all_data = _data
    _data = _data
    # dividing images into chunks
    _data = [val for val in chunks(_data, 40)]
    for character in _data:
        frequency[character] = frequency.get(character, 0) + 1

    all_characters_data = sorted(frequency.items(), key=lambda x: x[1])
    print all_characters_data
    return all_characters_data


def read_file(input_file_path):
    input_file_name = input_file_path
    global _data
    _file = open(input_file_name, 'r')
    _data = _file.read().rstrip()

    for character in _data:
        frequency[character] = frequency.get(character, 0) + 1

    all_characters_data = sorted(frequency.items(), key=lambda x: x[1])
    # print all_characters_data
    return all_characters_data


def read_file_words(input_file_path):
    input_file_name = input_file_path
    global _data
    _file = open(input_file_name, 'r')
    _data = _file.read().rstrip()
    _data = _data.split(" ")
    _count_words = 0
    for word in _data:
        frequency[word] = frequency.get(word, 0) + 1
        _count_words += 1
    frequency[" "] = int(_count_words)

    all_characters_data = sorted(frequency.items(), key=lambda x: x[1])
    # print all_characters_data
    return all_characters_data


def update_all_list_items(k1, k2, value):
    for key in huff_codes:
        if key not in [k1, k2]:
            # huff_codes[key].append(value)
            huff_codes[key] = [value] + huff_codes[key]


def build_0_1_sequence(root, sequence=""):
    if (root == None):
        return

    if (root.data[0] != None):
        huff_codes[root.data[0]] = sequence
        huff_code_to_value[sequence] = root.data[0]
        return

    if root.left.data[0] in huff_codes:
        return
    build_0_1_sequence(root.left, sequence + "0")
    if root.right.data[0] in huff_codes:
        return
    build_0_1_sequence(root.right, sequence + "1")


def create_tree_2(all_characters_data):
    for data in all_characters_data:
        node = Tree.Tree((data[0], data[1]))
        heapq.heappush(HEAP_DATA, node)

    while len(HEAP_DATA) > 1:
        node1 = heapq.heappop(HEAP_DATA)
        node2 = heapq.heappop(HEAP_DATA)

        new_node = Tree.Tree((None, node1.data[1] + node2.data[1]))
        new_node.left = node1
        new_node.right = node2

        heapq.heappush(HEAP_DATA, new_node)

    root_node = heapq.heappop(HEAP_DATA)
    build_0_1_sequence(root_node)


codes = {}


def str_to_byte(encoded_str):
    byte_array = bytearray()
    for i in range(0, len(encoded_str), 8):
        byte = encoded_str[i:i + 8]
        byte_array.append(int(byte, 2))
    return byte_array


def get_text_encoded():
    encoded_string = ""
    for character in _data:
        temp = "".join(huff_codes[character])
        huff_code_to_value[temp] = character
        if type == "word":
            encoded_string = encoded_string + huff_codes[" "] + temp
        else:
            encoded_string = encoded_string + temp
    return encoded_string


def compress(output_path, filename):
    output_file_path = output_path + filename + ".bin"
    encoded_string = get_text_encoded()
    encoded_string += "0" * (8 - len(encoded_string) % 8)
    encoded_string = str_to_byte(encoded_string)
    with open(output_file_path, 'wb') as output_file:
        output_file.write(bytes(encoded_string))
    file_size = os.path.getsize(output_file_path)
    return file_size


"""DECOMPRESS"""


def decode_str(encoded_text):
    huffman_bits = ""
    if type == "image":
        uncoded_str = ""
    else:
        uncoded_str = ""

    for bit in encoded_text:
        huffman_bits += bit
        if huff_code_to_value.get(huffman_bits, False) != False:
            uncoded_str += huff_code_to_value[huffman_bits]
            huffman_bits = ""

    return uncoded_str


def decompress(path="", file_name=""):
    print "*************************Decompressing***************************"
    bits_array = ""
    input_path = path + "/DECRYPT/" + file_name  # + ".bin"
    if type == "word":
        output_path = path + "/DECRYPT/output" + ".txt"
    else:
        output_path = path + "/DECRYPT/output" + ".jpg"

    with open(input_path, 'rb') as file, open(output_path, 'w') as output:

        byte = file.read(1)
        while (byte != ""):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bits_array += bits
            byte = file.read(1)

        encoded_text = bits_array
        decode_text = decode_str(encoded_text)
        if type == "word":
            output.write(decode_text)
            return output_path

        if type == "image":
            fh = open(output_path, "wb")
            fh.write(decode_text.decode('base64'))
            fh.close()
            return output_path
    print("Decompressed")


def write_data_for_word_cloud(folder_path):
    _sorted_data = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:200]
    '''
    {u'data': [{u'text': u'study', u'size': 40}, {u'text': u'motion', u'size': 15}, {u'text': u'forces', u'size': 100}]}
    '''
    _list = [{'text': item[0], 'size': item[1] * 10} for item in _sorted_data]

    word_cloud_data = {"data": _list}
    return word_cloud_data


def write_huffman_object(file_path):
    global huff_code_to_value
    file_name = "/object.pickle"

    with open(file_path + file_name, 'wb') as handle:
        pickle.dump(huff_code_to_value, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_huffman_object(file_path):
    global huff_code_to_value
    file_name = "/ENCRYPT/object.pickle"
    with open(file_path + file_name, 'rb') as handle:
        huff_code_to_value = pickle.load(handle)


def start(input_file_path, output_path="./output/", filename="output", run_type="word", mode="encrypt", uuid="",
          folder_path="", data_path=""):
    global type
    type = run_type
    stats = {}
    if mode == "encrypt":
        if type == "word":
            all_characters_data = read_file_words(input_file_path)
            huff_code_to_value[uuid] = "word"
        elif type == "image":
            all_characters_data = read_image2(input_file_path)
            huff_code_to_value[uuid] = "image"
        else:
            all_characters_data = read_file(input_file_path)
            huff_code_to_value[uuid] = "character"
        create_tree_2(all_characters_data)
        file_size = compress(output_path, filename)
        stats["file_size"] = file_size
        write_huffman_object(output_path)
        word_cloud_data = write_data_for_word_cloud(folder_path + "/" + uuid)
        stats["word_cloud_data"] = word_cloud_data
        return stats
    else:
        read_huffman_object(input_file_path)
        type = huff_code_to_value[uuid]

        if type == "image":
            print "imageimageimageimageimageimageimageimageimageimageimageimageimageimageimageimage"
            return decompress(input_file_path, filename)
        else:
            return decompress(input_file_path, filename)

# start("./input/input_file.txt")
# start("./input/umsltritons-logo.jpg",run_type="image")
