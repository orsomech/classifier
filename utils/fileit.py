
def write_to_file(file_name, input):
    try:
        with open(f'/Users/ors/PycharmProjects/classifier/{file_name}', mode='w') as f:
            f.write(input)
    finally:
        i = 0