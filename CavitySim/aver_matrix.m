

%scriptje om uit te middelen, maakt niet uit hoe de matrix georienteerd, en
%delete ook lijste lijn




function [matrix_aver]= aver_matrix(matrix_in,n)

[numr numc]=size(matrix_in);


%opstaande matrix
if numr>numc
    matrix_aver=blkproc(matrix_in, [n 1], @mean);
    matrix_aver=(matrix_aver(1:end-1,:));
%liggende matrix    
else
    matrix_in_tr=transpose(matrix_in);
    matrix_aver=blkproc(matrix_in_tr, [n 1], @mean);
    matrix_aver=(matrix_aver(1:end-1,:));     
end






end