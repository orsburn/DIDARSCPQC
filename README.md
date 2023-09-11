# DIDARSCPQC
Diagnostic Ion Data Analysis Reduction Adopted as a QC Pipeline for Multiplexed Single Cell Proteomics 
![image](https://user-images.githubusercontent.com/39571544/155019011-88808302-54f6-4a75-bf25-851754e46523.png)

DIDAR was originally developed by Conor J Jenkins (@SpecInformatics) for the identification and rapid filtering of files containing diagnostic fragment ions and based on earlier work on R.I.D.A.R. that he completed during his M.S. work at Hood College.
Here I have subverted DIDAR for multiplexed single cell proteomics. When used in this manner, DIDAR can provide direct metrics on the number of spectra containing reporter ions corresponding to single cells. It can also filter out spectra that do not contain a user specified number of single cell reporter ions for simplification of downstream data analysis. 
Inter and intrabatch measurements and graphics can be easily constructed from the tiny diagnostic ion text files. 
![image](https://user-images.githubusercontent.com/39571544/155019342-fc75fc49-3566-4e9a-9641-b97bef7d04aa.png)
For further information, please see the biorxiv preprint by Jenkins and Orsburn, 2022. 
For a brief and unprofessional tutorial on using the original version of this tool, check out this video: https://youtu.be/ojHdmJsFmEM

Just want to run the GUI version without using any stupid Python thing? You can download it and double click on it if you're using Windows. Here is a tutorial. https://youtu.be/i1-oPewLH00
