from subprocess import call
import re, sys
from optparse import OptionParser
import tempfile

SCHOOL_ID = "M1cR0B1TSCHO"
HUB_ID = "M1cR0B1THuBs"

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

parser.add_option("", "--output-file",
                  action="store",
                  type="string",
                  dest="output_file_path",
                  default="./hub.hex",
                  help="Output file path")

(options, args) = parser.parse_args()

def inject_ids(new_school_id, new_hub_id, output_file_path):

    if len(new_school_id) != len(SCHOOL_ID):
        print "New school id length must much the old: size %d" % len(SCHOOL_ID)
        return -1

    if len(new_hub_id) != len(HUB_ID):
        print "New hub id length must much the old: size %d" % len(HUB_ID)
        return -1

    with tempfile.NamedTemporaryFile() as hub_not_combined_modified_hex_file, \
            tempfile.NamedTemporaryFile() as hub_not_combined_modified_bin_file, \
            tempfile.NamedTemporaryFile() as hub_not_combined_uf2_file:

        # first convert the uncombined hex file into uf2
        call(["python","uf2conv.py","./hub-not-combined.hex", "-o", hub_not_combined_uf2_file.name])

        # replace the old ids with the new.
        uf2 = hub_not_combined_uf2_file.readlines()
        hub_not_combined_uf2_file.seek(0)

        for l in uf2:
            new_l = re.sub(SCHOOL_ID, new_school_id, l)
            new_l = re.sub(HUB_ID, new_hub_id, new_l)
            hub_not_combined_uf2_file.write(new_l)

        # convert to bin
        print "Converting back from uf2..."
        call(["python","uf2conv.py",hub_not_combined_uf2_file.name, "-o", hub_not_combined_modified_bin_file.name])

        # then to hex
        print "Creating final file: %s" % (output_file_path)
        call(["python","bin2hex.py", "--offset=0x18000", hub_not_combined_modified_bin_file.name, hub_not_combined_modified_hex_file.name])

        # finally creating the final binary.
        call(["python","merge_hex.py","./BOOTLOADER.hex", "./SOFTDEVICE.hex", hub_not_combined_modified_hex_file.name, "-o" + output_file_path])

if __name__ == '__main__':
    sys.exit(inject_ids(options.school_id, options.hub_id, options.output_file_path))