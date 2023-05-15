import csv
import os

import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = csv.reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, _, img_files in os.walk(path):
        for image in sorted(img_files):
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folders(path):
    object_types, folders_list = [], []

    for dirname in os.listdir(path):
        object_type = dirname.split("_", 1)[1]
        dirpath = os.path.join(path, dirname)
        folders_list.append(import_folder(dirpath))
        object_types.append(object_type)

    return object_types, folders_list


def reflect_images(frames):
    return [pygame.transform.flip(frame, True, False) for frame in frames]


def add_reflected(frames):
    keys = list(frames.keys())
    for right_key in keys:
        left_key = right_key.replace("right", "left")
        frames[left_key] = reflect_images(frames[right_key])
