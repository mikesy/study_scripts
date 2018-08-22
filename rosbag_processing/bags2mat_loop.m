%% data read script
% run once and use mats since reading bags takes significant time
clear all;
%% USER INPUTS for script

% mounted data or other data folder
DATAROOT = '~/Argall_Lab/data_temp/'; 
DATAROOT = '~/Argall_Lab/data_temp2/';
subjects = {'L01','L02','L03','L04'};
subjects = {'alex','deepak','nate'};
distractions = {'clean','math','nav','phone'};

tasks = {'turn','door'};

op_modes = {'tele','auto'};

%distractions = {'clean'};
%need to manually enter desired topics and field names for the data and
%time since it varies between topics
topics = {'joy',...
          'CAinfo',...
          'CAinfo',...
          'CAinfo',...
          'CAinfo',...
          'odom'};
            
topic_fields = {{'buttons'},...
                {'ucmd','linear'},...
                {'ucmd','angular'},...
                {'acmd','linear'},...
                {'acmd','angular'},...
                {'pose','pose','position'}};
             
time_fields = {{'header','stamp','time'},...
               {'ctime','time'},...
               {'ctime','time'},...
               {'ctime','time'},...
               {'ctime','time'},...
               {'header','stamp','time'}};
           
% topics = {'CAinfo'};
% topic_fields = {{'acmd','angular'}};
% time_fields = {{'ctime','time'}};
%input path for rosbag functions
addpath('~/Documents/MATLAB/matlab_rosbag-0.5.0-linux64/');


%% TO DO: ADD a file exist check for each distraction and subject
addpath('functions');
for i = 1:length(subjects)
    for j = 1:length(distractions)
        for k = 1:length(tasks)
            for l = 1:length(op_modes)
                bag_path = strcat(DATAROOT,subjects{i},'/bags/',subjects{i},'_',distractions{j},'_',tasks{k},'_',op_modes{l},'*.bag');
                mat_folder = strcat(DATAROOT,subjects{i},'/mats/');      % where mat files will store
                dat_folder = strcat(DATAROOT,subjects{i},'/dats/');
                prefix_label = strcat(subjects{i},'_',distractions{j},'_',tasks{k},'_',op_modes{l});  % used in file naming .mat files
                rosbags2mat(bag_path, mat_folder, dat_folder, prefix_label, topics, topic_fields, time_fields)
            end
        end
    end
end