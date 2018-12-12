function img2gif(image_cell, file_name, time_delay, color_num)
    % 将MATLAB图像转化为gif图.
    % Argus:
    %    image_cell:  Cell.
    %    file_name:   Char[].
    %    time_delay:  Double.
    %    color_num:   Integer.
    if nargin<4, color_num=20;  end
    if nargin<3, time_delay=.2; end
    if nargin<2, file_name='demo'; end
    len = length(image_cell);
    for i = 1:len
        [I,map] = rgb2ind(image_cell{i}, color_num); 
        if i == 1
           imwrite(I, map, [file_name, '.gif'], 'gif', 'Loopcount', inf, 'DelayTime', time_delay);
       else
           imwrite(I, map, [file_name, '.gif'], 'gif', 'WriteMode', 'append', 'DelayTime', time_delay);
       end
    end
end



% [filename, pathname] = uigetfile({'*.jpg;*.tif;*.png;*.gif',...
%                        'Ñ¡ÔñÍ¼Æ¬ÎÄ¼þ'});
% ¶ÁÈ¡ÎÄ¼þ
% pic_origin = imread(fullfile(pathname,filename));