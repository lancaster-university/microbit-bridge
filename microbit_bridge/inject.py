from subprocess import call
import re, sys, os
from optparse import OptionParser
import tempfile
from shutil import copyfile

SCHOOL_ID = "B1TSC"
HUB_ID = "B1THu"

BUILD_FOLDER_PATH = "../build/bbc-microbit-classic-gcc/source/microbit-samples.hex"

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
                  default="",
                  help="Output file path")

parser.add_option("-c", "",
                  action="store_true",
                  dest="clean",
                  default=False,
                  help="Copy the latest hex file, and replace hub-not-combined.hex")

(options, args) = parser.parse_args()

def inject_ids(new_school_id, new_hub_id, output_file_path, clean):

    if len(new_school_id) != len(SCHOOL_ID):
        print "New school id length (%d) must match the old (%d)" % (len(new_school_id), len(SCHOOL_ID))
        return -1

    if len(new_hub_id) != len(HUB_ID):
        print "New hub id length (%d) must match the old (%d)" % (len(new_hub_id), len(HUB_ID))
        return -1

    if clean:
        print "Removing old hub file."
        os.remove("./hub-not-combined.hex")

    if not os.path.isfile("./hub-not-combined.hex"):
        try:
            print "Copying latest hub file from: %s" % BUILD_FOLDER_PATH
            copyfile(BUILD_FOLDER_PATH, "./hub-not-combined.hex")
        except Exception as e:
            print "hub-combined-hex not available"

    with tempfile.NamedTemporaryFile() as hub_not_combined_modified_hex_file, \
            tempfile.NamedTemporaryFile() as hub_not_combined_modified_bin_file, \
                tempfile.NamedTemporaryFile() as temp_out_file:

        # first convert the uncombined hex file into uf2
        call(["python","hex2bin.py","./hub-not-combined.hex", hub_not_combined_modified_bin_file.name])

        # replace the old ids with the new.
        uf2 = hub_not_combined_modified_bin_file.readlines()
        hub_not_combined_modified_bin_file.seek(0)

        school_id_changed = False
        hub_id_changed = False

        for l in uf2:
            new_l = re.sub(SCHOOL_ID, new_school_id, l)

            if new_l != l:
                school_id_changed = True

            final_l = re.sub(HUB_ID, new_hub_id, new_l)

            if final_l != new_l:
                hub_id_changed = True

            hub_not_combined_modified_bin_file.write(final_l)

        hub_not_combined_modified_bin_file.flush()

        if not school_id_changed:
            print "School id not found in bin!"
            exit(1)

        if not hub_id_changed:
            print "Hub id not found in bin!"
            exit(1)

        # then to hex
        print "Creating final file: %s" % (output_file_path)
        call(["python","bin2hex.py", "--offset=0x18000", hub_not_combined_modified_bin_file.name, hub_not_combined_modified_hex_file.name])

        # finally creating the final binary.
        if len(output_file_path):
            call(["python","merge_hex.py","./BOOTLOADER.hex", "./SOFTDEVICE.hex", hub_not_combined_modified_hex_file.name, "-o" + output_file_path])
            return 0
        else:
            call(["python","merge_hex.py","./BOOTLOADER.hex", "./SOFTDEVICE.hex", hub_not_combined_modified_hex_file.name, "-o" + temp_out_file.name])

            temp_out_file.seek(0)
            return temp_out_file.readlines()

def generate_firmware(school_id, hub_id):
    return inject_ids(school_id, hub_id, "", False)

if __name__ == '__main__':
    sys.exit(inject_ids(options.school_id, options.hub_id, options.output_file_path, options.clean))