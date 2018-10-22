from subprocess import call
import re, sys
from optparse import OptionParser

SCHOOL_ID = "ABCDEFGHIJKL"
HUB_ID = "ABCDEFGHIJKL"

parser = OptionParser()

#command line options
parser.add_option("", "--school-id",
                  action="store",
	              type="string",
                  dest="school_id",
                  default="",
                  help="The new school id to splice into the hub hex file")

parser.add_option("", "--hub-id",
                  action="store",
	              type="string",
                  dest="hub_id",
                  default="",
                  help="The new hub id to splice into the hub hex file")

(options, args) = parser.parse_args()

def inject_ids(NEW_SCHOOL_ID, NEW_HUB_ID):

    if len(NEW_SCHOOL_ID) != len(SCHOOL_ID):
        print "New school id length must much the old: size %d" % len(SCHOOL_ID)
        return -1

    if len(NEW_HUB_ID) != len(HUB_ID):
        print "New hub id length must much the old: size %d" % len(HUB_ID)
        return -1

    # first convert the uncombined hex file into uf2
    call(["python","uf2conv.py","./hub-not-combined.hex", "-o", "./hub-not-combined.uf2"])

    # replace the old ids with the new.
    with open("./hub-not-combined.uf2", "r+") as f:
        uf2 = f.readlines()
        f.seek(0)

        for l in uf2:
            new_l = re.sub(SCHOOL_ID, NEW_SCHOOL_ID, l)
            new_l = re.sub(HUB_ID, NEW_HUB_ID, new_l)
            f.write(new_l)

        f.close()

    # convert to bin
    print "Converting back from uf2..."
    call(["python","uf2conv.py","./hub-not-combined.uf2", "-o", "./hub-not-combined-modified.bin"])

    # then to hex
    print "Creating final hub.hex..."
    call(["python","bin2hex.py", "--offset=0x18000", "./hub-not-combined-modified.bin", "./hub-not-combined-modified.hex"])

    # finally creating the final binary.
    call(["python","merge_hex.py","./BOOTLOADER.hex", "./SOFTDEVICE.hex", "./hub-not-combined-modified.hex", "-o./hub.hex"])

    print "Cleaning up..."
    call(["rm", "./hub-not-combined-modified.hex", "./hub-not-combined-modified.bin", "./hub-not-combined.uf2"])

if __name__ == '__main__':
    sys.exit(inject_ids(options.school_id, options.hub_id))

# call
# call(["sed -i -E 's/(THIS_IS_THE_UNIQUE_SCHOOL_ID)/\1POOP/' ./hub.uf2"])
# call(["sed", "-i", "-E", "'s/THIS_IS_THE_UNIQUE_SCHOOL_ID/POOP/'","./hub.uf2"])

# os.remove("./hub.uf2")