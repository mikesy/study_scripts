function rosbags2mat(bag_path, mat_folder, dat_folder, prefix_label, topics, topic_fields, time_fields)
%% REQUIRED: addpath('~/Documents/MATLAB/matlab_rosbag-0.5.0-linux64/')
% add before function call (location depends on installation) or manually using gui

%% inputs (FIX!! for ease of understanding)
% inputs (all as strings ' ')
% bag_path = bag name 
% pat_num  = randomly assigned patient number
% op_num   = operational mode 

%% 

clear rosbag_wrapper;
clear ros.Bag;
format long;


%% Load a bag and get information about it
% Using load() lets you auto-complete filepaths.
% grab some basic bag info and save it to .mat files
bag = ros.Bag.load(bag_path);
bag_info = bag.info();
ros_start = bag.time_begin;
file = strcat(mat_folder,prefix_label,'_baginfo');   %ROS bag info
save(file,'bag_info');
file = strcat(dat_folder,prefix_label,'_baginfo.dat');   %ROS bag info
csvwrite(file,bag_info);
file = strcat(mat_folder,prefix_label,'_ros_start'); %ROS bag start time
save(file,'ros_start');
file = strcat(dat_folder,prefix_label,'_ros_start.dat');
csvwrite(file, ros_start)

fprintf('Reading bag %s \n', bag_path);

for i = 1:length(topics)
    if i == 1 
        data = bag.readAll(strcat('/',topics{i}));
        
    elseif strcmp(topics{i},topics{i-1})==0
        data = bag.readAll(strcat('/',topics{i}));
    else
        fprintf('skipping a new read on %s on topic number %i in list\n',topics{i},i);
    end
    
    n = length(data);
    m = length(getfield(data{1},{1},topic_fields{i}{:}));
    dwt = zeros(m+1, n);                                    % data with time matrix
    for j = 1:n
        t = getfield(data{j},{1},time_fields{i}{:});
        d = getfield(data{j},{1},topic_fields{i}{:});
        dwt(:,j) = [t; d];
    end
    dwt(1,:) = dwt(1,:) - ros_start;
    
    fn = strcat('_',topics{i});
    for j = 1:length(topic_fields{i})
       fn = strcat(fn,'_',topic_fields{i}{j}); 
    end
    file  = strcat(mat_folder,prefix_label,fn,'.mat');
    file_dat = strcat(dat_folder,prefix_label,fn,'.dat');
    
    save(file,'dwt');
    csvwrite(file_dat, dwt)
end

