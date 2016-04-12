# Introduction

I need some stuff to help plan Drobo expansions.

The main thing is something that will backup the Drobo to two different external drives. Currently, I barely fit in 
an 8TB drive. That drive replaced my two 5TB drive solution. I put one of the 5TB drives in the Drobo so now have the 
8TB and other 5TB drives to split the Drobo.

This program should accept a list of directories to keep together. The program should check that directory set will 
fit on the largest drive. If not, then error. Else, make sure that the external drives are sufficient. If not, error. 
Else, copy the directory set to the larger drive. Then fit the rest of the Drobo across the remaining drives.

# Implementation

One of the destination drives will be the "primary destination" or "primeDest".  At its root, it will have a directory
called "prime".  In it will be the most important directories from the source drive.  Those files will be defined in
the config file.

- Read in the config file  

- Find the source drive and the two destination drives
  - Make sure the destination drives are sufficiently large
  
  
# File layout
In the source drive, the layout, for an example, could be:
\a
\b
\c
\d
\Photo catalog
\Joli Productions
  
In the primary destination drive, the layout will like the below as an example:
\prime
\prime\Photo catalog
\prime\Joli Productions
\other
\other\a
\other\b

In the secondary destination drive:
\other
\other\c
\other\d


# To do

(trivial change to test mail and name config)