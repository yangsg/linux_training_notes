import shutil  #// shell util
shutil.copyfile('/etc/fstab', '/tmp/fstab.bak')     #//copy 文件
shutil.copyfile('/etc/fstab', '/tmp/fstab.bak02')
shutil.move('/tmp/fstab.bak02', '/tmp/fstab_moved') #// 移动文件


