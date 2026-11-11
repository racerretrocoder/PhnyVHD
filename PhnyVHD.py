# PhnyVHD - By Phoenix
# Runs on Windows 7 SP1 and up
import os, time, sys, gzip
# could use import zlib   compressed = zlib.compress(data, level=6)  # data must be bytes
# could also use best lzma
print("Note! This program requires administrative rights!")
print("PhnyVHD - The Ultimate Hard Drive utility for full disk raw backups")
try:
    import wmi
    import psutil
except:
    print("I couldnt find some imports, I am going to install for you")
    os.system("pip install wmi")
    os.system("pip install psutil")
    time.sleep(10)
    print("wmi and psutil installed")
    import wmi, psutil
print("")
print("Checking out Physical Drives...")
print("")
drives = [] # drives list of total sectors per disk
drvpos = [] # for keeping order for drives[]
c = wmi.WMI()
for diskDrive in c.query("SELECT * FROM Win32_DiskDrive"):
    print(diskDrive.Name, "\nTotal Sectors: ", diskDrive.TotalSectors)
    drives.append(diskDrive.TotalSectors)# order is different, goes like pd2, pd1, pd0
    # actually order is non existant, will just say which index for which value
    drivesplit = diskDrive.Name
    drivesplit = drivesplit.split("PHYSICALDRIVE") # this means the second index (1) is the physicaldrivenumber for this sector count
    drivenum = int(drivesplit[1])
    drvpos.append(drivenum)
print("-------------- Couldnt detect any more Physical drives --------------")
print("Check out diskmgmt.msc to view the drive number for lettered volumes\n(drives listed from first 0 to last number from top to down)")
print("Disk 0 is PhysicalDrive0, Disk 1 is PhysicalDrive1, etc")
aeae = input("------ Press any key to continue ------")
# PVHD Operating modes.
# 0 = Save to .PVHD
# 1 = Restore from .PVHD
mode = 0 

def main():  
    global mode
    if os.name == "nt":
        os.system("cls")
        print("""
 ___________________________.
|;;|                     |;;||
|[]|---------------------|[]||
|;;|                     |;;||
|;;|                     |;;||
|;;|                     |;;||
|;;|                     |;;||   ______ __                 ___ ___ ______ ___
|;;|                     |;;||  |   __ \  |--.-----.--.--.|   |   |   |  |   \\
|;;|                     |;;||  |    __/     |     |  |  ||   |   |      |   |
|;;|_____________________|;;||  |___|  |__|__|__|__|___  | \_____/|___|__|___/
|;;;;;;;;;;;;;;;;;;;;;;;;;;;||                     |_____| 
|;;;;;;_______________ ;;;;;||
|;;;;;|  ___          |;;;;;||  Version 1.02 - Hard Drive Tools
|;;;;;| |;;;|         |;;;;;||
|;;;;;| |;;;|         |;;;;;||
|;;;;;| |;;;|         |;;;;;||
|;;;;;| |;;;|         |;;;;;||
|;;;;;| |___|         |;;;;;||
\_____|_______________|_____||
 ~~~~~^^^^^^^^^^^^^^^^^~~~~~~
                  """)
        time.sleep(1)
        print("PhnyVHD Version 1.02")
        print("Phoenix - Backdoor Interactive (c) 2026")
        print("DISCLAIMER: Use this software at your own risk. Any damage caused to data by mistake of input is\nNOT MY (or OUR) responsibility.\n")
        print("\nWhat would you like to do?\n0 --> Convert a physical drive to a .PVHD\n1 --> Flash a .PVHD to a physical drive\n")
        mode = int(input("\n> "))
        diskid = str(input("Enter a physicaldrive number\n> "))
        if mode == 0:
            print("Preparing drives - Please wait!") # read    
            os.system("cls")
            # note of funny variable, aeaeae is the filename
            aeaeae = str(input("Enter a filename without a path for the .PVHD\n\nWARNING: To prevent an infinite loop (where PVHD reads a PVHD its writing to)\nMake sure you save the PVHD on a different volume than the one you are\ngoing to convert. A USB Drive or portable secondary harddrive\n\n> "))
            if aeaeae[-5] != ".":
                aeaeae = aeaeae + ".PVHD" # auto append the filename
            thestring = "Where do you want to put "+aeaeae+" ? Enter the full directory without the filename\n\nNote: the directory doesnt have to exist, I will create it for you\n> "
            directory = str(input(thestring))
            if directory[-1] != "\\":
                directory = directory + "\\"
            read_sector(r"\\.\physicaldrive"+diskid, diskid, aeaeae, directory)
        if mode == 1:
            print("Preparing Drives - Please wait!")  # write  
            os.system("cls")
            aeaeae = str(input("Enter the full path with filename to the .PVHD file that will be written to a physical drive\n\nWARNING: Make sure you have the PVHD\non a different volume than the one you are going to flash! (common sense xd)\n\n> "))
            directory = "ae" # lol
            read_sector(r"\\.\physicaldrive"+diskid, diskid, aeaeae, directory)
    else:
        print("Hello linux user! I am sorry to say, but PVHD is not compatible on linux yet\nIt might be soon! So please stay tuned and keep in touch...\nIt is compatible with Windows 7 and up. Python 3.8.8")

def read_sector(disk, diskid, filename, directory, sector_no=0):
    diskid = int(diskid)
    global drives
    global drvpos
    #print(drives)
    global mode
    
    # statistics! Because who doesnt like statistics!
    sectorcounter = 0 # sector counter
    totalbyteswtn = 0 # total bytes written (approx)
    percentage = 0 # approx percentage of compleation

    drivesize = len(drives) - 1 # include the zero
    #print(drivesize)
    # Note this code aint used
    diskindexsectors = diskid
    if drivesize != 0:
        # looks like theres more than one hdd
        diskindexsectors = drivesize - diskid # if they choose drive 0, its the last index, if the choose drive 1, its the second last index.
    totalsectors = 0
    for i in range(len(drvpos)): # now we find it
        if int(drvpos[i]) == diskid: # found it!
            totalsectors = int(drives[i])
            print("the total sectors for this volume is ",totalsectors)
    print("Almost ready.")
    print("You selected Physicaldrive",diskid)
    if mode == 0:
        while True:
            try:
                bytesper = int(input("How many bytes per sector for this physical drive?\n> "))
                break
            except:
                print("Invalid entry! Your input must be an integer! (in bytes please)")
                time.sleep(0.5)
        request = input("How many bytes of the physical drive should the PVHD save? (Starting from the master boot record)\nEnter 0 to just copy the whole disk (This will make the PVHD be a fixed disk, the same size as the physical drive)\nSimply press ENTER without any numerical input to do it automatically\n> ")
        if request == "":
            print("Will automatically create a Dynamic PVHD\nThe used space on the disk will be the size of the PVHD")
            thestring = "What is the volume letter (C:\\, D:\\, etc) of Physicaldrive"+str(diskid)+"?\nCheck diskmgmt.msc if you are unsure\n> "
            drivelet = input(thestring)
            usage = psutil.disk_usage(drivelet+"\\")
            usedbytes = usage.used
            # check if the usage is divisable by a sector?
            sectorstowrite = usedbytes / bytesper
            if not sectorstowrite.is_integer():
                request = usedbytes + bytesper # Include an extra sector because the storage doesnt come out cleanly
            else:
                request = usedbytes # perfect used space!
        else:
            request = int(request) # Switch the input
        while True:

            # stuff about metadata 2.0
            # it must not exceed or come short of exactly 550 bytes. so "filler" must be added to meet the intentions
            print("Creating PVHD Metadata for: ",filename)
            name = str(input("Enter a name for the PVHD (Max 25 chars)\n> "))
            desc = str(input("Enter a description for the PVHD (Max 460 chars)> "))
            desc = desc.replace("~n","\n") # make the tip true ae
            if len(name) > 25:
                print("That name is longer than 25 chars! Please shorten it")
            elif len(desc) > 460:
                print("Your description is a little too long! Please shorten it to a maximum of 460 charecters")
            break
        if len(name) < 25:
            needed = 25 - len(name)
            for i in range(needed):
                    name = name + " " # add a filler
            print("done appending name")
            print(len(name))
            print(name)
        if len(desc) < 460:
            needed = 460 - len(desc)
            for i in range(needed):
                desc = desc + " " # add filler
            print("done appending desc")
            print(len(desc))# ||END|| 7 byte end header
        while True:
                #   New modes!
                #   R RAW
                #   C Compressed
                #   E Encrypted
            print("Which mode should the PVHD operate in?")
            print("R - RAW, save the drives contents directly")
            print("C - Compressed, (de)Compresses a large heap of sectors. Creates individual compressed files in a seperate folder")
            print("E - Encryption (and compression) WIP This option is broken")
            print("Press Enter to autoselect the RAW formate")
            pvhdmode = input("> ")
            if pvhdmode == "":
                pvhdmode = "R"
            pvhdmode = pvhdmode.upper()
            if pvhdmode == "r" or pvhdmode == "c" or pvhdmode == "R" or pvhdmode == "C":
                # valid
                break
            print("Invalid entry!")

        # Compression stuff
        # statisically speaking, for 512bps, a scale of 10,000 produces every 211 files for 1GB | Windows reports 5,000kb
        #```````````````````````````````````a scale of 100,000 produces every 22 files for 1GB but overshoots and goes to 1.04, Windows repots 50,000
        # 10,000 has its downside, a large file count, but accurate enough and can only overshoot by 5,000KB
        if len(str(bytesper)) > 3:
            compbytes = bytesper * 10000  # if 4096, 0.4096gb
        else:
            compbytes = bytesper * 10000 # if 512,  0.5120gb
        # NOTE: If you change these values, please be sure to change the values for the addedsector variable! (use control-f, youll find it)
        # NOTE: There are 2 instances of this variable, one here, and one all the way at the bottom for mode 1 (writing)
        # NOTE:                

        # total physicaldrive sectors will be in PVHD metadata for future referernce
        # This number will be limited to 15 bytes (so 15 digits). It will be parsed by string and the filler will be 0's
        # Good thing running int() on string "000000000000123" gives a number of 123 :D

        pvhdtotalsectors = 0 # to prevent null ref's
        for i in range(len(drvpos)): # now we find it
            if int(drvpos[i]) == diskid: # found it!
                pvhdtotalsectors = str(drives[i])
                print("the total sectors for this volume is ",pvhdtotalsectors)
        while True:
            if len(pvhdtotalsectors) != 15:
                # not 15 bytes, so add a couple zero's
                pvhdtotalsectors = "0" + pvhdtotalsectors
                print(pvhdtotalsectors) # print it out while its adding to visualize
            else:
                # done, total sectors is now ready to be placed in the header
                print("done filling totalsectors heres the result: ",pvhdtotalsectors)
                break 
        # now for used sectors
        pvhdusedsectors = request / bytesper # take used size bytes and divide it by bytes per sector to get sector count
        pvhdusedsectors = int(pvhdusedsectors) # trunk it / intify it
        pvhdusedsectors = str(pvhdusedsectors) # re-re-stringify it
        while True:
            if len(pvhdusedsectors) != 15:
                # not 15 bytes, so add a couple zero's
                pvhdusedsectors = "0" + pvhdusedsectors
                print(pvhdusedsectors) # print it out while its adding to visualize
            else:
                # done, total sectors is now ready to be placed in the header
                print("done filling used heres the result: ",pvhdusedsectors)
                break 

        metadata = "PVHD2.0|"+str(bytesper)+"|"+pvhdmode+"|"+pvhdtotalsectors+"|"+pvhdusedsectors+"|"+name+"|"+desc+"|" # This is header version 2.0
        # typically 533 bytes is the smallest header (with 512 bytes per sector and not a 4 byte number)
        # The header trailer (||END||) is 7 bytes long, so an extra 10 bytes of space is available in the header (max size is 550 bytes)
        while len(metadata) < 543: # add filler till theres just enough to fit the trailer
            # need filler
            metadata = metadata + "-" # add the dashes
        metadata = metadata + "||END||" # add the trailer
        print(metadata)
        print("Final length:")
        print(len(metadata))
        metabytes = metadata.encode("utf-8")
        print(metabytes)
        print(len(metabytes))
    if mode == 1:
        # get all info from pvhd metadata ae xd
        while True:
            with open(filename,"rb") as pvhd:
                pvhd.seek(0)
                metadata = pvhd.read(550)
                print("Loading PVHD...")
                #print(metadata)
                metaconvert = metadata.decode("utf-8")
                #print("Converted!")
                #print(metaconvert)
                listA = metaconvert.split("|")
                # Header version 1.0 "PVHD|"+str(bytesper)+"|"+name+"||E||"+desc+""
                # Header version 2.0  
                if str(listA[0] == "PVHD2.0"):
                    os.system("cls")
                    print("The given file is a valid PVHD File! (Version: 2.0)")
                    bytesper = int(listA[1])
                    pvhdmode = str(listA[2])
                    pvhdtotalsectors = int(listA[3])
                    pvhdusedsectors = int(listA[4])
                    name = str(listA[5])
                    name = name.replace("   ","") # Defiller
                    desc = str(listA[6])
                    desc = desc.replace("-","") # Defiller
                    desc = desc.replace("   ","") # Defiller
                    pvhdsize = pvhdtotalsectors * bytesper
                    pvhdused = pvhdusedsectors * bytesper
                    pvhdsizegb = pvhdsize / 1000000000
                    print("Information about ",filename)
                    print("Name:",name)
                    print("Description:",desc)
                    print("Bytes / Sector: ",bytesper)
                    print("Total Sectors: ",pvhdtotalsectors)
                    print("Used Sectors: ",pvhdusedsectors)
                    print("Virtual Physical Drive Size: ",int(pvhdsizegb),"GB")
                    dummyvar = input("Is file the one to flash? (y/n)\n> ")
                    if dummyvar == "y":
                        break #continue
                        print("Will flash ",filename," to Physicaldrive",diskid)
                        print("Selected Physical Drive",diskid)
                        time.sleep(1)
                    else:
                        filename = input("Enter the full path of a valid PVHD file to use.\n> ")
                else:
                    print("Error: ",filename," is not a valid PVHD File")
                    filename = input("Enter the full path of a valid PVHD file to use.\n> ")
                

    #os.system("cls")
    print("This is information about Physicaldrive",diskid," - The drive thats selected to read / write from")
    print("estimated total sectors detected: ",totalsectors)
    print("Calculating drive size manually...")
    estdrivesizebytes = totalsectors * bytesper
    estdrivesizegbyte = estdrivesizebytes / 1000000000
    print("estimated Physicaldrive size (in bytes): ",estdrivesizebytes," Bytes")
    print("estimated Physicaldrive size (in gbyte): ",estdrivesizegbyte," Gigabytes")
    print("If any of this information seems wrong, check to make sure you selected the correct physical drive number")
    if mode == 1:
        print("Warning! All data on PhysicalDrive",diskid," will be erased to flash the PVHD file!")
    ae2 = input("\nPress any key to start!!")
    read = None
    #
    # Reading and Writing
    #
    if mode == 0: # Read mode (Create PVHD)
        with open(disk, 'rb') as hdd: # init the hard disk
            # move the heads to the start
            hdd.seek(0)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if pvhdmode == "C": # Compression!
                if not os.path.exists(directory+filename+"compressed"):
                    os.makedirs(directory+filename+"compressed")
                    
            with open(directory+filename, 'wb') as pvhd:
                # clear the file and add in metadata!
                pvhd.write(metabytes) # Writeout the metadata
                os.system("cls")
                print("Reading the drive and writing to the PVHD file\nDo not close this window or unplug any drives\n")
                percentage = 0
                percentold = -1
                compresscounter = 0 # Start at file number 0
                while True:
                    try:
                        if pvhdmode == "R":
                            # Raw disk
                            sector = hdd.read(bytesper) # get the sector xd
                            if not sector:
                                print("Reached end of HDD disk!")
                                ae = input("Press any key to continue")
                                pvhd.close()
                                hdd.close()
                                break
                            pvhd.write(sector)
                            sectorcounter = sectorcounter + 1
                            totalbyteswtn = sectorcounter * bytesper
                            # now percentage calc!
                            # Request: If request is given (Dynamic PVHD)
                            if request != 0:
                                percentage = totalbyteswtn / request
                                percentage = percentage * 100
                                percentage = int(percentage) # change to int
                                perstring = str(percentage)
                                if percentold != percentage:
                                    os.system("cls")
                                    print("Reading the drive and writing to the PVHD file\nDo not close this window or unplug any drives\n")
                                    print("Progress: ",percentage,"% Complete") # ehh print it out why not
                                    percentold = percentage
                            if request != 0:
                                if request + bytesper < totalbyteswtn: # add just one extra sector to write
                                    print("-------------------- Finished! -------------------- \nThe PVHD has been successfully written to ",directory+filename,"\n")
                                    pvhd.close()
                                    ae = input("Press any key to exit the utility")
                                    break

                            if request == 0:
                                percentage = sectorcounter / totalsectors
                                percentage = percentage * 100
                                percentage = int(percentage) # change to int
                                perstring = str(percentage)
                                if percentold != percentage:
                                    os.system("cls")
                                    print("Reading the entire drive and writing to the PVHD file\nDo not close this window or unplug any drives\n")
                                    print("Progress: ",percentage,"% Complete") # ehh print it out why not
                                    percentold = percentage
                            if request == 0:
                                if sectorcounter == totalsectors or sectorcounter > totalsectors: # write data to the last sector and dont go over
                                    print("-------------------- Finished! -------------------- \nThe PVHD has been successfully written to ",directory+filename,"\n")
                                    pvhd.close()
                                    ae = input("Press any key to exit the utility")
                                    break
                        if pvhdmode == "C":
                            # Compression
                            # Variable is compbytes
                            sectorheap = hdd.read(compbytes)
                            if not sectorheap:
                                if compresscounter == 0:
                                    print("ERROR! The drive appears to be to small to compress")
                                print("Reached end of the drive!")
                                ae = input("Press any key to exit!")
                                pvhd.close()
                                hdd.close()
                                break
                            print("Compressing sectorheap #",str(compresscounter))

                            sectorheap = gzip.compress(sectorheap)
                            thestring = directory+filename+"compressed"+"\\compressedsectors"+str(compresscounter)+".bin"
                            
                            # write and compress
                            
                            with open(thestring, 'wb') as compressedbinary:
                                print("Writing out compressed data")
                                compressedbinary.write(sectorheap) # create a compressed file
                                compressedbinary.close() # close it
                                print("Completed compression of sectorheap #",str(compresscounter))
                                 
                            compresscounter = compresscounter + 1 # increment the file number
                            if len(str(bytesper)) > 3:
                                addedsector = 10000  # if 4096, 0.4096gb per file
                            else:
                                addedsector = 10000 # if 512,  0.5120gb per file (uncompressed)
                            # NOTE: if you change these values, please change the values for the variable compbytes aswell
                            # NOTE: There is a second instance of this variable over in mode 1 (the HDD writing section towards the bottom)
                            # (use control-f and search for "bytesper *")
                            # increase counter
                            sectorcounter = sectorcounter + addedsector
                            totalbyteswtn = sectorcounter * bytesper    # note: this is the total ammount of UNCOMPRESSED bytes written
                            print(totalbyteswtn)
                            # Percentage calc for compression progress
                            if request != 0:
                                percentage = totalbyteswtn / request
                                percentage = percentage * 100
                                percentage = int(percentage) # change to int
                                perstring = str(percentage)
                                if percentold != percentage:
                                    os.system("cls")
                                    print("Reading the drive, compressing and writing to the PVHD file\nDo not close this window or unplug any drives\n")
                                    print("Progress: ",percentage,"% Complete") # ehh print it out why not
                                    percentold = percentage
                            if request != 0:
                                if request + compbytes <= totalbyteswtn: # add just one extra sector to write
                                    print("-------------------- Finished! -------------------- \nThe PVHD has been successfully written to ",directory+filename,"\n")
                                    pvhd.close()
                                    ae = input("Press any key to exit the utility")
                                    break
                            if request == 0:
                                percentage = sectorcounter / totalsectors
                                percentage = percentage * 100
                                percentage = int(percentage) # change to int
                                perstring = str(percentage)
                                if percentold != percentage:
                                    os.system("cls")
                                    print("Reading the drive, compressing and writing to the PVHD file\nDo not close this window or unplug any drives\n")
                                    print("Progress: ",percentage,"% Complete") # ehh print it out why not
                                    percentold = percentage
                            if request == 0:
                                if sectorcounter == totalsectors or sectorcounter > totalsectors: # write data to the last sector and dont go over
                                    print("-------------------- Finished! -------------------- \nThe PVHD has been successfully written to ",directory+filename,"\n")
                                    pvhd.close()
                                    ae = input("Press any key to exit the utility")
                                    break
                        
                            
                    except Exception as e:
                        print("We've hit an error, most likely reached the end of the hard disk!")
                        print("At sector: ",sectorcounter)
                        print("Error: ",e)
                        pvhd.close()
                        print("The PVHD File was closed and data written to it may be corrupt")
                        break
    if mode == 1: # Write mode!
        os.system("cls")
        print("For Physicaldrive",diskid,", Please go into disk management\n(I will conviently open diskmgmt.msc for you) and UNMOUNT it\nTo do this: right click the drive, click change drive letters and paths\nthen hit remove, and finallky OK. \nThis unmounts the volume (Kinda like ejecting a flashdrive but not really)\nThis will allow PVHD to have full unrestricted access to the drive to write!\nIf the physical drive you are writing too is not a removeable device\nDelete all partitions on the drive you are writing to")
        os.system("start diskmgmt.msc")
        dummyvar = input("Press any key when ready to proceed")
        #try:
        print("Attempting to open PhysicalDrive",diskid," for excluseive write access")
        hdd = open(disk, 'rb+')# as hdd: # init hard disk
        hdd.seek(0)# move the heads to the start
        if pvhdmode == "R": # RAW Write
            print(filename)
            pvhd = open(filename, 'rb')
            print("PVHD opened")
            pvhd.seek(550) # Skip the header
            print("Reading PVHD...") # 
            pvhdsize = os.path.getsize(filename) - 550 # IMPORTANT: Skip the header!
            print("PVHD Size (in bytes):  ",pvhdsize)
            print("Writing to the disk. Please wait")
            percentold = -1
            while True:
                    # break check
                    percentage = totalbyteswtn / pvhdsize
                    percentage = percentage * 100
                    percentage = int(percentage)
                    if totalbyteswtn >= pvhdsize:
                        print("Files done!")
                        print("",percentage,"% Complete. Disk write finished successfully!!")
                        time.sleep(1)
                        dummyvar = input("Do a Disk Rescan in Disk Management\nPress any key to exit")
                        break
                    # so far: This only works well if both files have the same bytes per sector
                    sector = pvhd.read(bytesper) # get a sector from pvhd
                    #print("Sector to write:\n",sector)
                    if sector != b"":
                        hdd.write(sector) # write it out
                    else:
                        blanksector = 1
                    #print("Written that sector!")
                    # step up
                    totalbyteswtn = totalbyteswtn + bytesper
                    sectorcounter = sectorcounter + 1
                    perstring = str(percentage)
                    if percentold != percentage:
                        os.system("cls")
                        print("Flashing the PVHD to the Physical Drive\nDo not close this window or unplug any drives\n")
                        print("Progress: ",percentage,"% Complete") # ehh print it out why not
                        percentold = percentage
    if pvhdmode == "C":
        # Its a compressed PVHD
        # read the compressed file
        # decompress it
        # write it out
        # repeat
        compresscounter = 0
        thestring = filename+"compressed\\compressedsectors"+str(compresscounter)+".bin"
        percentold = -1
        if len(str(bytesper)) > 3:
            compbytes = bytesper * 10000  # if 4096, 0.4096gb
        else:
            compbytes = bytesper * 10000 # if 512,  0.5120gb
        if len(str(bytesper)) > 3:
            addedsector = 10000  # if 4096, 0.4096gb per file
        else:
            addedsector = 10000  # if 512,  0.5120gb per file (uncompressed)
        sectorcounter = 0
        while True:
            # read it, decomp, write it out, repeat till end of compfile list
            thestring = filename+"compressed\\compressedsectors"+str(compresscounter)+".bin"
            try:
                with open(thestring, "rb") as compsectors: # open a compression heap
                    compressed = compsectors.read()
                    if compressed != b"":
                        print("Decompressing sectorheap #",compresscounter)
                        sectorheap = gzip.decompress(compressed)
                        hdd.write(sectorheap) # write out the data

                    totalbyteswtn = sectorcounter * bytesper    # note: this is the total ammount of UNCOMPRESSED bytes written
                    percentage = totalbyteswtn / pvhdused
                    percentage = percentage * 100
                    percentage = int(percentage)
                    if totalbyteswtn >= pvhdsize:
                        print("Drive writing done!")
                        print("",percentage,"% Complete. Disk write finished successfully!!")
                        time.sleep(1)
                        dummyvar = input("Do a Disk Rescan in Disk Management\nPress any key to exit")
                        break
                    sectorcounter = sectorcounter + addedsector 
                    perstring = str(percentage)
                    if percentold != percentage:
                        os.system("cls")
                        print("Flashing the PVHD to the Physical Drive\nDo not close this window or unplug any drives\n")
                        print("Progress: ",percentage,"% Complete") # ehh print it out why not
                        percentold = percentage
                    compsectors.close()
            except:
                print("Physical write completed successfully!\nDo a disk rescan in diskmanagement to see the results!")
                ae = input("Press any key to exit")
                break
                exit()
            # End of loop xd
            compresscounter = compresscounter + 1 # visit the next compressed file
            thestring = filename+"compressed\\compressedsectors"+str(compresscounter)+".bin"
if __name__ == "__main__":
    main()
