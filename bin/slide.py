import sys, os, base64, requests

source_path = os.path.dirname(os.path.realpath(__file__))
call_path = os.getcwd()

def to_bytes(image_path):
    if image_path[:4] == "http":
        image = requests.get(image_path).content
    else:
        with open(image_path, "rb") as f:
            image = f.read()
    return base64.b64encode(image).decode("utf-8")

def img_type(image_path):
    extension = image_path.rsplit(".", 1)[1]
    if extension in ["jpeg", "jpg"]: return "jpeg"
    elif extension == "png": return "png"
    elif extension == "gif": return "gif"
    elif extension == "bmp": return "bmp"
    elif extension == "svg": return "svg"

# Replaces images and adds tabs
def format_lines(input_lines):
    output = []
    for line in input_lines:
        if len(line)>0 and line[0] == "@":
            image_path = line[1:]
            image_type = img_type(image_path.strip())
            image_text = to_bytes(image_path.strip())
            line = '<img src="data:image/%s;base64,%s">\n' % (image_type, image_text)
        output.append("\t\t\t" + line)
    return output

def main():
    with open(sys.argv[1], "r") as input:
        formatted = "".join(format_lines(input.readlines()))
    with open(os.path.join(source_path, "template.html"), "r") as template:
        result = template.read().replace("{{ CONTENT }}", formatted)
    with open(sys.argv[2], "w+") as output:
        output.write(result)

if __name__ == '__main__':
    main()