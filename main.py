import re
import os

command = ""
count = 0

# SkipWhite can be good if you want transparency
SkipWhite = True
SkipBlack = False

RepeatingOrImpulse = input("Repeating or inpulse, please put a r or i in as a answer: ").lower()
isImpulse = 'i' in RepeatingOrImpulse

tag = input("put in armor stand tag: ")

print("\n")

def correct_command(command):
    match = re.search(r'particle minecraft:dust (\d+(\.\d+)?) (\d+(\.\d+)?) (\d+(\.\d+)?) (\d+(\.\d+)?)', command)
    if match:
        color = [match.group(1), match.group(3), match.group(5)]
        
        if SkipWhite == True and all(float(c) >= 0.95 for c in color):
            print(f"Skipping white particle command: {command}")
            return None
        
        if SkipBlack == True and all(float(c) <= 0.05 for c in color):
            print(f"Skipping black particle command: {command}")
            return None
            
        scale = match.group(7)
        
        new_particle_format = f"minecraft:dust{{color:[{', '.join(color)}], scale:{scale}}}"
        corrected_command = re.sub(r'particle minecraft:dust \d+(\.\d+)? \d+(\.\d+)? \d+(\.\d+)? \d+(\.\d+)?', f'particle {new_particle_format}', command)
        return corrected_command
    else:
        print(f"No match: {command}")
    return None

base = """summon falling_block ~ ~1 ~1 {BlockState:{Name:redstone_block},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:falling_block,BlockState:{Name:activator_rail},Passengers:[{id:command_block_minecart,Command:'gamerule commandBlockOutput false'},"""

# template = """{id:command_block_minecart,Command:'setblock ~ ~{Yoffset} ~1 minecraft:chain_command_block[facing=up,conditional=false]{Command:"{command}"}'},"""

class startingCommandBlockImpulse:
  def __init__(self, Yoffset, commandToRun):
        self.command = (
            "{{id:command_block_minecart,Command:'setblock ~ ~{Yoffset} ~1 "
            "minecraft:command_block[facing=up,conditional=false]"
            "{{Command:\"{commandToRun}\"}}'}}"
        ).format(Yoffset=Yoffset, commandToRun=commandToRun)

class startingCommandBlockRepeat:
  def __init__(self, Yoffset, commandToRun):
        self.command = (
            "{{id:command_block_minecart,Command:'setblock ~ ~{Yoffset} ~1 "
            "minecraft:repeating_command_block[facing=up,conditional=false]"
            "{{Command:\"{commandToRun}\"}}'}}"
        ).format(Yoffset=Yoffset, commandToRun=commandToRun)

class commandd:
  def __init__(self, Yoffset, commandToRun):
        self.command = (
            "{{id:command_block_minecart,Command:'setblock ~ ~{Yoffset} ~1 "
            "minecraft:chain_command_block[facing=up,conditional=false]"
            "{{Command:\"{commandToRun}\",auto:1b}}'}}"
        ).format(Yoffset=Yoffset, commandToRun=commandToRun)

class execu:
    def __init__(self, leTag):
        self.leletag = ( "execute at @e[tag={leTag}] run " ).format(leTag=leTag)

endOfBase = """{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:"fill ~ ~ ~ ~ ~-2 ~ air"}'},{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"""

command = command + base

allCommands = []
cmdBlockYHeight = 0

splitCommand = True

with open("commands.txt") as txt:
    Lines = txt.readlines()
    total_lines = len(Lines)
    for line in Lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("#"):
            print("Line starts with #!")
            continue
        
        cmdBlockYHeight += 1
        count += 1
        subCMD = line
        CorrectedCommand = correct_command(subCMD)
        if CorrectedCommand is None:
            cmdBlockYHeight -= 1
            continue
            
        subCMD = execu(tag).leletag + CorrectedCommand
        if (cmdBlockYHeight == 1):
            if (isImpulse):
                tempTemplate = startingCommandBlockImpulse(cmdBlockYHeight + 1, subCMD)
            else:
                tempTemplate = startingCommandBlockRepeat(cmdBlockYHeight + 1, subCMD)
        if (cmdBlockYHeight > 1):
            tempTemplate = commandd(cmdBlockYHeight + 1, subCMD)
            
        command = command + tempTemplate.command + ","
        
        if (len(command) > 31500 and splitCommand == True):
            print(f"Current length of command: {len(command)}")

            command = command + endOfBase
            allCommands.append(command)
            command = ""
            command = command + base
            cmdBlockYHeight = 0
        
        if count == total_lines - 1:
            if command:
                command = command + endOfBase
                allCommands.append(command)

if (splitCommand == False):          
    command = command + endOfBase

save_path = "./commands/"
os.makedirs(save_path, exist_ok=True)

for i, cmd in enumerate(allCommands):
    print(cmd + "\n\n")
    file = os.path.join(save_path, f'command_{i+1}.txt')
    with open(file, 'w') as file:
        file.write(cmd)
