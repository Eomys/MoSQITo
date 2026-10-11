function compare_sqat_aures_recordings(sqat_root, mosqito_root)
% compare_sqat_aures_recordings  SQAT's Tonality_Aures1985 on the recordings shipped with MoSQITo.
%
%   compare_sqat_aures_recordings(sqat_root)
%   compare_sqat_aures_recordings(sqat_root, mosqito_root)
%
%   Runs SQAT's Aures tonality on the ISO 532-1 Annex B.5 recordings and a
%   few other WAV files that MoSQITo ships for its own validations, with the
%   calibration MoSQITo uses for them (16-bit samples scaled to [-1, 1] and
%   multiplied by the factor in the table below), and writes next to this
%   file sqat_aures_recordings.csv (one row per file, statistics over the
%   frames) and sqat_aures_recordings_frames.csv (one row per frame, the
%   time series K(t) that MoSQITo's tonality_aures_tv is compared with).
%
%   Nothing is modified in either repository. SQAT (GPL-3.0) is only run,
%   not copied: this script contains no SQAT code.
%
%   Inputs
%     sqat_root    : folder of the SQAT clone (contains psychoacoustic_metrics/)
%     mosqito_root : folder of the MoSQITo clone; default: the repository this
%                    file is part of

if nargin < 1 || isempty(sqat_root), error('give the folder of the SQAT clone as first argument'); end
if nargin < 2 || isempty(mosqito_root), mosqito_root = fileparts(fileparts(fileparts(fileparts(fileparts(mfilename('fullpath')))))); end

addpath(genpath(sqat_root));
here = fileparts(mfilename('fullpath'));
[~, sqat_commit] = system(sprintf('git -C "%s" rev-parse --short HEAD', sqat_root));
sqat_commit = strtrim(sqat_commit);
[~, sqat_date] = system(sprintf('git -C "%s" log -1 --format=%%cs', sqat_root));
sqat_date = strtrim(sqat_date);

b5 = fullfile(mosqito_root, 'validations', 'sq_metrics', 'loudness_zwtv', 'input', 'ISO_532-1', 'Annex B.5');
b4 = fullfile(mosqito_root, 'validations', 'sq_metrics', 'loudness_zwtv', 'input', 'ISO_532-1', 'Annex B.4');
st = fullfile(mosqito_root, 'validations', 'sq_metrics', 'loudness_zwst', 'input', 'ISO_532_1');
ti = fullfile(mosqito_root, 'tests', 'input');

% {file, calibration factor applied after scaling the samples to [-1, 1]}
files = {
    fullfile(b5, 'Test signal 14 (propeller-driven airplane).wav'), 2*sqrt(2)
    fullfile(b5, 'Test signal 15 (vehicle interior 40 kmh).wav'),   2*sqrt(2)
    fullfile(b5, 'Test signal 16 (hairdryer).wav'),                 2*sqrt(2)
    fullfile(b5, 'Test signal 17 (machine gun).wav'),               2*sqrt(2)
    fullfile(b5, 'Test signal 18 (hammer).wav'),                    2*sqrt(2)
    fullfile(b5, 'Test signal 19 (door creak).wav'),                2*sqrt(2)
    fullfile(b5, 'Test signal 20 (shaking coins).wav'),             2*sqrt(2)
    fullfile(b5, 'Test signal 21 (jackhammer).wav'),                2*sqrt(2)
    fullfile(b5, 'Test signal 22 (ratchet wheel (large)).wav'),     2*sqrt(2)
    fullfile(b5, 'Test signal 23 (typewriter).wav'),                2*sqrt(2)
    fullfile(b5, 'Test signal 24 (woodpecker).wav'),                2*sqrt(2)
    fullfile(b5, 'Test signal 25 (full can rattle).wav'),           2*sqrt(2)
    fullfile(b4, 'Test signal 7 (tone 1 kHz 30 dB - 80 dB).wav'),   2*sqrt(2)
    fullfile(st, 'Test signal 3 (1 kHz 60 dB).wav'),                2*sqrt(2)
    fullfile(st, 'Test signal 5 (pinknoise 60 dB).wav'),            2*sqrt(2)
    fullfile(st, 'trafic.wav'),                                     2*sqrt(2)
    fullfile(ti, 'white_noise_442_1768_Hz_stationary.wav'),         0.01
    fullfile(ti, 'white_noise_200_2000_Hz_stationary.wav'),         2*sqrt(2)
};

stamp = sprintf('# SQAT commit %s (%s), MATLAB %s, generated %s', sqat_commit, sqat_date, version, datestr(now, 'yyyy-mm-dd HH:MM'));
out = fullfile(here, 'sqat_aures_recordings.csv');
fid = fopen(out, 'w');
fprintf(fid, '%s\n', stamp);
fprintf(fid, 'file,calib,fs,duration_s,Leq_dB,nframes,K_mean,K_median,K_max,K5,wT_mean,wGr_mean\n');
fidf = fopen(fullfile(here, 'sqat_aures_recordings_frames.csv'), 'w');
fprintf(fidf, '%s\n', stamp);
fprintf(fidf, 'file,frame,time_s,K,wT,wGr\n');
fprintf('%-52s %7s %5s %7s %7s %7s %7s\n', 'file', 'Leq', 'nfr', 'K_mean', 'K_med', 'K_max', 'K5');
for k = 1:size(files, 1)
    [x, fs] = audioread(files{k, 1});          % samples in [-1, 1]
    x = double(x(:, 1)) * files{k, 2};         % pascals, MoSQITo convention
    leq = 10 * log10(mean(x.^2) / 4e-10);
    OUT = Tonality_Aures1985(x, fs, 0, 0, 0);  % free field, no time skip, no plot
    K   = OUT.InstantaneousTonality(:);
    wT  = OUT.TonalWeighting(:);
    wGr = OUT.LoudnessWeighting(:);
    Ks  = sort(K, 'descend');
    K5  = Ks(max(1, round(0.05 * numel(Ks))));
    [~, name, ext] = fileparts(files{k, 1});
    fprintf(fid, '"%s",%g,%d,%.3f,%.1f,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n', [name ext], files{k, 2}, fs, ...
        numel(x) / fs, leq, numel(K), mean(K, 'omitnan'), median(K, 'omitnan'), max(K), K5, mean(wT, 'omitnan'), mean(wGr, 'omitnan'));
    tt = frame_times(OUT, numel(K));
    for j = 1:numel(K)
        fprintf(fidf, '"%s",%d,%.6f,%.6f,%.6f,%.6f\n', [name ext], j, tt(j), K(j), wT(j), wGr(j));
    end
    fprintf('%-52s %7.1f %5d %7.3f %7.3f %7.3f %7.3f\n', [name ext], leq, numel(K), mean(K, 'omitnan'), median(K, 'omitnan'), max(K), K5);
end
fclose(fid);
fclose(fidf);
fprintf('\nwritten: %s and sqat_aures_recordings_frames.csv\nSQAT commit %s (%s)\n', out, sqat_commit, sqat_date);
end

function tt = frame_times(OUT, n)
% time stamps of SQAT's frames as the toolbox reports them, in seconds
if isfield(OUT, 'time') && numel(OUT.time) == n
    tt = OUT.time(:);
else
    tt = (0:n - 1).' * 0.125;   % frame starts, 125 ms hop, if no time vector is given
end
end
