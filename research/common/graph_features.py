import numpy as np

import networkx as nx


class GraphFeatureExtractor:

    def extract(self, matrix):

        G = nx.from_numpy_array(matrix)

        degree = np.mean(

            list(

                dict(

                    G.degree(weight="weight")

                ).values()

            )

        )

        clustering = nx.average_clustering(

            G,

            weight="weight",

        )

        efficiency = nx.global_efficiency(G)

        density = nx.density(G)

        assortativity = nx.degree_assortativity_coefficient(G)

        return np.asarray([

            degree,

            clustering,

            efficiency,

            density,

            assortativity,

        ])
