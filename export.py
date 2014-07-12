#coding: utf-8
import os, time, sys, fnmatch
import subprocess
import shutil
import click






def find_files(path):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*'):
            matches.append(os.path.join(root, filename))
            return matches

def out(str):
    print(str)
    sys.stdout.flush()

def findModified(before, after):
    modified = []
    for (bf,bmod) in before.items():
        if (after[bf] and after[bf] > bmod):
            modified.append(bf)
            return modified

@click.command()
@click.option("--watch")
@click.option("--output")
def export(watch,output):
    if watch:
        INPUT_PATH = watch
    else:
        print("type watch")
        return

    if output:
        OUTPUT_PATH = output
    else:
        print("type output")
        return
    print(INPUT_PATH)



    out("Watching {}".format(INPUT_PATH))
    before = dict ((f, os.path.getmtime(f)) for f in find_files(INPUT_PATH))
    while 1:
      time.sleep (1)
      after = dict ((f, os.path.getmtime(f)) for f in find_files(INPUT_PATH))
      added = [f for f in after.keys() if not f in before.keys()]
      removed = [f for f in before.keys() if not f in after.keys()]
      modified = findModified(before,after)
      if added: out("Added: " + ", ".join (added))
      if removed: out("Removed: " + ", ".join (removed))
      if modified: out("Changed: " + ", ".join (modified))
      if (added or removed or modified):
          print("detect change")
          out("Recompiling...")
          cmd = "sketchtool export slices {} --output={}".format(INPUT_PATH,OUTPUT_PATH)
          print(cmd)
          os.system(cmd)

      before = after




if __name__ == "__main__":
    export()






