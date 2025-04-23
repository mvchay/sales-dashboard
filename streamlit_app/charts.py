
import matplotlib.pyplot as plt

def plot_bar_chart(df, x_col, y_col, title, xlabel="", ylabel="", rotation=45, color='skyblue'):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col], color=color)
    plt.title(title)
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.xticks(rotation=rotation)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return plt

def plot_line_chart(df, x_col, y_col, title, xlabel="", ylabel="", color='green'):
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o', color=color)
    plt.title(title)
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
