function compare_sqat_aures(sqat_root, sounds_dir)
% compare_sqat_aures  Run SQAT's Tonality_Aures1985 on a fixed set of test signals.
%
%   compare_sqat_aures(sqat_root)
%   compare_sqat_aures(sqat_root, sounds_dir)
%
%   Runs SQAT's Aures tonality on deterministic signals generated here with
%   the same formulas as the Python side (sums of zero-phase sinusoids, and
%   multisines with pseudo-random phases for narrowband noise), then writes
%   sqat_aures_results.csv (one row per signal, statistics over the frames)
%   and sqat_aures_frames.csv (one row per frame: the time series K(t) that
%   MoSQITo's tonality_aures_tv is compared with) next to this file. With a
%   second argument it also
%   runs the nine Tonality_Aures1985 validation sounds of the SQAT v1.x data
%   set (1 kHz tone at 82 dB SPL in one critical band of noise, Zenodo
%   doi:10.5281/zenodo.7933206); they are neither in the SQAT repository nor
%   shipped with MoSQITo.
%
%   Nothing is modified in either repository. SQAT (GPL-3.0) is only run,
%   not copied: this script contains no SQAT code.
%
%   Inputs
%     sqat_root  : folder of the SQAT clone (contains psychoacoustic_metrics/)
%     sounds_dir : optional, a folder holding the 1Bark_tone_prominence_*.wav
%                  files of the data set (searched recursively)

if nargin < 1 || isempty(sqat_root), error('give the folder of the SQAT clone as first argument'); end
if nargin < 2, sounds_dir = ''; end

addpath(genpath(sqat_root));
here = fileparts(mfilename('fullpath'));

[~, sqat_commit] = system(sprintf('git -C "%s" rev-parse --short HEAD', sqat_root));
sqat_commit = strtrim(sqat_commit);
[~, sqat_date] = system(sprintf('git -C "%s" log -1 --format=%%cs', sqat_root));
sqat_date = strtrim(sqat_date);

fs  = 48000;   % Hz, SQAT accepts 44.1 or 48 kHz without resampling
dur = 2;       % s, gives 14 frames of 250 ms with 50 % overlap

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

% narrowband noise, and a tone in it: multisines with 1 Hz line spacing and
% pseudo-random phases from a Park-Miller generator, so that MATLAB and Python
% build the same samples. Phases linear in the line index (a golden-ratio
% sequence, for instance) would make a pulse train, which a frame-wise analysis
% reads very differently from the long-term spectrum; the generator phases keep
% the signal stationary at the frame scale (crest factor about 10 dB).
cases(end+1) = mk('lcg_band',      'multisine 961-1040 Hz 60 dB, LCG phases',                 multisine_lcg(fs, dur, 961, 1040, 60), fs);
cases(end+1) = mk('lcg_tone_26dB', '1000 Hz 82 dB + multisine 912-1088 Hz 56 dB, LCG phases', tone(fs, dur, 1000, 82) + multisine_lcg(fs, dur, 912, 1088, 56), fs);
cases(end+1) = mk('lcg_tone_6dB',  '1000 Hz 82 dB + multisine 912-1088 Hz 76 dB, LCG phases', tone(fs, dur, 1000, 82) + multisine_lcg(fs, dur, 912, 1088, 76), fs);

% the Tonality_Aures1985 validation sounds of the SQAT v1.x data set (1 kHz tone
% at 82 dB SPL in one critical band of noise, the tone 0 to 80 dB over the band)
wavs = [];
if ~isempty(sounds_dir)
    wavs = dir(fullfile(sounds_dir, '**', '1Bark_tone_prominence_*dB_fc_1khz*.wav'));
end
for k = 1:numel(wavs)
    [x, fsw] = audioread(fullfile(wavs(k).folder, wavs(k).name), 'native');
    x = double(x(:, 1));
    tok = regexp(wavs(k).name, 'prominence_(\d+)dB', 'tokens', 'once');
    cases(end+1) = mk(sprintf('wav_%02ddB', str2double(tok{1})), wavs(k).name, x, fsw); %#ok<AGROW>
end

out = fullfile(here, 'sqat_aures_results.csv');
fid = fopen(out, 'w');
stamp = sprintf('# SQAT commit %s (%s), MATLAB %s, generated %s', sqat_commit, sqat_date, version, datestr(now, 'yyyy-mm-dd HH:MM'));
fprintf(fid, '%s\n', stamp);
fprintf(fid, 'case,description,fs,nframes,K_mean,K_max,K_median,wT_mean,wGr_mean\n');
fidf = fopen(fullfile(here, 'sqat_aures_frames.csv'), 'w');
fprintf(fidf, '%s\n', stamp);
fprintf(fidf, 'case,frame,time_s,K,wT,wGr\n');
fprintf('%-14s %-58s %8s %8s %8s %8s %8s\n', 'case', 'description', 'K_mean', 'K_max', 'K_med', 'wT', 'wGr');
for k = 1:numel(cases)
    c = cases(k);
    OUT = Tonality_Aures1985(c.x, c.fs, 0, 0, 0);   % free field, no time skip, no plot
    K   = OUT.InstantaneousTonality(:);
    wT  = OUT.TonalWeighting(:);
    wGr = OUT.LoudnessWeighting(:);
    fprintf(fid, '%s,"%s",%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f\n', c.name, c.desc, c.fs, numel(K), ...
        mean(K), max(K), median(K), mean(wT), mean(wGr));
    tt = frame_times(OUT, numel(K));
    for j = 1:numel(K)
        fprintf(fidf, '%s,%d,%.6f,%.6f,%.6f,%.6f\n', c.name, j, tt(j), K(j), wT(j), wGr(j));
    end
    fprintf('%-14s %-58s %8.4f %8.4f %8.4f %8.4f %8.4f\n', c.name, c.desc, mean(K), max(K), median(K), mean(wT), mean(wGr));
end
fclose(fid);
fclose(fidf);
fprintf('\nwritten: %s and sqat_aures_frames.csv\nSQAT commit %s (%s)\n', out, sqat_commit, sqat_date);
end

function tt = frame_times(OUT, n)
% time stamps of SQAT's frames as the toolbox reports them, in seconds
if isfield(OUT, 'time') && numel(OUT.time) == n
    tt = OUT.time(:);
else
    tt = (0:n - 1).' * 0.125;   % frame starts, 125 ms hop, if no time vector is given
end
end

function c = mk(name, desc, x, fs)
c = struct('name', name, 'desc', desc, 'x', x(:), 'fs', fs);
end

function x = tone(fs, dur, f, spl)
% zero-phase sinusoid in pascals; identical formula on the Python side
t = (0:round(fs * dur) - 1).' / fs;
x = sqrt(2) * 2e-5 * 10^(spl / 20) * sin(2 * pi * f * t);
end

function x = multisine_lcg(fs, dur, flo, fhi, spl)
% equal-amplitude lines at 1 Hz spacing from flo to fhi, pseudo-random phases
% from the Park-Miller generator (seed 12345, exact in double precision);
% identical formula on the Python side
t = (0:round(fs * dur) - 1).' / fs;
n = fhi - flo + 1;
amp = sqrt(2 / n) * 2e-5 * 10^(spl / 20);
s = 12345;
x = zeros(size(t));
for k = 0:n - 1
    s = mod(16807 * s, 2147483647);
    x = x + amp * sin(2 * pi * (flo + k) * t + 2 * pi * s / 2147483647);
end
end
