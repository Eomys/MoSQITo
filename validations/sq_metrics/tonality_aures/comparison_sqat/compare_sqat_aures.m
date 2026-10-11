function compare_sqat_aures(sqat_root, mosqito_root)
% compare_sqat_aures  Run SQAT's Tonality_Aures1985 on a fixed set of test signals.
%
%   compare_sqat_aures(sqat_root, mosqito_root)
%
%   Runs SQAT's Aures tonality on deterministic signals (sums of zero-phase
%   sinusoids, generated here with the same formula as the Python side) and
%   on the nine Tonality_Aures1985 validation WAV files stored in the
%   MoSQITo fork, then writes sqat_aures_results.csv next to this file.
%
%   Nothing is modified in either repository. SQAT (GPL-3.0) is only run,
%   not copied: this script contains no SQAT code.
%
%   Inputs
%     sqat_root    : folder of the SQAT clone (contains psychoacoustic_metrics/)
%     mosqito_root : folder of the MoSQITo_zhenxian clone (branch master, 10b4ab2
%                    or later, which holds the validation WAV files)

if nargin < 1 || isempty(sqat_root),    error('give the folder of the SQAT clone as first argument'); end
if nargin < 2 || isempty(mosqito_root), mosqito_root = fileparts(fileparts(fileparts(fileparts(fileparts(mfilename('fullpath')))))); end

addpath(genpath(sqat_root));
here = fileparts(mfilename('fullpath'));

[~, sqat_commit] = system(sprintf('git -C "%s" rev-parse --short HEAD', sqat_root));
sqat_commit = strtrim(sqat_commit);
[~, sqat_date] = system(sprintf('git -C "%s" log -1 --format=%%cs', sqat_root));
sqat_date = strtrim(sqat_date);

fs  = 48000;   % Hz, SQAT accepts 44.1 or 48 kHz without resampling
dur = 2;       % s, gives 15 frames of 250 ms with 50 % overlap

cases = struct('name', {}, 'desc', {}, 'x', {}, 'fs', {});
cases(end+1) = mk('ref',     '1000 Hz 60 dB',                      tone(fs, dur, 1000, 60), fs);
for f = [1000 1003 1006.25 1009]
    cases(end+1) = mk(sprintf('bin_%g', f), sprintf('%g Hz 60 dB', f), tone(fs, dur, f, 60), fs); %#ok<AGROW>
end
cases(end+1) = mk('two_A',   '1000 Hz 60 dB + 1500 Hz 30 dB',      tone(fs, dur, 1000, 60) + tone(fs, dur, 1500, 30), fs);
cases(end+1) = mk('two_B',   '1000 Hz 60 dB + 1200 Hz 40 dB',      tone(fs, dur, 1000, 60) + tone(fs, dur, 1200, 40), fs);
cases(end+1) = mk('three',   '500 + 1000 + 2000 Hz, 50 dB each',   tone(fs, dur, 500, 50) + tone(fs, dur, 1000, 50) + tone(fs, dur, 2000, 50), fs);
for L = [40 50 60 70 80]
    cases(end+1) = mk(sprintf('level_%d', L), sprintf('1000 Hz %d dB', L), tone(fs, dur, 1000, L), fs); %#ok<AGROW>
end
for f = [250 500 2000 4000]
    cases(end+1) = mk(sprintf('freq_%d', f), sprintf('%d Hz 60 dB', f), tone(fs, dur, f, 60), fs); %#ok<AGROW>
end

% the SQAT validation WAV files kept in the MoSQITo fork (64-bit float, pascals)
wavdir = fullfile(mosqito_root, 'validations', 'sq_metrics', 'tonality_aures', 'input', 'Tonality_Aures1985');
wavs = dir(fullfile(wavdir, '*.wav'));
for k = 1:numel(wavs)
    [x, fsw] = audioread(fullfile(wavdir, wavs(k).name), 'native');
    x = double(x(:, 1));
    tok = regexp(wavs(k).name, 'prominence_(\d+)dB', 'tokens', 'once');
    cases(end+1) = mk(sprintf('wav_%02ddB', str2double(tok{1})), wavs(k).name, x, fsw); %#ok<AGROW>
end

out = fullfile(here, 'sqat_aures_results.csv');
fid = fopen(out, 'w');
fprintf(fid, '# SQAT commit %s (%s), MATLAB %s, generated %s\n', sqat_commit, sqat_date, version, datestr(now, 'yyyy-mm-dd HH:MM'));
fprintf(fid, 'case,description,fs,nframes,K_mean,K_max,K_median,wT_mean,wGr_mean\n');
fprintf('%-12s %-36s %8s %8s %8s %8s %8s\n', 'case', 'description', 'K_mean', 'K_max', 'K_med', 'wT', 'wGr');
for k = 1:numel(cases)
    c = cases(k);
    OUT = Tonality_Aures1985(c.x, c.fs, 0, 0, 0);   % free field, no time skip, no plot
    K   = OUT.InstantaneousTonality(:);
    wT  = OUT.TonalWeighting(:);
    wGr = OUT.LoudnessWeighting(:);
    fprintf(fid, '%s,"%s",%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f\n', c.name, c.desc, c.fs, numel(K), ...
        mean(K), max(K), median(K), mean(wT), mean(wGr));
    fprintf('%-12s %-36s %8.4f %8.4f %8.4f %8.4f %8.4f\n', c.name, c.desc, mean(K), max(K), median(K), mean(wT), mean(wGr));
end
fclose(fid);
fprintf('\nwritten: %s\nSQAT commit %s (%s)\n', out, sqat_commit, sqat_date);
end

function c = mk(name, desc, x, fs)
c = struct('name', name, 'desc', desc, 'x', x(:), 'fs', fs);
end

function x = tone(fs, dur, f, spl)
% zero-phase sinusoid in pascals; identical formula on the Python side
t = (0:round(fs * dur) - 1).' / fs;
x = sqrt(2) * 2e-5 * 10^(spl / 20) * sin(2 * pi * f * t);
end
