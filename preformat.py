import subprocess as sb

def process(filenames):
    sb.call("chmod +rwx script_format.sh",shell=True)
    sb.call("chmod +rwx script_format_per_file.sh",shell=True)
    sb.call("chmod +rwx clean.sh",shell=True)
    sb.call("./script_format.sh",shell=True)
