for file in ../genomes/*.fa   
do
blat $file /dev/null /dev/null -makeOoc=$file.11.ooc -repMatch=1024
done

blat ../genomes/a_th.fa ../input/eudicots.fasta -ooc=../genomes/a_th.fa.11.ooc ../blat_output/eudicots.psl


