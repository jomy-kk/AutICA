%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  PDSB Project 2021
%
%  Module: EEELAB
%  File: separate_train_test_set
%
%  Created on July 1, 2021
%  Last modified on July 1, 2021
%
%  Code rights reserved to João Saraiva
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_path = "/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/data/";

n_train_epochs = 1600;
subject = 15;
session = 6;

%for subject = 1:15
 %  for session = 1:7
        if (subject < 10)
            subject_code = strcat("SBJ0", int2str(subject));
        else
            subject_code = strcat("SBJ", int2str(subject));
        end
        session_code = strcat("S0", int2str(session));
        subject_session_data_path = strcat(data_path, subject_code, '/', session_code , '/');

        % Find pruned datasets
        filesList = dir(subject_session_data_path);
        serialList = regexpi({filesList.name}, '.+(pruned).+(.set)', 'match');
        pruned_datasets = vertcat(serialList{:});

        % Separate datasets in train and test subsets
        for i = 1:length(pruned_datasets)
            dataset_name = pruned_datasets{i, 1};
            dataset = pop_loadset(dataset_name, convertStringsToChars(subject_session_data_path));
            dataset = dataset.data;
            %dataset = normalize(dataset, 2);
            trainData = dataset(:, :, 1:n_train_epochs);
            testData = dataset(:, :, n_train_epochs+1:length(dataset(1,1,:)));
            save(strcat(subject_session_data_path, 'Train/train_', dataset_name(1:length(dataset_name)-4), '.mat'), 'trainData');
            save(strcat(subject_session_data_path, 'Test/test_', dataset_name(1:length(dataset_name)-4), '.mat'), 'testData');
            disp("Separated");
        end 
 %   end   
%end

