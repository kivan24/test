import sys
import os
import pwd
import grp

USER = 'root'
GROUP = 'root'
FILE_PERMISSIONS = [600, 700, 640, 740, 644]
FOLDER_PERMISSIONS = [700, 750, 755]


def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            path = os.path.join(root, name)
            owner, group, permissions = get_file_info(path)
            # print("Owner: {}, Group: {}, Permissions: {} -, Directory: {}".format(owner, group, permissions, path))
            check_object_permissions(path, owner, group, permissions, FOLDER_PERMISSIONS)

        for name in files:
            path = os.path.join(root, name)
            owner, group, permissions = get_file_info(path)
            # print("Owner: {}, Group: {}, Permissions: {} -, File: {}".format(owner, group, permissions, path))
            check_object_permissions(path, owner, group, permissions, FILE_PERMISSIONS)


def get_file_info(path):
    # Отримуємо інформацію про файл
    stat_info = os.stat(path)

    # Отримуємо власника, групу та права доступу
    owner = pwd.getpwuid(stat_info.st_uid).pw_name
    group = grp.getgrgid(stat_info.st_gid).gr_name
    permissions = int(oct(stat_info.st_mode & 0o777)[2:])

    return owner, group, permissions


def check_object_permissions(path, owner, group, permissions, normal_permissions):
    if owner != USER or group != GROUP:
        print("chown {}:{} {}".format(owner, group, path))

    if permissions not in normal_permissions:
        print("chmod {} {}".format(permissions, path))


if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
        # Викликаємо функцію для сканування каталогу
        scan_directory(sys.argv[1])
    else:
        print("Please give folder")
