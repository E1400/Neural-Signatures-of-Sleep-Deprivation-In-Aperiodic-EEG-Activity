# General Info 

The three main files for this research are:
- channel_specparam.ipynb
- specparam.ipynb
- eeg_preprocessing.py

the other files feature figures generated for analysis and csv files of extracted data

# Project Abstract

EEG signals are composed of both periodic (oscillatory) and aperiodic (non-oscillatory) features. 
Aperiodic features have been shown to influence the excitatory-inhibitory (E-I) balance of neural 
processes (Donoghue T et al, 2023). Sleep loss affects this E-I balance by increasing inhibition 
rate. Previous work describes aperiodic changes across sleep stages and after sleep deprivation, 
this change can result in neurological impacts such as worsened attention and memory. In the present 
investigation, we analyze an open resting-state EEG dataset with two sessions per subject: normal 
sleep (NS) vs. 24-h sleep deprivation (SD) - OpenNeuro ds004902 (Xiang, Fan, Bai, Lv, Lei; v1.0.8).
Using a spectral parameterization model (SpecParam), we extract parameters, aperiodic offset and 
aperiodic exponent, per channel and compare NS vs SD within-subject. Results show a significant 
increase in aperiodic offset after SD in 5 different channels, with no significant change in 
aperiodic exponent.

