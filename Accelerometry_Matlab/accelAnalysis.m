clear;
filename = "D:\University\Year 3\Dissertation\Accelerometer\AcelDemo.txt";
%fileID = fopen("filename, 'r');
%A = fscanf(fileID, '%f');
T = readtable(filename);
%remove unneccesary collumns
T(:,8) = [];
T(:,6) = [];
T(:,4) = [];
T(:,2) = [];
T(:,1) = [];
%convert table to cell to make manipulation easier
C = table2cell(T);
%isolating the data into their own files
posn = 1;
for i = 1:2:length(C)      %Isolates the data into their own arrays
    L(posn,:) = C(i,1:4);
    R(posn,:) = C(i+1,1:4);
    posn = posn + 1;
end
%Setting the time to t = 0
for i = 2:length(L)
    L{i,1} = L{i,1} - L{1,1};
    R{i,1} = R{i,1} - R{1,1};
end
L{1,1} = L{1,1} - L{1,1};
R{1,1} = R{1,1} - R{1,1};
%Converting the time variable from type duration to double
for i = 1:length(L)
    L{i,1} = seconds(L{i,1});
    R{i,1} = seconds(R{i,1});
end
%converting from cell array to double array
L = cell2mat(L);
R = cell2mat(R);


%%Plotting the results
figure(1)
sgtitle("Accelerometer Data of the GRUE System Game Being Played")

%Left Hand Plots
%LX
subplot(2,3,1)
plot(L(:,1),L(:,2))
grid on
xlabel("Time, s")
ylabel("XL Acceleration, g")
title("Left Side: X")

%Ly
subplot(2,3,2)
plot(L(:,1),L(:,3))
grid on
xlabel("Time, s")
ylabel("YL Acceleration, g")
title("Left Side: Y")

%Lz
subplot(2,3,3)
plot(L(:,1),L(:,4))
grid on
xlabel("Time, s")
ylabel("ZL Acceleration, g")
title("Left Side: Z")


%Right Hand Plots
%RX
subplot(2,3,4)
plot(R(:,1),R(:,2))
grid on
xlabel("Time, s")
ylabel("XR Acceleration, g")
title("Right Side: X")

%Ry
subplot(2,3,5)
plot(R(:,1),R(:,3))
grid on
xlabel("Time, s")
ylabel("YR Acceleration, g")
title("Right Side: Y")

%Rz
subplot(2,3,6)
plot(R(:,1),R(:,4))
grid on
xlabel("Time, s")
ylabel("ZR Acceleration, g")
title("Right Side: Z")


% %RX
% subplot(2,3,2)
% title("Right Side: X")
% plot(R(:,1),R(:,2), '-x')
% grid on
% xlabel("Time, s")
% ylabel("XR Acceleration, g")
% %LY
% subplot(2,3,3)
% title("Left Side: Y")
% plot(L(:,1),L(:,3), '-x')
% grid on
% xlabel("Time, s")
% ylabel("YL Acceleration, g")
% %RY
% subplot(2,3,4)
% title("Right Side: Y")
% plot(R(:,1),R(:,3), '-x')
% grid on
% xlabel("Time, s")
%ylabel("YR Acceleration, g")


