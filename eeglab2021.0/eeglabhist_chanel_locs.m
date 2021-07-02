% EEGLAB history file generated on the 02-Jul-2021
% ------------------------------------------------
EEG = pop_loadset('filename','SBJ15-S01.set','filepath','/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/data/SBJ15/S01/');
[ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );
EEG = eeg_checkset( EEG );
EEG = pop_importdata('dataformat','matlab','nbchan',0,'data','/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/data/SBJ03/S04/Test/testData.mat','srate',250,'pnts',350,'xmin',0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'gui','off'); 
EEG = eeg_checkset( EEG );
EEG=pop_chanedit(EEG, 'load',[],'changefield',{1,'labels','C3'},'append',1,'changefield',{2,'labels','Cz'},'append',2,'changefield',{3,'labels','C4'},'append',3,'changefield',{4,'labels','CPz'},'append',4,'changefield',{5,'labels','P3'},'append',5,'changefield',{6,'labels','Pz'},'append',6,'changefield',{7,'labels','P4'},'append',7,'changefield',{8,'labels','POz'},'changefield',{8,'datachan',1},'changefield',{7,'datachan',1},'changefield',{6,'datachan',1},'changefield',{5,'datachan',1},'changefield',{4,'datachan',1},'changefield',{3,'datachan',1},'changefield',{2,'datachan',1});
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
EEG = eeg_checkset( EEG );
EEG=pop_chanedit(EEG, 'lookup','/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/eeglab2021.0/plugins/dipfit/standard_BEM/elec/standard_1005.elc');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
eeglab redraw;
