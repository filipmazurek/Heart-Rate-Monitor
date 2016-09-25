clear 

% Make a sin wave for testing that will be 60 bpm. Then append to another 
% that will be 100 bpm, then another.. To test that the min averages can
% update correctly.

bpm = 60; % actual bpm x2 this becuase of absolute value finding
hz = 100;
secondsOfData = 240;

bps = bpm / 60; % how many sin waves per second
samples =  hz * secondsOfData;

time = linspace(0, secondsOfData, samples);
output_for_one = uint16(abs((sin(bps* 2.*pi.*time) .* 100))); % give arbitrary scaling
n=2; % make each data point repeat twice
x = output_for_one';
r=repmat(x,1,n)';
r=r(:)';

fileID = fopen('HRTester.bin', 'a');
% fwrite(fileID, hz, 'uint16');
fwrite(fileID, r, 'uint16');
fclose(fileID);