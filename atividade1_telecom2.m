clear all
close all
clc
%% Gerando Vetores
% intervalo de tempo entre amostras

A = 1; % Amplitudade
deltaT = 0.0001; % ou Fs = 10000 e deltaT = 1/Fs : deltaT = 1e-4;

T0 = 0;      % instante inicial

Tf = 0.02;   % instante final

Tempo = T0:deltaT:Tf; % vetor tempo

% vetor de amostras para x(t) = cos 100πt

Xt = A*cos(100*pi*Tempo);

% caso Xt tenha limitações para sua representação? (A/D de N bits)

N=10; % número de bits. use também 8, 6 e 4

mi = min(Xt);
Xi = Xt - mi; % retirar os valores negativo da curva
ma = max(Xi);
Xnorm = Xi ./ma; %normalizar a curva compatível com o número de níveis
Yt = ma* round(Xnorm*(2^(N)-1))./(2^(N)-1); % retira a normalização e
Yt = Yt + round(mi); % retorna os valores negativos.

delta = (ma-mi)/(2^N - 1);
erro_absoluto = delta/2;

figure(1)
title(string([num2str(N) ' bits.' ' Erro absoluto de ' num2str(erro_absoluto)]))
hold all

plot(Tempo,Xt); % plotando sinal contínuo 


plot(Tempo,Yt);
saveas(gcf, string([num2str(N) 'bits_' 'erro_' num2str(erro_absoluto) '_continuo' '.png']))
figure (2)

title(string([num2str(N) ' bits.' ' Erro absoluto de ' num2str(erro_absoluto)]))

hold all

stem(Tempo,Xt); % plotando sinal discreto

stem(Tempo,Yt);
saveas(gcf, string([num2str(N) 'bits_' 'erro_' num2str(erro_absoluto) '_stem' '.png']))
