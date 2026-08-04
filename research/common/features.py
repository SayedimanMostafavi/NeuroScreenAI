import numpy as np

from scipy.signal import welch

from scipy.stats import entropy


class FeatureExtractor:

    def __init__(self, sfreq=256):

        self.sfreq = sfreq

        self.bands = {
            "delta": (1, 4),
            "theta": (4, 8),
            "alpha": (8, 13),
            "beta": (13, 30),
            "gamma": (30, 40),
        }

    def _bandpower(self, freqs, psd, fmin, fmax):

        idx = (freqs >= fmin) & (freqs < fmax)

        return np.trapz(psd[idx], freqs[idx])

    def absolute_psd(self, window):

        features = []

        for ch in window:

            freqs, psd = welch(

                ch,

                fs=self.sfreq,

                nperseg=512,

            )

            for band in self.bands.values():

                features.append(

                    self._bandpower(

                        freqs,

                        psd,

                        band[0],

                        band[1],

                    )

                )

        return np.asarray(features)

    def relative_psd(self, window):

        features = []

        for ch in window:

            freqs, psd = welch(

                ch,

                fs=self.sfreq,

                nperseg=512,

            )

            total = self._bandpower(

                freqs,

                psd,

                1,

                40,

            )

            for band in self.bands.values():

                bp = self._bandpower(

                    freqs,

                    psd,

                    band[0],

                    band[1],

                )

                features.append(

                    bp / (total + 1e-12)

                )

        return np.asarray(features)

    def band_ratios(self, relative):

        ratios = []

        n = 5

        for ch in range(16):

            s = ch * n

            d = relative[s + 0]

            t = relative[s + 1]

            a = relative[s + 2]

            b = relative[s + 3]

            g = relative[s + 4]

            ratios.extend([

                t / (a + 1e-12),

                t / (b + 1e-12),

                a / (b + 1e-12),

                d / (a + 1e-12),

                b / (g + 1e-12),

            ])

        return np.asarray(ratios)

    def hjorth(self, window):

        feats = []

        for ch in window:

            d1 = np.diff(ch)

            d2 = np.diff(d1)

            var0 = np.var(ch)

            var1 = np.var(d1)

            var2 = np.var(d2)

            activity = var0

            mobility = np.sqrt(

                var1 / (var0 + 1e-12)

            )

            complexity = np.sqrt(

                var2 / (var1 + 1e-12)

            ) / (mobility + 1e-12)

            feats.extend([

                activity,

                mobility,

                complexity,

            ])

        return np.asarray(feats)

    def spectral_entropy(self, window):

        feats = []

        for ch in window:

            _, psd = welch(

                ch,

                fs=self.sfreq,

                nperseg=512,

            )

            p = psd / np.sum(psd)

            feats.append(

                entropy(p)

            )

        return np.asarray(feats)

    def faa(self, relative):

        idx = {

            "Fp1":0,

            "Fp2":1,

            "F3":2,

            "F4":3,

            "F7":4,

            "F8":5,

        }

        n = 5

        def alpha(i):

            return relative[i*n+2]

        return np.asarray([

            alpha(idx["Fp2"]) - alpha(idx["Fp1"]),

            alpha(idx["F4"]) - alpha(idx["F3"]),

            alpha(idx["F8"]) - alpha(idx["F7"]),

        ])

    def extract(self, window):

        abs_psd = self.absolute_psd(window)

        rel_psd = self.relative_psd(window)

        ratios = self.band_ratios(rel_psd)

        hj = self.hjorth(window)

        ent = self.spectral_entropy(window)

        faa = self.faa(rel_psd)

        return np.concatenate([

            abs_psd,

            rel_psd,

            ratios,

            hj,

            ent,

            faa,

        ]).astype(np.float32)
