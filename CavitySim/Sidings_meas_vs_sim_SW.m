
%verglijking tussen meting en simulatie voor de eerste dagen van februari

clear
clc
load('C:\PostDoc\Meetopstelling Vliet\DATA\OVERZICHT\RH_TC\.mat')
load('C:\PostDoc\Meetopstelling Vliet\DATA\OVERZICHT\METEO\METEO.mat')
load('C:\PostDoc\Meetopstelling Vliet\DATA\OVERZICHT\PRES\.mat')


%t
filerv='C:\PostDoc\SIMULATIES\IMPACT CLADDING\SIDINGS VLIET\VLIET\WAND23_SW.results\T_surf.out';
fid = fopen(filerv, 'rt');
a = textscan(fid, '%f %f','Delimiter',',', 'CollectOutput',0, 'HeaderLines',13);  
t_sim=cell2mat(a(:,2));

filerv='C:\PostDoc\SIMULATIES\IMPACT CLADDING\SIDINGS VLIET\VLIET\WAND23_SW_zon.results\T_surf.out';
fid = fopen(filerv, 'rt');
a = textscan(fid, '%f %f','Delimiter',',', 'CollectOutput',0, 'HeaderLines',13);  
t_sim1=cell2mat(a(:,2));

filerv='C:\PostDoc\SIMULATIES\IMPACT CLADDING\SIDINGS VLIET\VLIET\WAND23_SW_zon2.results\T_surf.out';
fid = fopen(filerv, 'rt');
a = textscan(fid, '%f %f','Delimiter',',', 'CollectOutput',0, 'HeaderLines',13);  
t_sim2=cell2mat(a(:,2));

filerv='C:\PostDoc\SIMULATIES\IMPACT CLADDING\SIDINGS VLIET\VLIET\WAND23_SW_zon3.results\T_surf.out';
fid = fopen(filerv, 'rt');
a = textscan(fid, '%f %f','Delimiter',',', 'CollectOutput',0, 'HeaderLines',13);  
t_sim3=cell2mat(a(:,2));


s=[datenum('01.02.2014 09:00:00','dd.mm.yyyy HH:MM:SS')]; 
e=[datenum('30.06.2014 18:00:00','dd.mm.yyyy HH:MM:SS')];

s_t=min(find(W23A3MTC(:,1)>=s));
e_t=max(find(W23A3MTC(:,1)<=e));
s_ex=min(find(temp_ex(:,1)>=s));
e_ex=max(find(temp_ex(:,1)<=e));

tijd_meas=aver_matrix(W23A3MTC(s_t:e_t,1),6);
t_3_meas=aver_matrix(W23A3MTC(s_t:e_t,:),6);
t_2_meas=aver_matrix(W23A2MTC(s_t:e_t,:),6);
t_4_meas=aver_matrix(W23A4MTC(s_t:e_t,:),6);
t_5_meas=aver_matrix(W23A5MTC(s_t:e_t,:),6);
t_ex=aver_matrix(temp_ex(s_ex:e_ex,:),6);
rad_ex=aver_matrix(rad_ex(s_ex:e_ex,:),6);

% hier pas je aan waar je wilt bekijken
%s=[datenum('24.05.2014 09:00:00','dd.mm.yyyy HH:MM:SS')]; 
%e=[datenum('08.06.2014 18:00:00','dd.mm.yyyy HH:MM:SS')];

 s=[datenum('01.02.2014 09:00:00','dd.mm.yyyy HH:MM:SS')]; 
 e=[datenum('14.02.2014 18:00:00','dd.mm.yyyy HH:MM:SS')];


aa=[datenum('01.01.2014 01:00:00','dd.mm.yyyy HH:MM:SS')]; 
bb=[datenum('01.01.2014 02:00:00','dd.mm.yyyy HH:MM:SS')]; 
eind=30*24*6
for i=1:eind
    tijd_sim(i)=aa+(bb-aa)*(i-1);
end
s_s=min(find(tijd_sim>=s));
e_s=max(find(tijd_sim<=e));


s_v=min(find(t_2_meas(:,1)>=s));
e_v=max(find(t_2_meas(:,1)<=e));
s_ex=min(find(t_ex(:,1)>=s));
e_ex=max(find(t_ex(:,1)<=e));



figure1=figure('Position',[200 50 900 500]);
subplot('Position',[0.08 0.81 0.85 0.15]);
plot(rad_ex(s_ex:e_ex,1),rad_ex(s_ex:e_ex,2),'k')
axis([rad_ex(s_ex,1) rad_ex(e_ex,1) 0 500])
datetick('x','dd/mm')
ylabel('Global rad. W/m²')

subplot('Position',[0.08 0.08 0.85 0.65]);
plot(tijd_sim(s_s:e_s),t_sim(s_s:e_s),'r')
hold on
plot(tijd_sim(s_s:e_s),t_sim1(s_s:e_s),'r')
plot(tijd_sim(s_s:e_s),t_sim2(s_s:e_s),'r')
plot(tijd_sim(s_s:e_s),t_sim3(s_s:e_s),'r')
plot(t_2_meas(s_v:e_v,1),t_2_meas(s_v:e_v,2),'g')
plot(t_2_meas(s_v:e_v,1),t_5_meas(s_v:e_v,2),'b')
plot(t_ex(s_ex:e_ex,1),t_ex(s_ex:e_ex,2),'k')
%axis([t_ex(s_ex,1) t_ex(e_ex,1) -5 40])
datetick('x','dd/mm')
ylabel('Temperature (°C)')
legend('SIM-cav','MEAS-cav','MEAS-surf','Exterior')
%saveas(1, 'sidings_sim_temp1', 'png')





figure
plot(t_sim(s_s:e_s),t_2_meas(s_v:e_v+2,2),'bo')
hold on
plot(t_sim1(s_s:e_s),t_2_meas(s_v:e_v+2,2),'ro')
plot(t_sim2(s_s:e_s),t_2_meas(s_v:e_v+2,2),'yo')

A=[5:1:35]
hold on
plot(A,A,'k')
plot(A,A*1.10,'k--')
plot(A,A*0.9,'k--')
ylabel('Measured temperature (°C)')
xlabel('Simulated temperature (°C)')
%saveas(2, 'sidings_sim_temp2', 'png')



x=t_sim(s_s:e_s);
y=t_2_meas(s_v:e_v+2,2);
p=polyfit(x,y,1)
yfit = polyval(p,x);
yfit =  p(1) * x + p(2);
yresid = y - yfit;
SSresid = sum(yresid.^2);
SStotal = (length(y)-1) * var(y);
rsq = 1 - SSresid/SStotal
plot(x,yfit,'m')

x=t_sim1(s_s:e_s);
y=t_2_meas(s_v:e_v+2,2);
p=polyfit(x,y,1)
yfit = polyval(p,x);
yfit =  p(1) * x + p(2);
yresid = y - yfit;
SSresid = sum(yresid.^2);
SStotal = (length(y)-1) * var(y);
rsq = 1 - SSresid/SStotal
plot(x,yfit,'g')

x=t_sim2(s_s:e_s);
y=t_2_meas(s_v:e_v+2,2);
p=polyfit(x,y,1)
yfit = polyval(p,x);
yfit =  p(1) * x + p(2);
yresid = y - yfit;
SSresid = sum(yresid.^2);
SStotal = (length(y)-1) * var(y);
rsq = 1 - SSresid/SStotal
plot(x,yfit,'r')














