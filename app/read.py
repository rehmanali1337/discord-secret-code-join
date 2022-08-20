
def read_txt_lines(file: str):
    lines = open(file, encoding="UTF-8").readlines()
    return [line.strip() for line in lines if line.strip() != ""]
