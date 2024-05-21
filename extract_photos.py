#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noai:et:tw=80:ts=4:ss=4:sts=4:sw=4:ft=python

'''
Title:              extract_photos.py
'''
import argparse
import time
import zipfile
import json
import shutil
import pathlib
import os
import re
import unicodedata


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Also strip leading and trailing whitespace,
    dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def main(args):
    """
    This function will extract the images located into the AP notes and rename
    them using the AP Name if available else it will use the the note text.
    """
    # Load and Unzip the Ekahau Project File
    current_filename = pathlib.PurePath(args.file).stem
    with zipfile.ZipFile(args.file, 'r') as myzip:
        myzip.extractall(current_filename)

        all_filenames = [f.filename for f in myzip.filelist]
        # Load the notes.json file into the notes Dictionary
        with myzip.open('notes.json') as note_file:
            notes = json.load(note_file)

        # Load the access_points.json file into the access_points dictionary
        if 'access_points.json' in all_filenames:
            with myzip.open('access_points.json') as ap_file:
                access_points = json.load(ap_file)
        else:
            access_points = False

        # Load the floor_plans.json file into the floor_plans dictionary
        if 'floor_plans.json' in all_filenames:
            with myzip.open('floor_plans.json') as floor_file:
                floor_plans = json.load(floor_file)
        else:
            floor_plans = False

    # Create a new directory to place the new image in
    newpath = os.path.abspath(pathlib.PurePath()) + "/AP-Images"
    check_dir(newpath)

    if access_points and floor_plans:
        # Create one sub directory per floor under the /AP-Images directrory
        for floor in floor_plans['floor_plans']:
            floor_name = slugify(floor['name'])
            sub = newpath + '/' + floor_name
            check_dir(sub)
            # Create the floor image
            if floor['imageId']:
                floor_full_path = os.getcwd() + '/' + current_filename + '/image-' + floor['imageId']
                floor_dst = sub + '/' + floor_name + '.png'
                shutil.copy(floor_full_path, floor_dst)

            # Move all the AP Images on this floor into the corresponding directory
            for ap in access_points['access_points']:
                if 'location' in ap.keys():
                    if ap['location']['floorPlanId'] == floor['id']:
                        if 'noteIds' in ap.keys():
                            for note in notes['notes']:
                                if note['id'] == ap['noteIds'][0] and len(note['imageIds']) > 0:
                                    ap_name = slugify(ap['name'])
                                    image_count = 1
                                    for image in note['imageIds']:
                                        image_full_path = os.getcwd() + '/' + current_filename + '/image-' + image
                                        if len(note['imageIds']) > 1:
                                            dst = newpath + '/' + floor_name + '/'+ ap_name + '-' + str(image_count) + '.png'
                                        else:
                                            dst = newpath + '/' + floor_name + '/'+ ap_name + '.png'
                                        shutil.copy(image_full_path, dst)
                                        image_count += 1
    elif access_points:
        for ap in access_points['access_points']:
            if 'noteIds' in ap.keys():
                for note in notes['notes']:
                    if note['id'] == ap['noteIds'][0] and len(note['imageIds']) > 0:
                        ap_name = slugify(ap['name'])
                        image_count = 1
                        for image in note['imageIds']:
                            image_full_path = os.getcwd() + '/' + current_filename + '/image-' + image
                            if len(note['imageIds']) > 1:
                                dst = newpath + '/'+ ap_name + '-' + str(image_count) + '.png'
                            else:
                                dst = newpath + '/'+ ap_name + '.png'
                                shutil.copy(image_full_path, dst)
                                image_count += 1
    else:
        if floor_plans:
            for floor in floor_plans['floor_plans']:
                # Create the floor image
                if floor['imageId']:
                    floor_full_path = os.getcwd() + '/' + current_filename + '/image-' + floor['imageId']
                    floor_dst = newpath + '/' + slugify(floor['name']) + '.png'
                    shutil.copy(floor_full_path, floor_dst)
        # Use note text for each image
        for note in notes['notes']:
            if len(note['imageIds']) > 0:
                note_text = slugify(note['text'])
                image_count = 1
                for image in note['imageIds']:
                    image_full_path = os.getcwd() + '/' + current_filename + '/image-' + image
                    if len(note['imageIds']) > 1:
                        dst = newpath + '/' + note_text + '-' + str(image_count) + '.png'
                    else:
                        dst = newpath + '/' + note_text + '.png'
                    shutil.copy(image_full_path, dst)
                    image_count += 1

    # Clean Up
    shutil.rmtree(current_filename)


if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Extract images located in the notes and rename them using the AP name or note text')
    parser.add_argument('file', metavar='esx_file', help='Ekahau project file')
    args = parser.parse_args()
    print('** Extracting AP picture notes...')
    main(args)
    run_time = time.time() - start_time
    print("** Time to run: %s sec" % round(run_time,2))

