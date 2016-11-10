apt-get install make zlib1g-dev build-essential default-jre unzip
wget https://github.com/samtools/htslib/releases/download/1.2.1/htslib-1.2.1.tar.bz2
tar -xvf htslib-1.2.1.tar.bz2
wget https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2
tar -xvf samtools-1.2.tar.bz2
wget https://github.com/samtools/bcftools/releases/download/1.2/bcftools-1.2.tar.bz2
tar -xvf bcftools-1.2.tar.bz2
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.33.zip
unzip Trimmomatic-0.33.zip
wget https://github.com/lomereiter/sambamba/releases/download/v0.5.9/sambamba_v0.5.9_linux.tar.bz2

https://help.ubuntu.com/lts/serverguide/openssh-server.html
http://askubuntu.com/questions/384062/how-do-i-create-and-tune-an-ext4-partition-from-the-command-line


#turn swap off 
swapoff -a
#rm the partitions for swap
#rm the line from fstab
reboot
#rm root partition and create a new one with desired size, make it bootable with "a"
reboot
#create the swap partition with fdisk make swap with "t" and 82 
mkswap /dev/XXX
#find the blkid with "blkid"
#add the line to fstab to mount swap
#resize main root parition
resize2fs /dev/xxx
reboot
