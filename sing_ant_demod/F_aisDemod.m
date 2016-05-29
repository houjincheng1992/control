function demodResult = F_aisDemod(sig)
% ----
% ������Ϊ���AIS�źŽ������
% ����:
%	sig:����Ĵ��������GMSK�ź�, Ϊm*n����, nΪ�źų�������, mΪ�����ź�������
% ���:
%	demodResult:������, dataΪ�����ȷ��Ϣ(����֡���ӱ���), posΪ�����ȷ
%				�ĳ�����λ��, slotNumΪ��ʱ϶��, parΪ�����ȷ�źŵĲ�������
% ----
	% ȫ�ֱ�������
	global Start_pos BlockLength os DecodLenth ant_num TrainingLength FlagLength
	Start_pos = 1;
	if size(sig, 1) > size(sig, 2)
		sig = sig.';
    end
    
      % test ���Զ����ߺ�˫��������ʱ���õ����߳�����������ź�
    if size(sig,1) ~= 1
        sig = sig(1,:);
    end
    
	aisData_all = cell(0);
	sigPos_all = zeros(0, 2);
	parsEst_all = zeros(0, 2);
	% ���ҵ�һ���ź�λ��, flagΪ1���ҵ�ͬ���ı�־
	End_pos = min(length(sig),Start_pos+2*DecodLenth*os-1);       % ��ȡ2*DecodLength*os����Ϣ����, ��֤���볤�����ҵ���ͬ��λ�����һ�����볤����������
	Delay = zeros(1, size(sig, 1));
	flag = zeros(1, size(sig,1));
%     allDelay=zeros(1,1);
%     allFreq=zeros(1,1);
%     i=0;
	while Start_pos<length(sig) && End_pos-Start_pos>=BlockLength*os-1
		SlotCutIdx = Start_pos:End_pos;     % ��ȡ��Ϣ��ȫ����Ϣ�еı��
		sig_ch = sig(:,SlotCutIdx);
		for ant_num = 1 : size(sig,1)
			% �Ը�ͨ���źŽ����ŵ����� �� VA������ź�ͬ��
			[Delay(ant_num), dopplerEst, hEst, flag(ant_num), decisionSeq, match_len, startIndex] = ...
				F_channelEstAndDemod(sig_ch(ant_num,:));
        end
%                         i=i+1;
%         allDelay(i)=Delay(ant_num)
%          allFreq(i)=dopplerEst
		if all(flag == 0)
			% �������߶�û���ҵ�ͬ��, ����������������С��ʱ�ӹ�����ͬ��
			Start_pos = max(1, Start_pos+min(Delay));
			End_pos = min(length(sig), Start_pos+2*DecodLenth*os-1);
			continue;
		else
			% ���ź��ҵ�ͬ��, ֤�����ǿ�ʼ����, ��ǰһ�ξ������¿�ʼͬ�������
			Start_pos = max(1, Start_pos+min(Delay)-10*os);      % ӦΪ110bit, ��Ϊ�źŵ������ǵ������ʱΪ110bit, �˴�Ϊ����ʱ��10bit
			End_pos = min(length(sig), Start_pos+2*DecodLenth*os-1);
			break;
		end
	end

	Block_count = 0;
	% �����ź�λ��, ���ҵ�����
	while Start_pos<length(sig)&& End_pos-Start_pos>=BlockLength*os-1
		% ȷ����һ���źŵ�λ��, ��ͬ����ʼ����ź�
		SlotCutIdx = Start_pos:End_pos;
		sig_ch = sig(:,SlotCutIdx);
        for ant_num = 1:size(sig,1)
			% �Ը�ͨ���źŽ����ŵ����� �� VA������ź�ͬ��
			[Delay(ant_num), dopplerEst, hEst, flag(ant_num), decisionSeq, match_len, startIndex] = ...
				F_channelEstAndDemod(sig_ch(ant_num,:));
        end
%         Delay(ant_num)
		if all(flag==0)
			% �������߶�û���ҵ�ͬ��, ��������������С��ʱ�ӹ�����ͬ��
			Start_pos = Start_pos+min(Delay);
			End_pos = min(length(sig),Start_pos+2*DecodLenth*os-1);
			continue;
		end
		
		% ����ͬ��λ�ý�ȡ�ź�
		SlotCutIdx = Start_pos : End_pos;
		SigLength = length(SlotCutIdx);
		if SigLength < BlockLength*os
			break;
		end
		Block_count = Block_count + 1;
		disp('==========================');
		disp(['ʱ϶: ' num2str(Block_count)]);
		disp(['��ʼλ��: ', num2str(Start_pos)]);
		for ant_num = 1 : 1 : size(sig,1)
			% �Ը��źŵ����߽��
			sig_ch = sig(ant_num,SlotCutIdx);
			[sig_ch_sic, aisData, sigPos, parsEst] = F_singleAntDemod(sig_ch);
            %test
            if length(aisData) > 0
                for iii = 1 : 1 : length(aisData)
                   curData = aisData{iii};
                   curData(curData == ' ') = [];
                   disp(['�����߽�����', curData]);
                end
            end
            %test end
			aisData_all = [aisData_all aisData];
			sigPos_all = [sigPos_all; sigPos];
			parsEst_all = [parsEst_all; parsEst];
% 			sig(ant_num,SlotCutIdx) = sig_ch_sic;
%           [sig_ch_sic1, aisData, sigPos, parsEst] = F_singleAntDemod(sig_ch_sic);
% 			aisData_all = [aisData_all aisData];
% 			sigPos_all = [sigPos_all; sigPos];
% 			parsEst_all = [parsEst_all; parsEst];  
            
			num_of_checked = length(aisData_all);          % ��������м�¼����ź�
			disp(['������ȷ���ĸ�����',num2str(num_of_checked)]);
		end
		Start_pos = Start_pos+(BlockLength-TrainingLength-FlagLength)*os;
		% 	    Start_pos = Start_pos+2*4*9600;
		End_pos = min(length(sig),Start_pos+2*DecodLenth*os-1);
	end
    % ɾ���ظ���֡
%     [sigPos_all_uni, ind_uni] = unique(sigPos_all, 'rows', 'stable');
% 	demodResult.data = aisData_all(ind_uni);
% 	demodResult.pos = sigPos_all_uni;
% 	demodResult.slotNum = Block_count;
% 	demodResult.par = parsEst_all(ind_uni, :);
	
	demodResult.data = aisData_all;
	demodResult.pos = sigPos_all;
	demodResult.slotNum = Block_count;
	demodResult.par = parsEst_all;
end