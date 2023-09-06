import os
import datetime
import random
from argparse import ArgumentParser


def uid():

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as YEAR-MONTH-DAY-HOUR:MINUTE:SECOND
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

    # Generate 4 random digits
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))

    # Combine the formatted datetime with the random digits
    return f"{formatted_datetime}_{random_digits}"

def execute(cmd):
    print("->      Running command: " + cmd)
    return os.system(cmd)


parser = ArgumentParser()
parser.add_argument("--src", required=True, help="Path to source code")
parser.add_argument("--dest", required=True, help="Destination path of copied code")
parser.add_argument("--exp-name", required=True, help="Experiment name")
parser.add_argument("-v", "--volume", action='append', help="Volumes to be attached to the running container. Docker format.")

args = parser.parse_args()
src_path = args.src

uid = uid()
exp_name = os.path.join(args.exp_name,uid) if args.exp_name else str(uid)
dest_path = os.path.join(args.dest, exp_name)
if dest_path.endswith("/"):
    dest_path = dest_path[:-1]
dest_image_name = f"{args.exp_name}:{uid}"

volumes = args.volume

def parse_volumes(vols):
    return " ".join([f"-v {v}" for v in vols])

# COPY code from some folder
cmd = f"cp -fr {src_path} {dest_path}"
execute(cmd)
# build docker container based on the copied folder
execute(f"cd {dest_path}; docker build -t {dest_image_name} .")
# run this container with mounted data volumes
execute(f"docker run -it  {parse_volumes(volumes)} {dest_image_name}")
