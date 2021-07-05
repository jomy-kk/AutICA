%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  PDSB Project 2021
%
%  Module: EEELAB
%  File: remove_components_only
%
%  Created on July 4, 2021
%  Last modified on July 4, 2021
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

subject = 12; 
session = 3;
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
subject_session_results_path = strcat(subject_session_results_path, '/', ica_algorithm, '/');
dataset_name = subject_code + "-" + session_code;

% Load dataset with ICA weights
EEG = pop_loadset('filename', convertStringsToChars(strcat(dataset_name, '-', ica_algorithm, '.set')),'filepath', convertStringsToChars(subject_session_data_path));
[ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );


%% Redo remove ICs

% Here it should be given control to the user to choose the ICs to remove
% according to:
% -> % of not-brain related activity
% -> keep the ones that most contribute to the largest ERP (in envelope)
to_remove = input("Component indices to remove (array []): ");

% Remove components
EEG = pop_subcomp( EEG, to_remove, 0);

% Save dataset
file_path = convertStringsToChars(subject_session_data_path + dataset_name + "-" + ica_algorithm + "-pruned-" + num2str(to_remove) + ".set");
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'setname', dataset_name + "-" + ica_algorithm + "-pruned-" + num2str(to_remove), 'savenew', file_path,'gui','off'); 


%% After ICA: p300-only subset

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
EEG = eeg_checkset( EEG );
EEG = pop_select( EEG, 'trial', p300_indices);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'setname', strcat(dataset_name, "-" + ica_algorithm + '-p300-only'),'gui','off'); 

% Plot Component propreties panel
for i = 1:(8-length(to_remove))
   pop_prop( EEG, 0, i, NaN, {'freqrange',[2 50] });
   saveas(gcf, strcat(subject_session_results_path, 'afterICA_p300-only_IC', int2str(i), '.png'));
   close(gcf)
end

% Plot ERP envelope
pop_envtopo(EEG, [100  900] ,'limcontrib',[200 500],'compsplot',[3],'title', convertStringsToChars("Largest ERP components of " + dataset_name + " pruned with " + ica_algorithm + " (p300-only)"),'electrodes','off');
saveas(gcf, strcat(subject_session_results_path, 'afterICA_ICs_ERP_evelope_p300-only.png'));
close(gcf)

% Plot ERP image of all channels
figure;
pop_timtopo(EEG, [200  500], [NaN], convertStringsToChars("ERP data and scalp maps of " + dataset_name + " pruned with " + ica_algorithm + " (p300-only)"));
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


disp("Analysis redone")


