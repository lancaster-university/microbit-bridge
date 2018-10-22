from subprocess import call

build_path = "./build/bbc-microbit-classic-gcc/source/microbit-samples.hex"

call(["cp", build_path, "./hub-not-combined.hex"])

