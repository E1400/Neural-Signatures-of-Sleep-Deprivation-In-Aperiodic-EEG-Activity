import mne
import mne.io.eeglab
import numpy as np
import pandas as pd
import os
# Neurodsp libraries
from neurodsp import spectral
# SpecParam libraries 
from specparam import SpectralModel, SpectralGroupModel



def load_eeg(file_path):
    return mne.io.read_raw_eeglab(file_path, preload=True)

def select_channel(raw, channel):
    return raw.copy().pick([channel])

def get_channel_data(raw):
    return raw.get_data()[0]

def load_and_extract_channel_data(file_path, channel):
    # loads data from file path
    # return sampling rate 
    raw = load_eeg(file_path)
    raw_channel = select_channel(raw, channel)
    return get_channel_data(raw_channel), raw.info['sfreq']  

def specparam_per_channel(root_path, participants_tsv, output_dir, f_range = (1,40)):
    participants = pd.read_csv(participants_tsv, sep = '\t')
    results_NS = []
    results_SD = []
    
    #info from participants_tsv
    for _, row in participants.iterrows():
        subject = row['participant_id']
        order = row['SessionOrder']
        
        if order == 'NS->SD':
            session_order = {'ses-1':'NS','ses-2':'SD'}
        else: 
            session_order = {'ses-1':'SD','ses-2':'NS'}
          
        for session, condition in session_order.items():
            eeg_dir = os.path.join(root_path, subject, session, 'eeg')
            eeg_files = [f for f in os.listdir(eeg_dir) if 'open' in f and 'clean' in f and f.endswith('.set')]
            if not eeg_files:
                print(f"No eyes-open file found for {subject} {session}")
                continue

            file_path = os.path.join(eeg_dir, eeg_files[0])
            print(f"Loading {subject} {session} ({condition}) → {file_path}")
            
            # Load and read EEG
            raw = mne.io.read_raw_eeglab(file_path, preload=True)
            data = raw.get_data()
            ch_names = raw.info['ch_names']
            sfreq = raw.info['sfreq']
            
            for ch_idx, ch_name in enumerate(ch_names):
                signal = data[ch_idx,:]
                freqs, psd = spectral.compute_spectrum(signal, sfreq, method='welch', avg_type='mean')
                
                psd = np.nan_to_num(psd, nan=0.0, posinf=0.0, neginf=0.0)
                psd[psd <= 0] = np.min(psd[psd > 0]) if np.any(psd > 0) else 1e-12
                
                model = SpectralModel(peak_width_limits=[1, 12], aperiodic_mode='fixed', verbose=False)
                model.fit(freqs,psd,f_range)
                
                # grab parameters
                aperiodic_params = model.aperiodic_params_
                aperiodic_exp = aperiodic_params[1] if len(aperiodic_params) > 1 else np.nan
                aperiodic_offset = aperiodic_params[0] if len(aperiodic_params) > 0 else np.nan
                n_peaks = len(model.peak_params_) if model.peak_params_ is not None else 0
                
                results = {
                    'subject':subject,
                    'session':session,
                    'condition':condition,
                    'channel':ch_name,
                    'aperiodic_exponent':aperiodic_exp,
                    'aperiodic_offset':aperiodic_offset,
                    'n_peaks':n_peaks
                }
                
                if condition == 'NS':
                    results_NS.append(results)
                else:
                    results_SD.append(results)

    NS_df = pd.DataFrame(results_NS)
    SD_df = pd.DataFrame(results_SD)
    
    os.makedirs(output_dir, exist_ok=True)
    NS_df.to_csv(os.path.join(output_dir, 'channel_specparam_NS.csv'), index=False)
    SD_df.to_csv(os.path.join(output_dir, 'channel_specparam_SD.csv'), index=False)

    print(f"\nSaved results → {output_dir}/specparam_NS.csv & specparam_SD.csv")
    return NS_df, SD_df
                
                           
            
    
      

