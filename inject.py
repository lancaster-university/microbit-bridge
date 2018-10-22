from subprocess import call
import re

call(["python","uf2conv.py","./hub-not-combined.hex", "-o", "./hub-not-combined.uf2"])

SCHOOL_ID = "THIS_IS_THE_UNIQUE_SCHOOL_ID"
NEW_SCHOOL_ID = "ABCD_12_456_POOQUE_SCHOOL_ID"
HUB_ID = "THIS_IS_THE_UNIQUE_HUB_ID"
NEW_HUB_ID = "THIS_IS_THE_UNIQUE_HUB_ID"

print "Replacing previous school_id: %s with: %s" % (SCHOOL_ID, NEW_SCHOOL_ID)
call(["sed","-i","s/"+SCHOOL_ID+"/"+NEW_SCHOOL_ID+"/", "./hub-not-combined.uf2"])

print "Replacing previous hub_id: %s with: %s" % (HUB_ID, NEW_HUB_ID)
call(["sed","-i","s/"+HUB_ID+"/"+NEW_HUB_ID+"/", "./hub-not-combined.uf2"])

# with open("./hub.uf2", "r+") as f:
#     uf2 = f.readlines()

#     new_lines = []
#     for l in uf2:
#         l = re.sub(SCHOOL_ID, "\1"+NEW_SCHOOL_ID, l)
#         new_lines += [l]
#     # uf2 = re.sub(SCHOOL_ID, "\1"+NEW_SCHOOL_ID, uf2)
#     # uf2 = re.sub(HUB_ID, "\1"+NEW_HUB_ID, uf2)

#     with open("./hub-test.uf2", "w") as f2:
#         f2.writelines(new_lines)

print "Converting back from uf2..."
call(["python","uf2conv.py","./hub-not-combined.uf2", "-o", "./hub-not-combined-modified.bin"])

print "Creating final hub.hex..."
call(["python","bin2hex.py", "--offset=0x18000", "./hub-not-combined-modified.bin", "./hub-not-combined-modified.hex"])
call(["python","merge_hex.py","./BOOTLOADER.hex", "./SOFTDEVICE.hex", "./hub-not-combined-modified.hex", "-o./hub.hex"])

print "Cleaning up..."
call(["rm", "./hub-not-combined-modified.hex", "./hub-not-combined-modified.bin", "./hub-not-combined.uf2"])

# call
# call(["sed -i -E 's/(THIS_IS_THE_UNIQUE_SCHOOL_ID)/\1POOP/' ./hub.uf2"])
# call(["sed", "-i", "-E", "'s/THIS_IS_THE_UNIQUE_SCHOOL_ID/POOP/'","./hub.uf2"])

# os.remove("./hub.uf2")