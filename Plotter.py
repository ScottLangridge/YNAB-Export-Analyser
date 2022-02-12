import matplotlib.pyplot as plt


class Plotter:
    @staticmethod
    def dict_to_pie(data_dict):
        labels = [k for k in data_dict.keys()]
        values = [v for v in data_dict.values()]

        plt.pie(values, labels=labels)
        plt.axis('equal')
        plt.tight_layout()
        plt.legend()
        plt.show()
