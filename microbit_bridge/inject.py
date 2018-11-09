from subprocess import call
import re, sys, os
from optparse import OptionParser
import tempfile
from shutil import copyfile

from intelhex import IntelHex, bin2hex, hex2bin
from io import StringIO

SCHOOL_ID = "B1TSC"
HUB_ID = "B1THu"

BUILD_FOLDER_PATH = "../build/bbc-microbit-classic-gcc/source/microbit-samples.hex"

package_directory = os.path.dirname(os.path.abspath(__file__))

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
                  default="./hub-final.hex",
                  help="Output file path")

parser.add_option("-c", "",
                  action="store_true",
                  dest="clean",
                  default=False,
                  help="Copy the latest hex file, and replace hub-not-combined.hex")

(options, args) = parser.parse_args()

"""
    Injects the given ids into a hex file and outputs it as a file (if given a path).

    @param new_school_id the new school id to replace in the hub hex file

    @param new_hub_id the new hub id to replace in the hub hex file

    @param output_file_path the output path (defaults to ./hub-final.hex), if not specified, the file will be returned

    @param clean defaults to False, if set to True, the latest hub-not-combined hex will be pulled from the build dir.
"""
def inject_ids(new_school_id, new_hub_id, output_file_path="", clean=False):

    if len(new_school_id) != len(SCHOOL_ID):
        print("New school id length (%d) must match the old (%d)" % (len(new_school_id), len(SCHOOL_ID)))
        return -1

    if len(new_hub_id) != len(HUB_ID):
        print("New hub id length (%d) must match the old (%d)" % (len(new_hub_id), len(HUB_ID)))
        return -1

    if clean:
        print("Removing old hub file.")
        os.remove(package_directory + "/hexes/hub-not-combined.hex")

    if not os.path.isfile(package_directory + "/hexes/hub-not-combined.hex"):
        try:
            print("Copying latest hub file from: %s" % BUILD_FOLDER_PATH)
            copyfile(BUILD_FOLDER_PATH, package_directory + "/hexes/hub-not-combined.hex")
        except Exception as e:
            print("hub-combined-hex not available")

    with tempfile.NamedTemporaryFile() as hub_not_combined_modified_hex_file, \
            tempfile.NamedTemporaryFile() as hub_not_combined_modified_bin_file, \
                tempfile.NamedTemporaryFile() as temp_out_file:

        # first convert the uncombined hex file into bin
        hex_as_bin = hex2bin(package_directory + "/hexes/hub-not-combined.hex", hub_not_combined_modified_bin_file.name)

        # replace the old ids with the new.
        print("Replacing ids.")
        bin_data = hub_not_combined_modified_bin_file.readlines()
        hub_not_combined_modified_bin_file.seek(0)

        school_id_changed = False
        hub_id_changed = False

        for l in bin_data:
            try:
                new_l = re.sub(bytes(SCHOOL_ID, 'utf-8'), bytes(new_school_id, 'utf-8'), l)
            except:
                new_l = re.sub(SCHOOL_ID, new_school_id, l)

            if new_l != l:
                school_id_changed = True

            try:
                final_l = re.sub(bytes(HUB_ID, 'utf-8'), bytes(new_hub_id,'utf-8'), new_l)
            except:
                final_l = re.sub(HUB_ID, new_hub_id, new_l)

            if final_l != new_l:
                hub_id_changed = True

            hub_not_combined_modified_bin_file.write(final_l)

        hub_not_combined_modified_bin_file.flush()

        if not school_id_changed:
            print("School id not found in bin!")
            exit(1)

        if not hub_id_changed:
            print("Hub id not found in bin!")
            exit(1)

        # then to hex
        print ("Creating final file: %s" % (output_file_path))
        bin2hex(hub_not_combined_modified_bin_file.name, hub_not_combined_modified_hex_file.name, 0x18000)
        replaced_hex = IntelHex(hub_not_combined_modified_hex_file.name)
        bootloader_hex = IntelHex(package_directory + "/hexes/BOOTLOADER.hex")
        softdevice_hex = IntelHex(package_directory + "/hexes/SOFTDEVICE.hex")

        replaced_hex.merge(bootloader_hex)
        replaced_hex.merge(softdevice_hex)

        # finally creating the final binary.
        if len(output_file_path):
            with open(output_file_path, 'w') as f:
                replaced_hex.write_hex_file(f.name)
                f.close()
                return 0
        else:
            sio = StringIO()
            replaced_hex.write_hex_file(sio)
            return sio.getValue()

if __name__ == '__main__':
    sys.exit(inject_ids(options.school_id, options.hub_id, options.output_file_path, options.clean))