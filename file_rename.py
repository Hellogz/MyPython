import os

"""
file_path: 文件路径，例如：'D:/test/file_rename/'，需要注意 windows 和 linux 的路径分割符，路径名末尾需要带上分隔符
old_prefix: 旧文件名前缀，需要修改的部分
new_prefix: 新文件名前缀，需要修改为的部分
"""
def file_rename(file_path, old_prefix, new_prefix):
    file_list = os.listdir(file_path)
    change_file_name_count = 0
    for file_name in file_list:
        if file_name[:len(old_prefix)] == old_prefix:
            old_name = file_path + file_name
            new_name = file_path + new_prefix + file_name[len(old_prefix):]
            print("%s -> %s" %(old_name, new_name))
            os.rename(old_name, new_name)
            change_file_name_count += 1
    print("%s have %d file rename." %(file_path, change_file_name_count))

if __name__ == '__main__':
    file_path = 'D:/test/file_rename/'
    old_prefix = 'abcd'
    new_prefix = 'efgh'
    file_rename(file_path, old_prefix, new_prefix)
