%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  PDSB Project 2021
%
%  Module: EEELAB
%  File: analysis_protocol
%
%  Created on July 1, 2021
%  Last modified on July 2, 2021
%
%  Code rights reserved to João Saraiva
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_path = "/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/data/";
results_path = "/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/results/";

sf = 250; % Hz
time_points = 350; % samples
t0 = -0.2; % seconds
n_channels = 8;
n_train_epochs = 1600;

subject = 8; 
session = 7;
ica_algorithm = 'picard';

% Initialize EEGLAB session
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;


if (subject < 10)
    subject_code = strcat("SBJ0", int2str(subject));
else
    subject_code = strcat("SBJ", int2str(subject));
end

session_code = strcat("S0", int2str(session));

subject_session_data_path = strcat(data_path, subject_code, '/', session_code , '/');
subject_session_results_path = strcat(results_path, subject_code, '/', session_code, '/');


% Load train set
EEG = pop_importdata('dataformat','matlab','nbchan',n_channels,'data', strcat(subject_session_data_path, 'Train/trainData.mat'),'srate',sf,'pnts',time_points,'xmin',t0, 'subject', subject_code, 'session', session);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 

% Load test set
EEG = pop_importdata('dataformat','matlab','nbchan',n_channels,'data', strcat(subject_session_data_path, 'Test/testData.mat'),'srate',sf,'pnts',time_points,'xmin',t0, 'subject', subject_code, 'session', session);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'gui','off'); 

% Append train + test epochs in a single dataset
EEG = eeg_checkset( EEG );
EEG = pop_mergeset( ALLEEG, [1  2], 0); % merge
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'setname','Merged subsets','gui','off'); 


% Associate channel locations
EEG = eeg_checkset( EEG );
EEG=pop_chanedit(EEG, 'load',[],'changefield',{1,'labels','C3'},'append',1,'changefield',{2,'labels','Cz'},'append',2,'changefield',{3,'labels','C4'},'append',3,'changefield',{4,'labels','CPz'},'append',4,'changefield',{5,'labels','P3'},'append',5,'changefield',{6,'labels','Pz'},'append',6,'changefield',{7,'labels','P4'},'append',7,'changefield',{8,'labels','POz'},'changefield',{8,'datachan',1},'changefield',{7,'datachan',1},'changefield',{6,'datachan',1},'changefield',{5,'datachan',1},'changefield',{4,'datachan',1},'changefield',{3,'datachan',1},'changefield',{2,'datachan',1});
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
EEG = eeg_checkset( EEG );
EEG=pop_chanedit(EEG, 'lookup','/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/eeglab2021.0/plugins/dipfit4.1/standard_BEM/elec/standard_1005.ced');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% Trim epochs in time [0, 10000] ms, regarding to onset
EEG = eeg_checkset( EEG );
EEG = pop_select( EEG, 'time',[0 1] );

% Save dataset as SBJXX-SYY
dataset_name = subject_code + "-" + session_code;
file_path = convertStringsToChars(subject_session_data_path + dataset_name + ".set");
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 3,'setname',dataset_name,'savenew', file_path,'gui','off'); 


%% Before ICA: Not-p300 subset

% Load train not-p300 indices
fileID = fopen(strcat(subject_session_data_path, 'Train/not_p300_indices.txt'), 'r');
train_not_p300_indices = fscanf(fileID, '%i');

% Load test not-p300 indices
fileID = fopen(strcat(subject_session_data_path, 'Test/not_p300_indices.txt'), 'r');
test_not_p300_indices = fscanf(fileID, '%i');

% Join not-p300 indices
test_not_p300_indices = test_not_p300_indices + n_train_epochs; % shift indices of test set
not_p300_indices = vertcat(train_not_p300_indices,test_not_p300_indices); % concatenate train and test indices

% Filter not-P300 trials
EEG = eeg_checkset( EEG );
EEG = pop_select( EEG, 'trial', not_p300_indices);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'setname', strcat(dataset_name, '-not-p300'),'gui','off'); 

% ERP image of channel Cz
EEG = eeg_checkset( EEG );
figure; pop_erpimage(EEG,1, [2],[[]],'Cz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [2] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'beforeICA_not-p300_ERP_Cz.png'));
close(gcf)

% ERP image of channel Pz
EEG = eeg_checkset( EEG );
figure; pop_erpimage(EEG,1, [6],[[]],'Pz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [6] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'beforeICA_not-p300_ERP_Pz.png'));
close(gcf)

%% Before ICA: p300-only subset

% Load train p300 indices
fileID = fopen(strcat(subject_session_data_path, 'Train/p300_indices.txt'), 'r');
train_p300_indices = fscanf(fileID, '%i');

% Load test p300 indices
fileID = fopen(strcat(subject_session_data_path, 'Test/p300_indices.txt'), 'r');
test_p300_indices = fscanf(fileID, '%i');

% Join p300 indices
test_p300_indices = test_p300_indices + n_train_epochs; % shift indices of test set
p300_indices = vertcat(train_p300_indices, test_p300_indices); % concatenate train and test indices

% Filter p300 trials
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 5,'retrieve',4,'study',0); 
EEG = eeg_checkset( EEG );
EEG = pop_select( EEG, 'trial', p300_indices);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'setname', strcat(dataset_name, '-p300-only'),'gui','off'); 

% ERP image of channel Cz
EEG = eeg_checkset( EEG );
figure; pop_erpimage(EEG,1, [2],[[]],'Cz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [2] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'beforeICA_p300-only_ERP_Cz.png'));
close(gcf)

% ERP image of channel Pz
EEG = eeg_checkset( EEG );
figure; pop_erpimage(EEG,1, [6],[[]],'Pz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [6] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'beforeICA_p300-only_ERP_Pz.png'));
close(gcf)

% Plot ERP image of all channels
figure;
pop_timtopo(EEG, [200  550], [NaN], convertStringsToChars("ERP data and scalp maps of " + dataset_name + " (p300-only)"));
saveas(gcf, strcat(subject_session_results_path, 'beforeICA_all_channels_ERP_p300-only.png'));
close(gcf)


%% Doing ICA: full set

% FastICA approach
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 6,'retrieve',4,'study',0); 
EEG = eeg_checkset( EEG );
timer = tic();
EEG = pop_runica(EEG, 'icatype', ica_algorithm);
time_elapsed = toc(timer);
disp("This ICA algorithm toke " + time_elapsed + " seconds")
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% Save weights
EEG = eeg_checkset( EEG );
file_name = convertStringsToChars(dataset_name + "-" + ica_algorithm + ".set");
EEG = pop_saveset( EEG, 'filename', file_name,'filepath', convertStringsToChars(subject_session_data_path));
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% Obraining dipoles estimation of ICs
EEG = eeg_checkset( EEG );
%EEG = pop_dipfit_settings( EEG, 'hdmfile','/Applications/EEGLAB/application/EEGLAB.app/Contents/Resources/EEGLAB_mcr/EEGLAB/plugins/dipfit/standard_BEM/standard_vol.mat','coordformat','MNI','mrifile','/Applications/EEGLAB/application/EEGLAB.app/Contents/Resources/EEGLAB_mcr/EEGLAB/plugins/dipfit/standard_BEM/standard_mri.mat','chanfile','/Applications/EEGLAB/application/EEGLAB.app/Contents/Resources/EEGLAB_mcr/EEGLAB/plugins/dipfit/standard_BEM/elec/standard_1005.elc','coord_transform',[0 0 0 0 0 -1.5708 1 1 1] ,'chansel',[1:8] );
%[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
%EEG = pop_multifit(EEG, [1:8] ,'threshold',100,'plotopt',{'normlen','on'});
%[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% overwrite results path to be algortihm-specific
subject_session_results_path = strcat(subject_session_results_path, '/', ica_algorithm, '/');
if ~exist(subject_session_results_path, 'dir')
       mkdir(subject_session_results_path)
 end

% Plot components scalp maps
pop_topoplot(EEG, 0, [1:8] , convertStringsToChars(dataset_name),[3 3] ,0,'electrodes','on');
saveas(gcf, strcat(subject_session_results_path, 'ICA_components.png'));
close(gcf)

% Plot ERP envelope
pop_envtopo(EEG, [200  550] ,'limcontrib',[200 550],'compsplot',[3],'title', convertStringsToChars("Largest ERP components of " + dataset_name), 'electrodes','off');
saveas(gcf, strcat(subject_session_results_path, 'ICs_ERP_evelope.png'));
close(gcf)

% Plot ERP envelope (p300 only)
EEG = pop_select( EEG, 'trial', p300_indices);
%[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 7,'setname', strcat(dataset_name, "-" + ica_algorithm + '-p300-only'),'gui','off'); 
EEG = eeg_checkset( EEG );
pop_envtopo(EEG, [200  550] ,'limcontrib',[200 550],'compsplot',[8],'title', convertStringsToChars("All ERP components of " + dataset_name + " (p300 only)"), 'electrodes','off');
saveas(gcf, strcat(subject_session_results_path, 'ICs_ERP_evelope_p300-only.png'));
close(gcf)

% Classify ICs
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 6,'retrieve',4,'study',0); 
EEG = eeg_checkset( EEG );
EEG = pop_iclabel(EEG, 'default');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

% Here it should be given control to the user to choose the ICs to remove
% according to:
% -> % of not-brain related activity
% -> keep the ones that most contribute to the largest ERP (in envelope)
pop_viewprops(EEG, 0, 1:8, {'freqrange',[2 60] })
to_remove = input("Component indices to remove (array []): ");

% Remove components
EEG = pop_subcomp( EEG, to_remove, 0);

% Save dataset
file_path = convertStringsToChars(subject_session_data_path + dataset_name + "-" + ica_algorithm + "-pruned-" + num2str(to_remove) + ".set");
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'setname', dataset_name + "-" + ica_algorithm + "-pruned-" + num2str(to_remove), 'savenew', file_path,'gui','off'); 


%% After ICA: p300-only subset

EEG = pop_select( EEG, 'trial', p300_indices);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 7,'setname', strcat(dataset_name, "-" + ica_algorithm + '-p300-only'),'gui','off'); 

% Plot Component propreties panel
for i = 1:(8-length(to_remove))
   pop_prop( EEG, 0, i, NaN, {'freqrange',[2 50] });
   saveas(gcf, strcat(subject_session_results_path, 'afterICA_p300-only_IC', int2str(i), '.png'));
   close(gcf)
end

% Plot ERP envelope
pop_envtopo(EEG, [200  550] ,'limcontrib',[200 550],'compsplot',[3],'title', convertStringsToChars("Largest ERP components of " + dataset_name + " pruned with " + ica_algorithm + " (p300-only)"),'electrodes','off');
saveas(gcf, strcat(subject_session_results_path, 'afterICA_ICs_ERP_evelope_p300-only.png'));
close(gcf)

% Plot ERP image of all channels
figure;
pop_timtopo(EEG, [200  550], [NaN], convertStringsToChars("ERP data and scalp maps of " + dataset_name + " pruned with " + ica_algorithm + " (p300-only)"));
saveas(gcf, strcat(subject_session_results_path, 'afterICA_all_channels_ERP_p300-only.png'));
close(gcf)

% ERP image of channel Cz
figure; pop_erpimage(EEG,1, [2],[[]],'Cz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [2] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'afterICA_p300-only_ERP_Cz.png'));
close(gcf)

% ERP image of channel Pz
figure; pop_erpimage(EEG,1, [6],[[]],'Pz',10,1,{},[],'' ,'yerplabel','\muV','erp','on','cbar','on','topo', { [6] EEG.chanlocs EEG.chaninfo } );
saveas(gcf, strcat(subject_session_results_path, 'afterICA_p300-only_ERP_Pz.png'));
close(gcf)


disp("Analysis completed")


