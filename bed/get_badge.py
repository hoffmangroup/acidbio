import tempfile
import webbrowser

from run_all import run_all
# Do some URL stuff to get the tool name
# .
# .
# .

# Pretend that <tool> is the name of a tool from the URL parser
tool = "ucsc"

# Temporary file to store results, won't be used.
trash_file = tempfile.NamedTemporaryFile()

# Whether it passes the threshold or not for each BED version
passing = [False for _ in range(11)]

for i in range(3, 13):
    num_correct, correct_list, name_list = run_all(
        "BED" + str(i).zfill(2), trash_file.name, tool
    )

    if (sum(num_correct) / len(num_correct)) / len(correct_list) >= 0.7:
        passing[i-3] = True

generated_url = "https://img.shields.io/badge/BED Parser-"
for i in range(10):
    if passing[i]:
        generated_url += "BED{} %7C".format(i+3)
generated_url = generated_url[:-4] + "-informational"
print(generated_url)
# In reality this would be a redirection to the generated badge
webbrowser.open(generated_url)